import numpy as np
# import tensorflow as tf
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Conv2D, Flatten, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from helpers import *



app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
model = load_model("tetris_model_200k.keras")
inv_vocab = {0:"N", 1:"G", 2:"I", 3:"O", 4:"T", 5:"S", 6:"Z", 7:"J", 8:"L"}
vocab = {"N":0,"G":1,"I":2,"O":3,"T":4,"S":5,"Z":6,"J":7,"L":8}

class PredictRequest(BaseModel):
    placed: str
    hold: str
    queue: str
    init_board: str


def get_candidates(playfield_array, piece):
    if piece == 0:
        return []
    
    boards1 = get_board_arrays(
        getAllBoardStates(playfield_array, piece, True),
        mod_board_matrix_to_helper(playfield_array),
        inv_vocab[piece]
    )
    
    return boards1 

def get_board_arrays(states, init_board_matrix, init_piece):
    seen = {}
    for px, py, r in states:
        arr = getBoardArray(init_board_matrix, init_piece, px, py, r)
        key = tuple(arr)
        if key not in seen:
            seen[key] = (arr, px, py, r)
    return list(seen.values())

def board_to_flat_string(board):
    grid = mod_board_matrix_to_helper(board)  # list of lists
    return "".join("".join(row) for row in grid)

@app.post("/predict")
def predict(req: PredictRequest):

    print('Received request:')
    print(req.placed, req.hold, req.queue, req.init_board)



    board_array = np.array([vocab[c] for c in req.init_board]).reshape(40, 10)
    print('board_array', board_array)
    board_int = np.flip(board_array, axis=0).flatten().tolist()  
    queue_int = [vocab[c] for c in req.queue]
    to_place_int = vocab[req.placed]
    if req.hold == "N":
        hold_int = queue_int[0]
    else:
        hold_int = vocab[req.hold]

    print('board_int', board_int)
    print('to_place_int', to_place_int)
    print('hold_int', hold_int)
    print('queue_int', queue_int)

    candidates_place = get_candidates(np.array(board_int), to_place_int)
    candidates_hold = get_candidates(np.array(board_int), hold_int)
    all_candidates_with_pos = candidates_place + candidates_hold
    n = len(all_candidates_with_pos)
    labels = [req.placed] * len(candidates_place) + [req.hold] * len(candidates_hold)
    while len(queue_int) < 14:
        queue_int.append(0)  # pad to length 14

    all_candidates = [item[0] for item in all_candidates_with_pos]
    all_positions  = [(item[1], item[2], item[3]) for item in all_candidates_with_pos]

    X_queue     = np.array([queue_int] * n)
    X_hold      = np.array([[hold_int]] * n)
    X_place     = np.array([[to_place_int]] * n)
    X_start     = np.flip(np.array([board_int] * n).reshape(n, 40, 10), axis=1)
    X_candidate = np.flip(np.array(all_candidates).reshape(n, 40, 10), axis=1)

    print('X_queue shape', X_queue.shape)
    print('X_hold shape', X_hold.shape)
    print('X_place shape', X_place.shape)
    print('X_start shape', X_start.shape)
    print('X_candidate shape', X_candidate.shape)
    pred = model.predict(
        [X_queue, X_hold, X_place, X_start, X_candidate],
        batch_size=32,
        verbose=1
    ).flatten()

    best_idx       = np.argmax(pred)
    best_candidate = all_candidates[best_idx]
    best_label     = labels[best_idx]
    best_x, best_y, best_r = all_positions[best_idx]

    best_candidate_str = board_to_flat_string(best_candidate)
    print('best_candidate_str', best_candidate_str)
    print('best_label', best_label)
    print('best_x', best_x, 'best_y', best_y, 'best_r', best_r)

    # Convert backend y (0-indexed in 40-row world) to frontend y (0-indexed in 25-row board).
    # The frontend pads 15 empty rows above the 25-row game, so row 15 in backend = row 0 in frontend.
    frontend_y = int(best_y) - 15

    return {
        "pred_board_state": best_candidate_str,
        "used": best_label,
        "pred_x": int(best_x),
        "pred_y": frontend_y,
        "pred_r": int(best_r),
    }


if __name__ == "__main__":
    uvicorn.run("server_rowan:app", host="0.0.0.0", port=8001, reload=True)