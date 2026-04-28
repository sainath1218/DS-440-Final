import { type PIECE, type CELL } from "./types";
import { PIECE_INFO, ROWS, COLS, KICK_TABLE } from "./gameinfo";
import { astar } from "./astar";
import type { AStarState } from "./astar";

export let board: CELL[][] = [];
export let currPiece: PIECE | null = null;
export let pieceQueue: PIECE[] = [];
export let currPos = [3, 0];
export let currRotation = 0;
export let holdPiece: PIECE | null = null;
export let prediction: { x: number; y: number; r: string } | null = null;
let swapped: boolean = false;

// A* animation state
export let animPath: AStarState[] = [];
export let animStep = 0;
let pendingBoardState = "";

export async function applyPrediction() {
  if (!currPiece || animPath.length > 0) return;

  const boardStr = [...board].map(row => row.map(c => c ?? "N").join("")).join("").padStart(400, "N");
  const body = {
    placed: currPiece,
    hold: holdPiece ?? "N",
    queue: pieceQueue.join(""),
    init_board: boardStr,
  };

  try {
    const res = await fetch("http://localhost:8001/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();

    pendingBoardState = data.pred_board_state;
    const targetX: number = data.pred_x;
    const targetY: number = data.pred_y; // already in frontend coords (server subtracts 15)
    const targetR: number = data.pred_r;

    // Perform hold swap before A* so currPiece reflects the piece being placed
    if (data.used !== currPiece) {
      if (holdPiece !== null) {
        [currPiece, holdPiece] = [holdPiece, currPiece];
        currPos = [currPiece === "O" ? 4 : 3, 0];
        currRotation = 0;
      } else {
        holdPiece = currPiece;
        getNextPiece(); // advances currPiece to the queue piece being played
      }
    }

    const path = astar(currPiece!, board, currPos[0], currPos[1], currRotation, targetX, targetY, targetR);

    if (path.length === 0) {
      // Already at target or unreachable — apply board immediately
      finishAIMove();
      return;
    }

    animPath = path;
    animStep = 0;
  } catch (e) {
    console.error("applyPrediction failed", e);
  }
}

export function stepAnimation() {
  if (animStep >= animPath.length) return;
  const s = animPath[animStep];
  currPos[0] = s.x;
  currPos[1] = s.y;
  currRotation = s.r;
  animStep++;
}

export function finishAIMove() {
  const trimmed = pendingBoardState.substring(150);
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const char = trimmed[r * COLS + c];
      board[r][c] = (char === "N" || char === undefined) ? null : (char as CELL);
    }
  }
  getNextPiece();
  swapped = false;
  animPath = [];
  animStep = 0;
}

resetBoard();

function resetBoard() {
  board = [];
  for (let r = 0; r < ROWS; r++) {
    const row: CELL[] = [];
    for (let c = 0; c < COLS; c++) row.push(null);
    board.push(row);
  }
}

export function initGame() {
  resetBoard();
  initPieceQueue();
  getNextPiece();
}

function getNextPiece() {
  const nextPiece = pieceQueue.shift();
  if (nextPiece == "O") currPos = [4, 0];
  else currPos = [3, 0];
  currRotation = 0;
  if (nextPiece != undefined) currPiece = nextPiece;
  if (pieceQueue.length <= 7) pieceQueue.push(...getSevenBag());
}

function initPieceQueue() {
  pieceQueue = [];
  pieceQueue.push(...getSevenBag());
  pieceQueue.push(...getSevenBag());
}

function getSevenBag() {
  const pieceMap: PIECE[] = ["I", "O", "T", "S", "Z", "J", "L"];
  const arr = [0, 1, 2, 3, 4, 5, 6];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr.map(val => pieceMap[val]);
}

export function swapHoldPiece() {
  if (swapped) return;
  if (holdPiece != null) {
    [currPiece, holdPiece] = [holdPiece, currPiece];
    if (currPiece == "O") currPos = [4, 0];
    else currPos = [3, 0];
    currRotation = 0;
  } else {
    holdPiece = currPiece;
    getNextPiece();
  }
  swapped = true;
}

export function hardDropPiece() {
  while (tryMove(0, 1));
  lockPiece();
}

function lockPiece() {
  if (currPiece == null) return;
  const px = currPos[0];
  const py = currPos[1];
  const rotation = PIECE_INFO[currPiece].rotations[currRotation];
  for (let dy = 0; dy < rotation.length; dy++) {
    for (let dx = 0; dx < rotation[dy].length; dx++) {
      if (rotation[dy][dx] == 1) board[py + dy][px + dx] = currPiece;
    }
  }
  clearLines();
  getNextPiece();
  swapped = false;
}

export function tryMove(dx: number, dy: number) {
  if (currPiece == null) return;
  const newX = currPos[0] + dx;
  const newY = currPos[1] + dy;
  const rMatrix = PIECE_INFO[currPiece].rotations[currRotation];
  for (let dy = 0; dy < rMatrix.length; dy++) {
    for (let dx = 0; dx < rMatrix[dy].length; dx++) {
      const x = newX + dx;
      const y = newY + dy;
      if (rMatrix[dy][dx] == 1 && (x < 0 || x >= COLS || y < 0 || y >= ROWS || board[y][x] != null)) {
        return false;
      }
    }
  }
  currPos = [newX, newY];
  return true;
}

export function tryRotation(dir: number) {
  if (currPiece == null) return;
  let newRotation = currRotation + dir;
  while (newRotation < 0) newRotation += 4;
  while (newRotation > 3) newRotation -= 4;
  const px = currPos[0];
  const py = currPos[1];
  const rMatrix = PIECE_INFO[currPiece].rotations[newRotation];
  const kicks = KICK_TABLE[PIECE_INFO[currPiece].kick_index][currRotation][newRotation];
  for (let i = 0; i < kicks.length; i++) {
    const [kx, ky] = kicks[i];
    if (isValidPosRot(px + kx, py - ky, rMatrix)) {
      currRotation = newRotation;
      currPos = [px + kx, py - ky];
      return true;
    }
  }
  return false;
}

function isValidPosRot(px: number, py: number, rMatrix: number[][]) {
  for (let dy = 0; dy < rMatrix.length; dy++) {
    for (let dx = 0; dx < rMatrix[dy].length; dx++) {
      const x = px + dx;
      const y = py + dy;
      if (rMatrix[dy][dx] == 1 && (x < 0 || x >= COLS || y < 0 || y >= ROWS || board[y][x] != null)) {
        return false;
      }
    }
  }
  return true;
}

function clearLines() {
  for (let row = 0; row < ROWS; row++) {
    if (isRowFull(row)) moveLinesDown(row);
  }
}

function moveLinesDown(row: number) {
  while (row > 0) {
    for (let c = 0; c < COLS; c++) board[row][c] = board[row - 1][c];
    row--;
  }
  for (let c = 0; c < COLS; c++) board[row][c] = null;
}

function isRowFull(row: number): boolean {
  for (let c = 0; c < COLS; c++) {
    if (board[row][c] == null) return false;
  }
  return true;
}

export function getGhostPieceLocation() {
  let currY = currPos[1];
  while (validYPos(currY + 1)) currY++;
  return [currPos[0], currY];
}

function validYPos(py: number) {
  if (!currPiece) return;
  const px = currPos[0];
  const rMatrix = PIECE_INFO[currPiece].rotations[currRotation];
  for (let dy = 0; dy < rMatrix.length; dy++) {
    for (let dx = 0; dx < rMatrix[dy].length; dx++) {
      const x = px + dx;
      const y = py + dy;
      if (rMatrix[dy][dx] == 1 && (x < 0 || x >= COLS || y < 0 || y >= ROWS || board[y][x] != null)) return false;
    }
  }
  return true;
}
