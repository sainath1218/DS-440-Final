# DS440 Final — Tetris AI

A browser-based Tetris game with an AI that watches your board and plays moves for you using a pre-trained neural network. Click **AI Move** and the current piece animates step-by-step to the model's recommended placement.

---

## Repositories

| Repo | Role |
|------|------|
| `DS440-Tetris` (branch: `rowan_web_version`) | React/TypeScript frontend — game engine, rendering, A\* animation |
| `DS440-Data` | Python/FastAPI backend — model inference server |

---

## How It Works

```
Browser (React)
    │
    │  POST /predict  { placed, hold, queue, init_board }
    ▼
FastAPI server (Python)
    │
    ├─ Enumerates every legal placement for the current piece and the held piece
    ├─ Runs each candidate board through the pre-trained Keras model
    └─ Returns the best board state + the (x, y, rotation) of the winning placement
    │
    ▼
Browser runs A* from the piece's current position to (x, y, rotation)
and animates the piece moving there one step at a time
```

### Model

The backend loads `tetris_model_200k.keras` — a CNN trained on 200,000 Tetris game states. It takes the current board, the queue, the held piece, and a candidate resulting board as input, and outputs a score for that candidate. The candidate with the highest score is chosen.

---

## Changes Made This Session

### 1. Cloned the correct branch

The working branch of the frontend is `rowan_web_version`, not `main`. This branch contains the `applyPrediction` function and the "AI Move" button that the fixes below depend on.

### 2. Fixed J and L piece definitions (`DS440-Data/helpers.py`)

The rotation matrices for `"J"` and `"L"` were swapped in the backend relative to the frontend. The backend's `"J"` had the shape of a standard L-piece and vice versa.

**Effect of the bug:** when the player held a J-piece and clicked AI Move, the backend generated all valid placements using the *L-piece* shape. The returned board state had an L-shaped footprint where a J should have landed.

**Fix:** swapped the rotation matrices and colors for `"J"` and `"L"` in `PIECE_INFO` inside `helpers.py` so they match `gameinfo.ts` in the frontend.

| | `"J"` rotation 0 | `"L"` rotation 0 |
|---|---|---|
| **Before (wrong)** | `[[0,0,1],[1,1,1]]` — top-right jut | `[[1,0,0],[1,1,1]]` — top-left jut |
| **After (correct)** | `[[1,0,0],[1,1,1]]` — top-left jut | `[[0,0,1],[1,1,1]]` — top-right jut |

### 3. Verified board state consistency between frontend and backend

Traced the full round-trip of the board string through both sides to confirm every step is consistent:

- **Frontend serialization** (`applyPrediction` in `gameutils.ts`): uses `.map(...).join("").padStart(400, "N")` — top-first with 15 empty rows prepended to reach the backend's 40-row format.
- **Backend flip** (`server_rowan.py`): `np.flip(board_array, axis=0)` converts the top-first string to bottom-first, which is the format `mod_board_matrix_to_helper` expects before it reverses again to produce top-first for `getAllBoardStates`.
- **Response parsing** (`applyPrediction`): `pred_board_state.substring(150)` skips the 15 empty rows above the 25-row visible game, then reads the 25 rows directly into `board[0..24]`.
- **Model inputs** (`X_start`, `X_candidate`): both end up top-first after their respective flips — consistent with each other.

### 4. Implemented A\* pathfinding for animated AI moves (`DS440-Tetris/src/utils/astar.ts`)

Previously, clicking AI Move instantly snapped the board to the predicted state. The piece visually teleported.

**New behaviour:** the piece animates step-by-step from its current position to the predicted landing position before the board state is applied.

**State space:** `{ x, y, rotation }` — at most 10 × 25 × 4 = 1,000 states.

**Actions from each state:**
- Move left / right / down (validated against the live board)
- Rotate CW or CCW — uses the same SRS kick tables as the manual controls, so the AI path is always physically reachable

**Heuristic (admissible):**
```
h(state) = |x − goalX| + max(0, goalY − y) + minRotationDistance(r, goalR)
```

**Integration:**
- `server_rowan.py` now also returns `pred_x`, `pred_y`, `pred_r` alongside `pred_board_state`. The y coordinate is converted from the backend's 40-row space to the frontend's 25-row space (`frontend_y = backend_y − 15`).
- `applyPrediction` in `gameutils.ts` performs any hold-piece swap first (so the correct piece shape is used for pathfinding), then calls `astar(...)` and stores the resulting path.
- The canvas RAF loop in `TetrisCanvas.tsx` steps through the path at 60 ms per move, then calls `finishAIMove()` which applies the board state and advances the piece queue.
- Keyboard input is blocked and the button shows **"AI Moving…"** while the animation runs.
- If A\* finds no path (unreachable target), `finishAIMove()` is called immediately as a fallback.

### 5. Fixed double `getNextPiece()` call

The original `applyPrediction` called `getNextPiece()` twice when the hold slot was empty and the server chose to use the held piece, silently skipping a piece in the queue. The refactored version calls it exactly once per placement in all cases.

---

## Project Structure

```
DS440_Final/
├── DS440-Tetris/               # Frontend (branch: rowan_web_version)
│   └── src/
│       ├── components/
│       │   └── TetrisCanvas.tsx      # Game canvas + animation loop
│       └── utils/
│           ├── astar.ts              # A* pathfinding (new)
│           ├── gameutils.ts          # Game state, applyPrediction, finishAIMove
│           ├── gameinfo.ts           # Piece shapes, kick tables, constants
│           └── drawing.ts            # Canvas rendering
└── DS440-Data/                 # Backend
    ├── server_rowan.py               # FastAPI server — /predict endpoint
    ├── helpers.py                    # Board utils, piece definitions, candidate generation
    ├── model.py                      # Keras model architecture
    └── tetris_model_200k.keras       # Pre-trained weights (200k training samples)
```

---

## Running Locally

**Requirements:** Python 3.10+, Node 18+

### Backend

```bash
cd DS440-Data
pip install numpy pandas fastapi uvicorn tensorflow
python server_rowan.py
# → http://localhost:8001
```

### Frontend

```bash
cd DS440-Tetris
npm install
npm run dev
# → http://localhost:5173
```

Open `http://localhost:5173` in your browser.

---

## Controls

| Key | Action |
|-----|--------|
| ← → | Move left / right |
| ↓ | Soft drop |
| ↑ | Hard drop |
| X | Rotate clockwise |
| Z | Rotate counter-clockwise |
| Space | Hold piece |
| **AI Move button** | Let the model play the current piece |
