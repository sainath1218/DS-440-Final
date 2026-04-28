# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
from helpers import *
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

print('top of models2')
# init_board = getBoardMatrix("GGGGGNGGGGGGGGGGGGGNGGGGGGGGGNGGGGGGGGGNGGGGGGGGGNGGGGGGGGGNGGGGGGNGGGGGGGGNGGGGGGGGGNGGGGGGGGGNGGGGSSTTTLNJJJNSSTNNNLZJNNNNNNNLZZNNNNNNNLLZNNNNIIIIOONNNNNNNNOONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
# init_piece = "J"
# print(isValid(init_board, init_piece, 7, 37, 1))
# print(boardToString(init_board))

# print(len(sorted(boardStrings)))

# does the creation of df_transformed

def get_board_arrays(states, init_board_matrix, init_piece):
    seen = {}
    for px, py, r in states:
        arr = getBoardArray(init_board_matrix, init_piece, px, py, r)
        seen[tuple(arr)] = arr
    return list(seen.values())

def string_board_states(states, init_board_matrix, init_piece):
    boardStrings = []
    for px, py, r in states:
        boardStrings += [getBoardString(init_board_matrix, init_piece, px, py, r)]

    return sorted(list(set(boardStrings)))

'''
df = pd.read_pickle("data.pkl")
print('og df info')
print(df.info())


df = df.sort_values(['game_id', 'subframe']).reset_index(drop=True)
df['next_playfield'] = df.groupby('game_id')['playfield_transformed'].shift(-1)
df_transformed = df.dropna(subset=['next_playfield']).copy()
# added to remove the garbage issue NEEDS TO BE FIXED
df_transformed = df_transformed[df_transformed['immediate_garbage'] == 0]

df_transformed = df_transformed[[
    'playfield_transformed',
    'playfield',
    'placed',
    'hold',
    'next',         
    'next_playfield'   
]]
print('df transformed info')
print(df_transformed.info())


#already performed so it is just loaded now

# switching all of df_transformed to int for CNN
vocab = {"N":0,"G":1,"I":2,"O":3,"T":4,"S":5,"Z":6,"J":7,"L":8}
df_int = df_transformed.copy()
df_int['playfield_array'] = df_transformed['playfield_transformed'].apply(
    lambda s: np.array([vocab[c] for c in s], dtype=np.int32)
)
print('finshed transforming playfield to int arrays')
df_int['placed'] = df_transformed['placed'].apply(lambda s: vocab[s])
print('finshed transforming placed to int')
df_int['hold'] = df_transformed['hold'].apply(lambda s: vocab[s])
print('finshed transforming hold to int')

df_int['queue'] = df_transformed['next'].apply(
    lambda s: np.array([vocab[c] for c in s], dtype=np.int32)
)
print('finshed transforming queue to int arrays')
df_int['next_playfield']= df_transformed['next_playfield'].apply(
    lambda s: np.array([vocab[c] for c in s], dtype=np.int32)
)
print('finshed transforming next_playfield to int arrays')
df_int = df_int[[
    'playfield_array',
    'placed',
    'hold',
    'queue',         
    'next_playfield'   
]]

print('df int info')
df_int.to_pickle("df_int.pkl")
# df_int = pd.read_pickle("df_int.pkl")
print(df_int.info())
print(df_int.iloc[0])

inv_vocab = {0:"N", 1:"G", 2:"I", 3:"O", 4:"T", 5:"S", 6:"Z", 7:"J", 8:"L"}

'''
# for string
'''
playfield_counts=[]
failed = 0
boardStrings2 = []
for x in range(1000):
    boardStrings2 = [] 

    boardStrings1 = string_board_states(
        getAllBoardStates(getBoardMatrix(df_transformed.iloc[x]['playfield_transformed']), df_transformed.iloc[x]['placed'], False),
        getBoardMatrix(df_transformed.iloc[x]['playfield_transformed']),
        df_transformed.iloc[x]['placed']
    )
    

    if df_transformed.iloc[x]['hold'] != 'N':
        boardStrings2 = string_board_states(
            getAllBoardStates(getBoardMatrix(df_transformed.iloc[x]['playfield_transformed']), df_transformed.iloc[x]['hold'], False),
            getBoardMatrix(df_transformed.iloc[x]['playfield_transformed']),
            df_transformed.iloc[x]['hold']
        )
        playfield_counts.append(len(boardStrings2)+len(boardStrings1))
    else:
        playfield_counts.append(len(boardStrings1))

    if df_transformed.iloc[x]['next_playfield'] not in boardStrings1 and df_transformed.iloc[x]['next_playfield'] not in boardStrings2:
        # print(df_transformed.iloc[x]['playfield_transformed'])
        # print(df_transformed.iloc[x]['next_playfield'])
        # print(boardStrings1)
        # print(boardStrings2)
        # print(df_transformed.iloc[x]['placed'])
        # print(df_transformed.iloc[x]['hold'])
        # print('---')
        failed += 1
        



    # print(df_transformed.iloc[x]['next_playfield'])
    # print(boardStrings1, boardStrings2)
'''
#for numpy ints
'''
playfield_counts=[]
failed = 0
boardStrings2 = []
for x in range(0):
    boardStrings2 = [] 
    # print('playfield_array',df_int.iloc[x]['playfield_array'])

    boardStrings1 = get_board_arrays(
        getAllBoardStates(df_int.iloc[x]['playfield_array'], df_int.iloc[x]['placed'], True), 
                          mod_board_matrix_to_helper(df_int.iloc[x]['playfield_array']), 
                          inv_vocab[df_int.iloc[x]['placed']])

    if df_int.iloc[x]['hold'] != 0:
        boardStrings2 = get_board_arrays(
            getAllBoardStates(df_int.iloc[x]['playfield_array'], df_int.iloc[x]['hold'], True), 
                              mod_board_matrix_to_helper(df_int.iloc[x]['playfield_array']), 
                              inv_vocab[df_int.iloc[x]['hold']])
        playfield_counts.append(len(boardStrings2)+len(boardStrings1))
    else:
        playfield_counts.append(len(boardStrings1))

    boardSet1 = {tuple(arr) for arr in boardStrings1}
    boardSet2 = {tuple(arr) for arr in boardStrings2}

    if tuple(df_int.iloc[x]['next_playfield']) not in boardSet1 and tuple(df_int.iloc[x]['next_playfield']) not in boardSet2:

    # if df_int.iloc[x]['next_playfield'] not in boardStrings1 and df_int.iloc[x]['next_playfield'] not in boardStrings2:
        # print('playfield',df_int.iloc[x]['playfield_array'])
        # print('next playfield',df_int.iloc[x]['next_playfield'])
        # print(boardStrings1)
        # print(boardStrings2)
        # print(df_int.iloc[x]['placed'])
        # print(df_int.iloc[x]['hold'])
        # print('---')
        # print('mod_board_matrix_helper ',mod_board_matrix_to_helper(df_int.iloc[x]['playfield_array']))
        # print('placed piece',inv_vocab[df_int.iloc[x]['placed']])
        # print('transformed playfield',getBoardMatrix(df_transformed.iloc[x]['playfield_transformed']))
        # print('transformed placed',df_transformed.iloc[x]['placed'])
        # break
        failed += 1


print(f"Failed to find next_playfield in candidates {failed} out of {len(playfield_counts)}")
print(f"Average number of candidates: {sum(playfield_counts)/len(playfield_counts)}")
print(f"Max number of candidates: {max(playfield_counts)}")
'''
inv_vocab = {0:"N", 1:"G", 2:"I", 3:"O", 4:"T", 5:"S", 6:"Z", 7:"J", 8:"L"}

# takes in the padding size and the list of candidates and outputs the padded candidates and a mask of which candidates are real vs padding
def candidate_padding(input_candidates,padding_size = 128):
    output_candidates = np.zeros((padding_size, 400), dtype=np.int32)
    mask  = np.zeros((padding_size,), dtype=bool)
    for i , candidate in enumerate(input_candidates):
        output_candidates[i] = candidate
        mask[i] = True
    return output_candidates, mask

# sample_20k = df_int.iloc[:20000].copy()

def get_candidates_1(row):
    boards1 = get_board_arrays(
        getAllBoardStates(row['playfield_array'], row['placed'], True),
        mod_board_matrix_to_helper(row['playfield_array']),
        inv_vocab[row['placed']]
    )
    print('---')
    print('len getallboardstates', len(getAllBoardStates(row['playfield_array'], row['placed'], True)))
    print('got boards1', boards1)
    
    boards2 = []
    if row['hold'] != 0:
        boards2 = get_board_arrays(
            getAllBoardStates(row['playfield_array'], row['hold'], True),
            mod_board_matrix_to_helper(row['playfield_array']),
            inv_vocab[row['hold']]
        )
        print('got boards2', len(boards2))
    print('boards2=', boards2)
    boards, mask = candidate_padding(boards1 + boards2, padding_size=128)
    return boards, mask

def get_candidates_2(row):
    boards1 = get_board_arrays(
        getAllBoardStates(row['playfield_array'], row['placed'], True),
        mod_board_matrix_to_helper(row['playfield_array']),
        inv_vocab[row['placed']]
    )
    # print('---')
    # print('len getallboardstates', len(getAllBoardStates(row['playfield_array'], row['placed'], True)))
    # print('got boards1', boards1)
    
    boards2 = []
    if row['hold'] != 0:
        boards2 = get_board_arrays(
            getAllBoardStates(row['playfield_array'], row['hold'], True),
            mod_board_matrix_to_helper(row['playfield_array']),
            inv_vocab[row['hold']]
        )
    #     print('got boards2', len(boards2))
    # print('boards2=', boards2)
    return boards1 + boards2

# working with 20k
'''
print('working with 20k')
sample_20k['candidate_boards'] = sample_20k.apply(get_candidates_2, axis=1)
print('---')
thing = sample_20k.iloc[0]['candidate_boards']
print(len(thing))
print(sample_20k.info())
sample_20k.to_pickle("df_20k.pkl")
'''

#################################################################################
# testing models
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Conv2D, Flatten, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping

# print(-'top of model testing')
# df_20k = pd.read_pickle("./DS440-Data/df_20k.pkl")
# print(df_20k.columns)
# print(np.flip(df_20k['playfield_array'][20].reshape(40, 10), axis=0))

MAKE_NEW_DF=False
if MAKE_NEW_DF:
    print('working with 200k')
    df_int = pd.read_pickle("df_int.pkl")
    sample_50k = df_int.iloc[:200000].copy()
    sample_50k['candidate_boards'] = sample_50k.apply(get_candidates_2, axis=1)
    print('---')
    thing = sample_50k.iloc[0]['candidate_boards']
    print(len(thing))
    sample_50k['playfield_array'] = sample_50k['playfield_array'].apply(lambda arr: np.flip(arr.reshape(40, 10), axis=0))
    sample_50k['next_playfield'] = sample_50k['next_playfield'].apply(lambda arr: np.flip(arr.reshape(40, 10), axis=0))
    print(sample_50k.info())
    sample_50k = sample_50k.explode("candidate_boards").reset_index(drop=True)
    sample_50k = sample_50k.rename(columns={"candidate_boards": "candidate_board"})
    sample_50k['candidate_board'] = sample_50k['candidate_board'].apply(lambda arr: np.flip(arr.reshape(40, 10), axis=0))
    sample_50k["correct"] = sample_50k.apply(
        lambda row: int(np.array_equal(row["candidate_board"], row["next_playfield"])),
        axis=1
    )

    correct_df = sample_50k[sample_50k["correct"] == 1]
    incorrect_df = sample_50k[sample_50k["correct"] == 0]

    # target: final dataset should be 90% incorrect, 10% correct
    # so negatives should be 9 times the number of positives
    n_correct = len(correct_df)
    n_incorrect_keep = 9 * n_correct

    # sample negatives
    incorrect_df = incorrect_df.sample(n=min(n_incorrect_keep, len(incorrect_df)), random_state=42)

    # combine back together
    sample_50k = pd.concat([correct_df, incorrect_df], ignore_index=True)

    # shuffle rows
    sample_50k = sample_50k.sample(frac=1, random_state=42).reset_index(drop=True)

    # check result
    print(sample_50k["correct"].value_counts(normalize=True))
    print(sample_50k["correct"].value_counts())

    print(sample_50k)

    sample_50k.to_pickle("sample_200k.pkl")

else:
    print('loading 200k')
    sample_50k = pd.read_pickle("sample_200k.pkl")
    print('loaded 200k')
# this model only takes in the board states and attempts to score them on its own 
def model_only_using_moves():

    board_input = Input(shape=(40, 10, 1), name="board_input") # shape is 40 rows 10 cols and 1 channel

    # takes the input board and learns to recognize base patterns and featurs of the boards and outputs it as a set of 32 feature maps.
    x = Conv2D(
        filters=32, # gens 32 weights
        kernel_size=(4, 4), # looks at 4x4 sections of the board at a time
        strides=(1, 1), # moves the window 1 cell at a time
        padding="same", # 
        activation="relu",
        name="conv1"
    )(board_input)

    # takes the 32 feature maps and learns to recognize pattern/feature combos.
    x = Conv2D(
        filters=64, # gens 64 weights
        kernel_size=(4, 4), # looks at 4x4 sections of the board at a time
        strides=(1, 1), # moves the window 1 cell at a time
        padding="same", 
        activation="relu",
        name="conv2"
    )(x)

    # flattens the output from the conv layers into a 1d vector for the dense layers to process.
    x = Flatten(name="flatten")(x)

    # takes the massive flattened vector and refines it to 128 features
    x = Dense(
        units=128, # number of neurons per layer
        activation="relu",
        name="dense1"
    )(x)

    # takes the 128 features and refines it to 64 features
    x = Dense(
        units=64, # number of neurons per layer
        activation="relu",
        name="dense2"
    )(x)

    # outputs one number which is a board score
    score_output = Dense(
        units=1, 
        activation=None,
        name="score"
    )(x)

    model = Model(inputs=board_input, outputs=score_output, name="tetris_board_scorer")

    model.summary()

def model_2(train_queue, train_hold, train_place, train_start, train_candidate,train_y):
    queue_input = Input(shape=(14,), name="queue_input")
    hold_input = Input(shape=(1,), name="hold_input")
    place_input = Input(shape=(1,), name="place_input")

    start_board_input = Input(shape=(40, 10, 1), name="start_board_input")
    candidate_board_input = Input(shape=(40, 10, 1), name="candidate_board_input")

    # learning start board
        # takes the input board and learns to recognize base patterns and featurs of the boards and outputs it as a set of 32 feature maps.
    s = Conv2D(
        filters=32, # gens 32 weights
        kernel_size=(4, 4), # looks at 4x4 sections of the board at a time
        strides=(1, 1), # moves the window 1 cell at a time
        padding="same", # 
        activation="relu",
        name="conv11"
    )(start_board_input)

    # takes the 32 feature maps and learns to recognize pattern/feature combos.
    s = Conv2D(
        filters=64, # gens 64 weights
        kernel_size=(4, 4), # looks at 4x4 sections of the board at a time
        strides=(1, 1), # moves the window 1 cell at a time
        padding="same", 
        activation="relu",
        name="conv12"
    )(s)

    # flattens the output from the conv layers into a 1d vector for the dense layers to process.
    s = Flatten(name="flatten1")(s)

    # takes the massive flattened vector and refines it to 128 features
    s = Dense(
        units=128, # number of neurons per layer
        activation="relu",
        name="dense1"
    )(s)

    #####
    # learns candidate board
    #####
    c = Conv2D(
        filters=32, # gens 32 weights
        kernel_size=(4, 4), # looks at 4x4 sections of the board at a time
        strides=(1, 1), # moves the window 1 cell at a time
        padding="same", # 
        activation="relu",
        name="conv21"
    )(candidate_board_input)

    # takes the 32 feature maps and learns to recognize pattern/feature combos.
    c = Conv2D(
        filters=64, # gens 64 weights
        kernel_size=(4, 4), # looks at 4x4 sections of the board at a time
        strides=(1, 1), # moves the window 1 cell at a time
        padding="same", 
        activation="relu",
        name="conv22"
    )(c)

    # flattens the output from the conv layers into a 1d vector for the dense layers to process.
    c = Flatten(name="flatten2")(c)

    # takes the massive flattened vector and refines it to 128 features
    c = Dense(
        units=128, # number of neurons per layer
        activation="relu",
        name="dense2"
    )(c)

    #####
    # learns q, hold, place
    #####
    meta = Concatenate(name="meta_concat")([queue_input, hold_input, place_input])
    meta = Dense(32, activation="relu", name="meta_dense1")(meta)
    meta = Dense(16, activation="relu", name="meta_dense2")(meta)

    #####
    # combine the seperate layers
    #####
    x = Concatenate(name="all_features")([s, c, meta])
    x = Dense(128, activation="relu", name="combined_dense1")(x)
    x = Dense(64, activation="relu", name="combined_dense2")(x)

    #####
    # output one number which is a board score
    #####
    output = Dense(1, activation="sigmoid", name="chosen_prob")(x)
    
    model = Model(
    inputs=[queue_input, hold_input, place_input, start_board_input, candidate_board_input],
    outputs=output,
    name="tetris_choice_model")

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall"),
            tf.keras.metrics.AUC(name="auc")
        ]
    )

    model.summary()

    early_stop = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)


    model.fit(
    [train_queue, train_hold, train_place, train_start, train_candidate],
    train_y,
    batch_size=32,
    epochs=20,
    validation_split=0.2,
    callbacks=[early_stop])

    print('finished training model 2')
    model.save("tetris_model_200k.keras")
    print('saved model 2')
    # preds = model.predict([Q_batch, H_batch, P_batch, S_batch, C_batch])
    # best_idx = preds.argmax()
    # best_candidate = candidate_boards[best_idx]


train_df, test_df = train_test_split(sample_50k, test_size=0.2, random_state=42)
print('starting to train model 2')
model_2(
    train_queue=np.stack(train_df['queue'].values),
    train_hold=np.stack(train_df['hold'].values),
    train_place=np.stack(train_df['placed'].values),
    train_start=np.stack(train_df['playfield_array'].values),
    train_candidate=np.stack(train_df['candidate_board'].values),
    train_y=train_df['correct'].values
)


'''
correct
0    465300
1     51700

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Layer (type)                  ┃ Output Shape              ┃         Param # ┃ Connected to               ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ start_board_input             │ (None, 40, 10, 1)         │               0 │ -                          │
│ (InputLayer)                  │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ candidate_board_input         │ (None, 40, 10, 1)         │               0 │ -                          │
│ (InputLayer)                  │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ conv11 (Conv2D)               │ (None, 40, 10, 32)        │             544 │ start_board_input[0][0]    │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ conv21 (Conv2D)               │ (None, 40, 10, 32)        │             544 │ candidate_board_input[0][… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ queue_input (InputLayer)      │ (None, 14)                │               0 │ -                          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ hold_input (InputLayer)       │ (None, 1)                 │               0 │ -                          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ place_input (InputLayer)      │ (None, 1)                 │               0 │ -                          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ conv12 (Conv2D)               │ (None, 40, 10, 64)        │          32,832 │ conv11[0][0]               │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ conv22 (Conv2D)               │ (None, 40, 10, 64)        │          32,832 │ conv21[0][0]               │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ meta_concat (Concatenate)     │ (None, 16)                │               0 │ queue_input[0][0],         │
│                               │                           │                 │ hold_input[0][0],          │
│                               │                           │                 │ place_input[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ flatten1 (Flatten)            │ (None, 25600)             │               0 │ conv12[0][0]               │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ flatten2 (Flatten)            │ (None, 25600)             │               0 │ conv22[0][0]               │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ meta_dense1 (Dense)           │ (None, 32)                │             544 │ meta_concat[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ dense1 (Dense)                │ (None, 128)               │       3,276,928 │ flatten1[0][0]             │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ dense2 (Dense)                │ (None, 128)               │       3,276,928 │ flatten2[0][0]             │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ meta_dense2 (Dense)           │ (None, 16)                │             528 │ meta_dense1[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ all_features (Concatenate)    │ (None, 272)               │               0 │ dense1[0][0],              │
│                               │                           │                 │ dense2[0][0],              │
│                               │                           │                 │ meta_dense2[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ combined_dense1 (Dense)       │ (None, 128)               │          34,944 │ all_features[0][0]         │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ combined_dense2 (Dense)       │ (None, 64)                │           8,256 │ combined_dense1[0][0]      │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ chosen_prob (Dense)           │ (None, 1)                 │              65 │ combined_dense2[0][0]      │
└───────────────────────────────┴───────────────────────────┴─────────────────┴────────────────────────────┘
 Total params: 6,664,945 (25.42 MB)
 Trainable params: 6,664,945 (25.42 MB)
 Non-trainable params: 0 (0.00 B)
Epoch 1/10
10340/10340 ━━━━━━━━━━━━━━━━━━━━ 268s 26ms/step - accuracy: 0.9115 - loss: 0.2073 - val_accuracy: 0.9168 - val_loss: 0.1877
Epoch 2/10
10340/10340 ━━━━━━━━━━━━━━━━━━━━ 260s 25ms/step - accuracy: 0.9239 - loss: 0.1735 - val_accuracy: 0.9239 - val_loss: 0.1740
Epoch 3/10
10340/10340 ━━━━━━━━━━━━━━━━━━━━ 261s 25ms/step - accuracy: 0.9300 - loss: 0.1585 - val_accuracy: 0.9270 - val_loss: 0.1629
Epoch 4/10
10340/10340 ━━━━━━━━━━━━━━━━━━━━ 263s 25ms/step - accuracy: 0.9349 - loss: 0.1472 - val_accuracy: 0.9272 - val_loss: 0.1597
Epoch 5/10
10340/10340 ━━━━━━━━━━━━━━━━━━━━ 273s 26ms/step - accuracy: 0.9402 - loss: 0.1363 - val_accuracy: 0.9280 - val_loss: 0.1585
Epoch 6/10
10340/10340 ━━━━━━━━━━━━━━━━━━━━ 268s 26ms/step - accuracy: 0.9452 - loss: 0.1258 - val_accuracy: 0.9276 - val_loss: 0.1626
Epoch 7/10
10340/10340 ━━━━━━━━━━━━━━━━━━━━ 261s 25ms/step - accuracy: 0.9517 - loss: 0.1136 - val_accuracy: 0.9271 - val_loss: 0.1672
Epoch 8/10
10340/10340 ━━━━━━━━━━━━━━━━━━━━ 270s 26ms/step - accuracy: 0.9586 - loss: 0.1001 - val_accuracy: 0.9269 - val_loss: 0.2037
Epoch 9/10
10340/10340 ━━━━━━━━━━━━━━━━━━━━ 263s 25ms/step - accuracy: 0.9649 - loss: 0.0873 - val_accuracy: 0.9270 - val_loss: 0.1824
Epoch 10/10
10340/10340 ━━━━━━━━━━━━━━━━━━━━ 264s 26ms/step - accuracy: 0.9701 - loss: 0.0756 - val_accuracy: 0.9272 - val_loss: 0.2041
finished training model 2
saved model 2
'''
### 200k failed to save :(

"""
(tf-gpu) rowan@rowansLegion:/mnt/c/Users/rowan/Desktop/Classes/DS 440/TETRIS MASTER/DS440-Data$ python models2.py
top of models2
2026-04-16 13:04:00.432249: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2026-04-16 13:04:00.521641: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
E0000 00:00:1776359040.568728   82344 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered
E0000 00:00:1776359040.588657   82344 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered
W0000 00:00:1776359040.703852   82344 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.
W0000 00:00:1776359040.703916   82344 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.
W0000 00:00:1776359040.703920   82344 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.
W0000 00:00:1776359040.703923   82344 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.
2026-04-16 13:04:00.720937: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 AVX512F AVX512_VNNI AVX512_BF16 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
loading 200k
loaded 200k
starting to train model 2
I0000 00:00:1776359117.546990   82344 gpu_device.cc:2019] Created device /job:localhost/replica:0/task:0/device:GPU:0 with 13508 MB memory:  -> device: 0, name: NVIDIA GeForce RTX 4090 Laptop GPU, pci bus id: 0000:01:00.0, compute capability: 8.9
Model: "tetris_choice_model"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Layer (type)                  ┃ Output Shape              ┃         Param # ┃ Connected to               ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ start_board_input             │ (None, 40, 10, 1)         │               0 │ -                          │
│ (InputLayer)                  │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ candidate_board_input         │ (None, 40, 10, 1)         │               0 │ -                          │
│ (InputLayer)                  │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ conv11 (Conv2D)               │ (None, 40, 10, 32)        │             544 │ start_board_input[0][0]    │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ conv21 (Conv2D)               │ (None, 40, 10, 32)        │             544 │ candidate_board_input[0][… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ queue_input (InputLayer)      │ (None, 14)                │               0 │ -                          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ hold_input (InputLayer)       │ (None, 1)                 │               0 │ -                          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ place_input (InputLayer)      │ (None, 1)                 │               0 │ -                          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ conv12 (Conv2D)               │ (None, 40, 10, 64)        │          32,832 │ conv11[0][0]               │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ conv22 (Conv2D)               │ (None, 40, 10, 64)        │          32,832 │ conv21[0][0]               │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ meta_concat (Concatenate)     │ (None, 16)                │               0 │ queue_input[0][0],         │
│                               │                           │                 │ hold_input[0][0],          │
│                               │                           │                 │ place_input[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ flatten1 (Flatten)            │ (None, 25600)             │               0 │ conv12[0][0]               │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ flatten2 (Flatten)            │ (None, 25600)             │               0 │ conv22[0][0]               │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ meta_dense1 (Dense)           │ (None, 32)                │             544 │ meta_concat[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ dense1 (Dense)                │ (None, 128)               │       3,276,928 │ flatten1[0][0]             │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ dense2 (Dense)                │ (None, 128)               │       3,276,928 │ flatten2[0][0]             │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ meta_dense2 (Dense)           │ (None, 16)                │             528 │ meta_dense1[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ all_features (Concatenate)    │ (None, 272)               │               0 │ dense1[0][0],              │
│                               │                           │                 │ dense2[0][0],              │
│                               │                           │                 │ meta_dense2[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ combined_dense1 (Dense)       │ (None, 128)               │          34,944 │ all_features[0][0]         │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ combined_dense2 (Dense)       │ (None, 64)                │           8,256 │ combined_dense1[0][0]      │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ chosen_prob (Dense)           │ (None, 1)                 │              65 │ combined_dense2[0][0]      │
└───────────────────────────────┴───────────────────────────┴─────────────────┴────────────────────────────┘
 Total params: 6,664,945 (25.42 MB)
 Trainable params: 6,664,945 (25.42 MB)
 Non-trainable params: 0 (0.00 B)
Epoch 1/20
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1776359129.981641   83221 service.cc:152] XLA service 0x7ce530026f50 initialized for platform CUDA (this does not guarantee that XLA will be used). Devices:
I0000 00:00:1776359129.981702   83221 service.cc:160]   StreamExecutor device (0): NVIDIA GeForce RTX 4090 Laptop GPU, Compute Capability 8.9
2026-04-16 13:05:30.043260: I tensorflow/compiler/mlir/tensorflow/utils/dump_mlir_util.cc:269] disabling MLIR crash reproducer, set env var `MLIR_CRASH_REPRODUCER_DIRECTORY` to enable.
I0000 00:00:1776359130.336307   83221 cuda_dnn.cc:529] Loaded cuDNN version 90300
2026-04-16 13:05:30.903904: I external/local_xla/xla/stream_executor/cuda/subprocess_compilation.cc:346] ptxas warning : Registers are spilled to local memory in function 'gemm_fusion_dot_695', 12 bytes spill stores, 12 bytes spill loads

2026-04-16 13:05:30.935323: I external/local_xla/xla/stream_executor/cuda/subprocess_compilation.cc:346] ptxas warning : Registers are spilled to local memory in function 'gemm_fusion_dot_695', 4 bytes spill stores, 4 bytes spill loads

I0000 00:00:1776359132.454760   83221 device_compiler.h:188] Compiled cluster using XLA!  This line is logged at most once for the lifetime of the process.
41380/41383 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - accuracy: 0.9161 - auc: 0.9091 - loss: 0.1986 - precision: 0.6186 - recall: 0.37902026-04-16 13:09:12.235524: I external/local_xla/xla/stream_executor/cuda/subprocess_compilation.cc:346] ptxas warning : Registers are spilled to local memory in function 'gemm_fusion_dot_195', 4 bytes spill stores, 4 bytes spill loads

2026-04-16 13:09:12.240522: I external/local_xla/xla/stream_executor/cuda/subprocess_compilation.cc:346] ptxas warning : Registers are spilled to local memory in function 'gemm_fusion_dot_195', 12 bytes spill stores, 12 bytes spill loads

41383/41383 ━━━━━━━━━━━━━━━━━━━━ 224s 5ms/step - accuracy: 0.9234 - auc: 0.9369 - loss: 0.1752 - precision: 0.6585 - recall: 0.4865 - val_accuracy: 0.9294 - val_auc: 0.9521 - val_loss: 0.1579 - val_precision: 0.6384 - val_recall: 0.6596
Epoch 2/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 223s 5ms/step - accuracy: 0.9345 - auc: 0.9565 - loss: 0.1485 - precision: 0.6971 - recall: 0.6102 - val_accuracy: 0.9362 - val_auc: 0.9592 - val_loss: 0.1443 - val_precision: 0.7289 - val_recall: 0.5645
Epoch 3/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 219s 5ms/step - accuracy: 0.9399 - auc: 0.9630 - loss: 0.1376 - precision: 0.7118 - recall: 0.6709 - val_accuracy: 0.9412 - val_auc: 0.9637 - val_loss: 0.1343 - val_precision: 0.7138 - val_recall: 0.6766
Epoch 4/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 220s 5ms/step - accuracy: 0.9444 - auc: 0.9677 - loss: 0.1287 - precision: 0.7305 - recall: 0.7037 - val_accuracy: 0.9421 - val_auc: 0.9663 - val_loss: 0.1329 - val_precision: 0.7031 - val_recall: 0.7174
Epoch 5/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 232s 6ms/step - accuracy: 0.9477 - auc: 0.9709 - loss: 0.1221 - precision: 0.7430 - recall: 0.7291 - val_accuracy: 0.9422 - val_auc: 0.9674 - val_loss: 0.1309 - val_precision: 0.6859 - val_recall: 0.7660
Epoch 6/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 224s 5ms/step - accuracy: 0.9507 - auc: 0.9733 - loss: 0.1167 - precision: 0.7577 - recall: 0.7453 - val_accuracy: 0.9444 - val_auc: 0.9666 - val_loss: 0.1294 - val_precision: 0.7447 - val_recall: 0.6657
Epoch 7/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 214s 5ms/step - accuracy: 0.9533 - auc: 0.9756 - loss: 0.1116 - precision: 0.7698 - recall: 0.7600 - val_accuracy: 0.9455 - val_auc: 0.9677 - val_loss: 0.1285 - val_precision: 0.7275 - val_recall: 0.7168
Epoch 8/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 210s 5ms/step - accuracy: 0.9557 - auc: 0.9774 - loss: 0.1072 - precision: 0.7823 - recall: 0.7724 - val_accuracy: 0.9436 - val_auc: 0.9674 - val_loss: 0.1289 - val_precision: 0.7422 - val_recall: 0.6578
Epoch 9/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 226s 5ms/step - accuracy: 0.9580 - auc: 0.9788 - loss: 0.1033 - precision: 0.7932 - recall: 0.7848 - val_accuracy: 0.9449 - val_auc: 0.9534 - val_loss: 0.1884 - val_precision: 0.7201 - val_recall: 0.7231
Epoch 10/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 219s 5ms/step - accuracy: 0.9601 - auc: 0.9805 - loss: 0.0985 - precision: 0.8159 - recall: 0.7765 - val_accuracy: 0.9423 - val_auc: 0.9607 - val_loss: 0.1518 - val_precision: 0.7586 - val_recall: 0.6101
Epoch 11/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 213s 5ms/step - accuracy: 0.9621 - auc: 0.9819 - loss: 0.0944 - precision: 0.8279 - recall: 0.7836 - val_accuracy: 0.9416 - val_auc: 0.9633 - val_loss: 0.1401 - val_precision: 0.7750 - val_recall: 0.5761
Epoch 12/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 217s 5ms/step - accuracy: 0.9641 - auc: 0.9832 - loss: 0.0905 - precision: 0.8379 - recall: 0.7942 - val_accuracy: 0.9424 - val_auc: 0.9579 - val_loss: 0.1620 - val_precision: 0.7571 - val_recall: 0.6145

"""

# model saved
"""
(tf-gpu) rowan@rowansLegion:/mnt/c/Users/rowan/Desktop/Classes/DS 440/TETRIS MASTER/DS440-Data$ python models2.py
top of models2
2026-04-16 13:55:20.233715: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2026-04-16 13:55:20.275770: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
E0000 00:00:1776362120.301007  115032 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered
E0000 00:00:1776362120.308769  115032 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered
W0000 00:00:1776362120.346362  115032 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.
W0000 00:00:1776362120.346421  115032 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.
W0000 00:00:1776362120.346426  115032 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.
W0000 00:00:1776362120.346428  115032 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.
2026-04-16 13:55:20.356217: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 AVX512F AVX512_VNNI AVX512_BF16 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
loading 200k
loaded 200k
starting to train model 2
I0000 00:00:1776362190.529214  115032 gpu_device.cc:2019] Created device /job:localhost/replica:0/task:0/device:GPU:0 with 13508 MB memory:  -> device: 0, name: NVIDIA GeForce RTX 4090 Laptop GPU, pci bus id: 0000:01:00.0, compute capability: 8.9
Model: "tetris_choice_model"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Layer (type)                  ┃ Output Shape              ┃         Param # ┃ Connected to               ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ start_board_input             │ (None, 40, 10, 1)         │               0 │ -                          │
│ (InputLayer)                  │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ candidate_board_input         │ (None, 40, 10, 1)         │               0 │ -                          │
│ (InputLayer)                  │                           │                 │                            │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ conv11 (Conv2D)               │ (None, 40, 10, 32)        │             544 │ start_board_input[0][0]    │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ conv21 (Conv2D)               │ (None, 40, 10, 32)        │             544 │ candidate_board_input[0][… │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ queue_input (InputLayer)      │ (None, 14)                │               0 │ -                          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ hold_input (InputLayer)       │ (None, 1)                 │               0 │ -                          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ place_input (InputLayer)      │ (None, 1)                 │               0 │ -                          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ conv12 (Conv2D)               │ (None, 40, 10, 64)        │          32,832 │ conv11[0][0]               │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ conv22 (Conv2D)               │ (None, 40, 10, 64)        │          32,832 │ conv21[0][0]               │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ meta_concat (Concatenate)     │ (None, 16)                │               0 │ queue_input[0][0],         │
│                               │                           │                 │ hold_input[0][0],          │
│                               │                           │                 │ place_input[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ flatten1 (Flatten)            │ (None, 25600)             │               0 │ conv12[0][0]               │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ flatten2 (Flatten)            │ (None, 25600)             │               0 │ conv22[0][0]               │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ meta_dense1 (Dense)           │ (None, 32)                │             544 │ meta_concat[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ dense1 (Dense)                │ (None, 128)               │       3,276,928 │ flatten1[0][0]             │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ dense2 (Dense)                │ (None, 128)               │       3,276,928 │ flatten2[0][0]             │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ meta_dense2 (Dense)           │ (None, 16)                │             528 │ meta_dense1[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ all_features (Concatenate)    │ (None, 272)               │               0 │ dense1[0][0],              │
│                               │                           │                 │ dense2[0][0],              │
│                               │                           │                 │ meta_dense2[0][0]          │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ combined_dense1 (Dense)       │ (None, 128)               │          34,944 │ all_features[0][0]         │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ combined_dense2 (Dense)       │ (None, 64)                │           8,256 │ combined_dense1[0][0]      │
├───────────────────────────────┼───────────────────────────┼─────────────────┼────────────────────────────┤
│ chosen_prob (Dense)           │ (None, 1)                 │              65 │ combined_dense2[0][0]      │
└───────────────────────────────┴───────────────────────────┴─────────────────┴────────────────────────────┘
 Total params: 6,664,945 (25.42 MB)
 Trainable params: 6,664,945 (25.42 MB)
 Non-trainable params: 0 (0.00 B)
Epoch 1/20
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1776362204.390348  115822 service.cc:152] XLA service 0x7d4cd4005780 initialized for platform CUDA (this does not guarantee that XLA will be used). Devices:
I0000 00:00:1776362204.390613  115822 service.cc:160]   StreamExecutor device (0): NVIDIA GeForce RTX 4090 Laptop GPU, Compute Capability 8.9
2026-04-16 13:56:44.452930: I tensorflow/compiler/mlir/tensorflow/utils/dump_mlir_util.cc:269] disabling MLIR crash reproducer, set env var `MLIR_CRASH_REPRODUCER_DIRECTORY` to enable.
I0000 00:00:1776362204.710715  115822 cuda_dnn.cc:529] Loaded cuDNN version 90300
2026-04-16 13:56:45.221009: I external/local_xla/xla/stream_executor/cuda/subprocess_compilation.cc:346] ptxas warning : Registers are spilled to local memory in function 'gemm_fusion_dot_695', 4 bytes spill stores, 4 bytes spill loads

2026-04-16 13:56:45.229380: I external/local_xla/xla/stream_executor/cuda/subprocess_compilation.cc:346] ptxas warning : Registers are spilled to local memory in function 'gemm_fusion_dot_695', 12 bytes spill stores, 12 bytes spill loads

I0000 00:00:1776362206.747344  115822 device_compiler.h:188] Compiled cluster using XLA!  This line is logged at most once for the lifetime of the process.
41374/41383 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - accuracy: 0.9147 - auc: 0.9053 - loss: 0.2016 - precision: 0.6096 - recall: 0.36572026-04-16 14:00:21.093883: I external/local_xla/xla/stream_executor/cuda/subprocess_compilation.cc:346] ptxas warning : Registers are spilled to local memory in function 'gemm_fusion_dot_195', 4 bytes spill stores, 4 bytes spill loads

2026-04-16 14:00:21.124025: I external/local_xla/xla/stream_executor/cuda/subprocess_compilation.cc:346] ptxas warning : Registers are spilled to local memory in function 'gemm_fusion_dot_195', 12 bytes spill stores, 12 bytes spill loads

41383/41383 ━━━━━━━━━━━━━━━━━━━━ 219s 5ms/step - accuracy: 0.9222 - auc: 0.9352 - loss: 0.1772 - precision: 0.6484 - recall: 0.4843 - val_accuracy: 0.9323 - val_auc: 0.9533 - val_loss: 0.1527 - val_precision: 0.6831 - val_recall: 0.5879
Epoch 2/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 212s 5ms/step - accuracy: 0.9336 - auc: 0.9557 - loss: 0.1498 - precision: 0.6849 - recall: 0.6223 - val_accuracy: 0.9358 - val_auc: 0.9582 - val_loss: 0.1448 - val_precision: 0.6944 - val_recall: 0.6265
Epoch 3/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 340s 8ms/step - accuracy: 0.9375 - auc: 0.9601 - loss: 0.1424 - precision: 0.7007 - recall: 0.6549 - val_accuracy: 0.9361 - val_auc: 0.9601 - val_loss: 0.1425 - val_precision: 0.6699 - val_recall: 0.6962
Epoch 4/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 234s 6ms/step - accuracy: 0.9401 - auc: 0.9632 - loss: 0.1370 - precision: 0.7110 - recall: 0.6750 - val_accuracy: 0.9372 - val_auc: 0.9611 - val_loss: 0.1405 - val_precision: 0.6779 - val_recall: 0.6948
Epoch 5/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 211s 5ms/step - accuracy: 0.9420 - auc: 0.9654 - loss: 0.1332 - precision: 0.7175 - recall: 0.6924 - val_accuracy: 0.9371 - val_auc: 0.9616 - val_loss: 0.1397 - val_precision: 0.6700 - val_recall: 0.7163
Epoch 6/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 213s 5ms/step - accuracy: 0.9444 - auc: 0.9675 - loss: 0.1291 - precision: 0.7300 - recall: 0.7047 - val_accuracy: 0.9375 - val_auc: 0.9610 - val_loss: 0.1421 - val_precision: 0.7406 - val_recall: 0.5657
Epoch 7/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 228s 5ms/step - accuracy: 0.9462 - auc: 0.9689 - loss: 0.1263 - precision: 0.7380 - recall: 0.7156 - val_accuracy: 0.9348 - val_auc: 0.9605 - val_loss: 0.1480 - val_precision: 0.7706 - val_recall: 0.4846
Epoch 8/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 217s 5ms/step - accuracy: 0.9479 - auc: 0.9705 - loss: 0.1229 - precision: 0.7478 - recall: 0.7233 - val_accuracy: 0.9388 - val_auc: 0.9605 - val_loss: 0.1415 - val_precision: 0.7048 - val_recall: 0.6558
Epoch 9/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 221s 5ms/step - accuracy: 0.9499 - auc: 0.9721 - loss: 0.1192 - precision: 0.7538 - recall: 0.7408 - val_accuracy: 0.9373 - val_auc: 0.9619 - val_loss: 0.1407 - val_precision: 0.6717 - val_recall: 0.7158
Epoch 10/20
41383/41383 ━━━━━━━━━━━━━━━━━━━━ 217s 5ms/step - accuracy: 0.9517 - auc: 0.9736 - loss: 0.1160 - precision: 0.7640 - recall: 0.7486 - val_accuracy: 0.9383 - val_auc: 0.9606 - val_loss: 0.1444 - val_precision: 0.7112 - val_recall: 0.6318
finished training model 2
saved model 2
"""