import { PIECE_INFO, COLS, ROWS, KICK_TABLE } from "./gameinfo";
import type { PIECE, CELL } from "./types";

export interface AStarState {
  x: number;
  y: number;
  r: number;
}

interface Node {
  state: AStarState;
  g: number;
  f: number;
  parent: Node | null;
}

function validAt(board: CELL[][], piece: PIECE, x: number, y: number, r: number): boolean {
  const rMatrix = PIECE_INFO[piece].rotations[r];
  for (let dy = 0; dy < rMatrix.length; dy++) {
    for (let dx = 0; dx < rMatrix[dy].length; dx++) {
      if (rMatrix[dy][dx] === 1) {
        const nx = x + dx;
        const ny = y + dy;
        if (nx < 0 || nx >= COLS || ny < 0 || ny >= ROWS || board[ny][nx] !== null) {
          return false;
        }
      }
    }
  }
  return true;
}

function minRotDist(r: number, gr: number): number {
  const diff = Math.abs(r - gr);
  return Math.min(diff, 4 - diff);
}

function h(s: AStarState, goal: AStarState): number {
  return Math.abs(s.x - goal.x) + Math.max(0, goal.y - s.y) + minRotDist(s.r, goal.r);
}

function stateKey(s: AStarState): string {
  return `${s.x},${s.y},${s.r}`;
}

function getNeighbors(board: CELL[][], piece: PIECE, s: AStarState): AStarState[] {
  const { x, y, r } = s;
  const result: AStarState[] = [];

  if (validAt(board, piece, x - 1, y, r)) result.push({ x: x - 1, y, r });
  if (validAt(board, piece, x + 1, y, r)) result.push({ x: x + 1, y, r });
  if (validAt(board, piece, x, y + 1, r)) result.push({ x, y: y + 1, r });

  // CW (+1) and CCW (+3 mod 4) rotations with kick tables
  for (const delta of [1, 3]) {
    const nr = (r + delta) % 4;
    const kicks = KICK_TABLE[PIECE_INFO[piece].kick_index][r][nr];
    for (const [kx, ky] of kicks) {
      // ky is positive=up in the kick table, so subtract from y
      if (validAt(board, piece, x + kx, y - ky, nr)) {
        result.push({ x: x + kx, y: y - ky, r: nr });
        break;
      }
    }
  }

  return result;
}

export function astar(
  piece: PIECE,
  board: CELL[][],
  sx: number, sy: number, sr: number,
  gx: number, gy: number, gr: number
): AStarState[] {
  if (sx === gx && sy === gy && sr === gr) return [];

  const goal: AStarState = { x: gx, y: gy, r: gr };
  const start: AStarState = { x: sx, y: sy, r: sr };

  const open: Node[] = [{ state: start, g: 0, f: h(start, goal), parent: null }];
  const closed = new Set<string>();
  const gBest = new Map<string, number>();
  gBest.set(stateKey(start), 0);

  while (open.length > 0) {
    // Pop lowest-f node
    let minIdx = 0;
    for (let i = 1; i < open.length; i++) {
      if (open[i].f < open[minIdx].f) minIdx = i;
    }
    const cur = open.splice(minIdx, 1)[0];
    const ck = stateKey(cur.state);

    if (closed.has(ck)) continue;
    closed.add(ck);

    if (cur.state.x === gx && cur.state.y === gy && cur.state.r === gr) {
      const path: AStarState[] = [];
      let node: Node | null = cur;
      while (node !== null && node.parent !== null) {
        path.unshift(node.state);
        node = node.parent;
      }
      return path;
    }

    for (const nb of getNeighbors(board, piece, cur.state)) {
      const nk = stateKey(nb);
      if (closed.has(nk)) continue;
      const ng = cur.g + 1;
      if (ng < (gBest.get(nk) ?? Infinity)) {
        gBest.set(nk, ng);
        open.push({ state: nb, g: ng, f: ng + h(nb, goal), parent: cur });
      }
    }
  }

  return [];
}
