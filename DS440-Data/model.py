import numpy as np
import tensorflow as tf
from keras import layers



"""
TensorFlow (Keras) model:
Inputs:
  - queue:  (B, 5, 7) one-hot pieces
  - boards: (B, Kmax, 40, 10, 1) binary candidate resulting boards
  - mask:   (B, Kmax) 1=real candidate, 0=pad

Outputs:
  - logits: (B, Kmax) scores for each candidate index

Loss:
  - masked sparse softmax cross entropy over candidates
  - + beta * KL(q(z|x) || N(0, I))  (VAE-style regularizer)
"""
NEG_INF = -1e9


# ---------- Utils ----------
def apply_mask_to_logits(logits, mask):
    """logits: (B,Kmax), mask: (B,Kmax) in {0,1} -> masked logits"""
    mask = tf.cast(mask, logits.dtype)
    return tf.where(mask > 0, logits, tf.cast(NEG_INF, logits.dtype))


def masked_sparse_ce_loss(y_true, logits, mask):
    """y_true: (B,), logits: (B,Kmax), mask: (B,Kmax)"""
    masked_logits = apply_mask_to_logits(logits, mask)
    per_ex = tf.nn.sparse_softmax_cross_entropy_with_logits(
        labels=tf.cast(y_true, tf.int32),
        logits=masked_logits
    )
    return tf.reduce_mean(per_ex)


# ---------- VAE Sampling Layer ----------
class Sampling(layers.Layer):
    """Reparameterization trick: z = mu + exp(0.5*logvar) * eps"""
    def call(self, inputs):
        mu, logvar = inputs
        eps = tf.random.normal(shape=tf.shape(mu))
        return mu + tf.exp(0.5 * logvar) * eps


# ---------- Build Encoder ----------
def build_encoder(Kmax, latent_dim, board_h=40, board_w=10, board_c=1):
    # Inputs
    queue_in  = keras.Input(shape=(5, 7), name="queue")                       # (B,5,7)
    boards_in = keras.Input(shape=(Kmax, board_h, board_w, board_c), name="boards")  # (B,Kmax,40,10,1)
    mask_in   = keras.Input(shape=(Kmax,), name="mask")                       # (B,Kmax)

    # --- Queue embedding ---
    q = layers.Flatten()(queue_in)                # (B, 35)
    q = layers.Dense(64, activation="relu")(q)    # (B, 64)
    q = layers.Dense(64, activation="relu")(q)    # (B, 64)

    # --- Candidate boards -> per-candidate embedding via shared CNN ---
    # TimeDistributed applies the same CNN to each candidate board
    cnn = keras.Sequential([
        layers.Conv2D(16, 3, padding="same", activation="relu"),
        layers.MaxPool2D(pool_size=(2, 2)),
        layers.Conv2D(32, 3, padding="same", activation="relu"),
        layers.MaxPool2D(pool_size=(2, 2)),
        layers.Conv2D(64, 3, padding="same", activation="relu"),
        layers.GlobalAveragePooling2D(),          # -> (B, 64)
        layers.Dense(128, activation="relu"),     # -> (B, 128)
    ], name="board_cnn")

    cand_emb = layers.TimeDistributed(cnn, name="cand_emb")(boards_in)  # (B, Kmax, 128)

    # --- Masked pooling over candidates to summarize the set of candidates ---
    # mask: (B,Kmax) -> (B,Kmax,1)
    m = layers.Lambda(lambda t: tf.expand_dims(tf.cast(t, tf.float32), -1), name="mask_expand")(mask_in)
    cand_sum = layers.Lambda(lambda t: tf.reduce_sum(t[0] * t[1], axis=1), name="masked_sum")([cand_emb, m])  # (B,128)
    m_sum = layers.Lambda(lambda t: tf.reduce_sum(t, axis=1), name="mask_count")(m)                            # (B,1)
    m_sum = layers.Lambda(lambda t: tf.maximum(t, 1.0), name="mask_count_safe")(m_sum)
    cand_mean = layers.Lambda(lambda t: t[0] / t[1], name="masked_mean")([cand_sum, m_sum])                    # (B,128)

    # --- Combine queue + candidate-summary, then produce latent params ---
    h = layers.Concatenate()([q, cand_mean])      # (B, 64+128=192)
    h = layers.Dense(256, activation="relu")(h)
    h = layers.Dense(256, activation="relu")(h)

    mu = layers.Dense(latent_dim, name="z_mu")(h)
    logvar = layers.Dense(latent_dim, name="z_logvar")(h)

    z = Sampling(name="z_sample")([mu, logvar])

    return keras.Model([queue_in, boards_in, mask_in], [mu, logvar, z], name="encoder")


# ---------- Build Policy Head (MLP -> Kmax logits) ----------
def build_policy_head(Kmax):
    z_in = keras.Input(shape=(None,), name="z_in")  # latent_dim inferred
    h = layers.Dense(256, activation="relu")(z_in)
    h = layers.Dense(256, activation="relu")(h)
    logits = layers.Dense(Kmax, name="logits")(h)   # (B, Kmax)
    return keras.Model(z_in, logits, name="policy_head")


# ---------- Full Model w/ custom train_step ----------
class VAEPolicyModel(keras.Model):
    def __init__(self, Kmax, latent_dim, beta=1e-3, **kwargs):
        super().__init__(**kwargs)
        self.Kmax = Kmax
        self.latent_dim = latent_dim
        self.beta = beta

        self.encoder = build_encoder(Kmax=Kmax, latent_dim=latent_dim)
        self.policy_head = build_policy_head(Kmax=Kmax)

        # trackers
        self.loss_tracker = keras.metrics.Mean(name="loss")
        self.ce_tracker = keras.metrics.Mean(name="ce_loss")
        self.kl_tracker = keras.metrics.Mean(name="kl_loss")
        self.acc_tracker = keras.metrics.Mean(name="acc")  # masked accuracy over argmax

    @property
    def metrics(self):
        return [self.loss_tracker, self.ce_tracker, self.kl_tracker, self.acc_tracker]

    def call(self, inputs, training=False):
        queue, boards, mask = inputs
        mu, logvar, z = self.encoder([queue, boards, mask], training=training)
        logits = self.policy_head(z, training=training)
        return logits, mu, logvar

    def train_step(self, data):
        # data can be ([queue, boards, mask], y) OR ((queue, boards, mask), y)
        (x, y) = data
        queue, boards, mask = x

        with tf.GradientTape() as tape:
            logits, mu, logvar = self([queue, boards, mask], training=True)

            # main supervised loss (as described earlier)
            ce = masked_sparse_ce_loss(y, logits, mask)

            # KL(q(z|x) || N(0,I)) averaged over batch
            # KL = -0.5 * sum(1 + logvar - mu^2 - exp(logvar))
            kl_per_ex = -0.5 * tf.reduce_sum(
                1.0 + logvar - tf.square(mu) - tf.exp(logvar),
                axis=-1
            )
            kl = tf.reduce_mean(kl_per_ex)

            loss = ce + self.beta * kl

        grads = tape.gradient(loss, self.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables))

        # masked accuracy: argmax over masked logits compared to y
        masked_logits = apply_mask_to_logits(logits, mask)
        pred = tf.argmax(masked_logits, axis=-1, output_type=tf.int32)
        acc = tf.reduce_mean(tf.cast(tf.equal(pred, tf.cast(y, tf.int32)), tf.float32))

        self.loss_tracker.update_state(loss)
        self.ce_tracker.update_state(ce)
        self.kl_tracker.update_state(kl)
        self.acc_tracker.update_state(acc)

        return {m.name: m.result() for m in self.metrics}

    def test_step(self, data):
        (x, y) = data
        queue, boards, mask = x
        logits, mu, logvar = self([queue, boards, mask], training=False)

        ce = masked_sparse_ce_loss(y, logits, mask)
        kl_per_ex = -0.5 * tf.reduce_sum(
            1.0 + logvar - tf.square(mu) - tf.exp(logvar),
            axis=-1
        )
        kl = tf.reduce_mean(kl_per_ex)
        loss = ce + self.beta * kl

        masked_logits = apply_mask_to_logits(logits, mask)
        pred = tf.argmax(masked_logits, axis=-1, output_type=tf.int32)
        acc = tf.reduce_mean(tf.cast(tf.equal(pred, tf.cast(y, tf.int32)), tf.float32))

        self.loss_tracker.update_state(loss)
        self.ce_tracker.update_state(ce)
        self.kl_tracker.update_state(kl)
        self.acc_tracker.update_state(acc)
        return {m.name: m.result() for m in self.metrics}


# ---------- Example wiring ----------
if __name__ == "__main__":
    Kmax = 64          # choose based on your candidate generator upper bound
    latent_dim = 32
    beta = 1e-3        # KL weight; tune (often 1e-4 to 1e-2)

    model = VAEPolicyModel(Kmax=Kmax, latent_dim=latent_dim, beta=beta, name="vae_policy")

    # Compile (optimizer only; loss handled in train_step)
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-3))

    # Dummy batch to sanity-check shapes
    B = 8
    queue = tf.zeros((B, 5, 7), dtype=tf.float32)
    boards = tf.zeros((B, Kmax, 40, 10, 1), dtype=tf.float32)
    mask = tf.concat([tf.ones((B, 20)), tf.zeros((B, Kmax - 20))], axis=1)  # first 20 real
    y = tf.random.uniform((B,), minval=0, maxval=20, dtype=tf.int32)

    # One forward pass
    logits, mu, logvar = model([queue, boards, mask], training=False)
    print("logits:", logits.shape, "mu:", mu.shape, "logvar:", logvar.shape)

    # One train step
    out = model.train_on_batch([queue, boards, mask], y, return_dict=True)
    print(out)

    # Inference: predicted candidate index (ignoring padded)
    masked_logits = apply_mask_to_logits(logits, mask)
    pred_index = tf.argmax(masked_logits, axis=-1)
    print("pred_index:", pred_index.numpy())


