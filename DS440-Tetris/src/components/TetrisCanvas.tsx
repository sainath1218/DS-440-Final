import { useEffect, useRef, useState } from "react";
import { ROWS, COLS, CELL_SIZE_PX } from "../utils/gameinfo";
import {
  board, currPiece, currPos, currRotation, holdPiece, pieceQueue, prediction,
  initGame, tryMove, tryRotation, hardDropPiece, swapHoldPiece,
  applyPrediction, stepAnimation, finishAIMove, animPath, animStep,
} from "../utils/gameutils";
import { drawGame, drawPosDot } from "../utils/drawing";

const ANIM_MS = 60; // ms per animation step

export default function TetrisCanvas() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const rafIdRef = useRef<number | null>(null);
  const lastAnimTimeRef = useRef<number>(0);
  const [, setTick] = useState(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    canvas.width = COLS * CELL_SIZE_PX;
    canvas.height = ROWS * CELL_SIZE_PX;
    const ctx = canvas.getContext("2d");

    const drawCanvasLoop = (timestamp: number) => {
      if (!ctx) return;

      // Advance A* animation one step per ANIM_MS interval
      if (animPath.length > 0) {
        if (timestamp - lastAnimTimeRef.current >= ANIM_MS) {
          if (animStep < animPath.length) {
            stepAnimation();
          } else {
            finishAIMove();
          }
          lastAnimTimeRef.current = timestamp;
        }
      }

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      drawGame(ctx);
      if (prediction) drawPosDot(ctx, prediction.x, prediction.y);
      setTick(t => t + 1);

      rafIdRef.current = requestAnimationFrame(drawCanvasLoop);
    };

    rafIdRef.current = requestAnimationFrame(drawCanvasLoop);

    const keyListener = (e: KeyboardEvent) => {
      // Block all input while AI animation is running
      if (animPath.length > 0) return;

      if (e.key === "ArrowDown") tryMove(0, 1);

      if (!e.repeat) {
        if (e.key === "ArrowUp")    hardDropPiece();
        if (e.key === "ArrowLeft")  tryMove(-1, 0);
        if (e.key === "ArrowRight") tryMove(1, 0);
        if (e.key === "x")          tryRotation(1);
        if (e.key === "z")          tryRotation(-1);
        if (e.key === " ")          swapHoldPiece();
        if (e.key === "l") console.log(`piece: ${currPiece}, pos: ${JSON.stringify(currPos)}, rotation: ${currRotation}`);
        if (e.key === "b") console.log(`Board: ${JSON.stringify(board)}`);
      }
    };

    addEventListener("keydown", keyListener);
    initGame();

    return () => {
      if (rafIdRef.current != null) cancelAnimationFrame(rafIdRef.current);
      removeEventListener("keydown", keyListener);
    };
  }, []);

  const isAnimating = animPath.length > 0;

  return (
    <div className="outline-[1px] outline-[#999]" style={{ position: "relative" }}>
      <canvas ref={canvasRef} />
      <pre style={{ fontSize: 11, lineHeight: 1.3, position: "fixed", top: 0, left: 0, whiteSpace: "pre-wrap", width: 360 }}>
        {`piece: ${currPiece}  hold: ${holdPiece}  queue: ${pieceQueue.slice(0, 5).join("")}\n`}
        {`prediction: x=${prediction?.x ?? "?"} y=${prediction?.y ?? "?"} r=${prediction?.r ?? "?"}\n`}
        {([...board].reverse().map(row => row.map(c => c ?? "N").join("")).join("").padEnd(400, "N"))}
      </pre>
      <button
        onClick={() => applyPrediction()}
        disabled={isAnimating}
        style={{ position: "fixed", top: 10, right: 10, opacity: isAnimating ? 0.4 : 1 }}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        {isAnimating ? "AI Moving…" : "AI Move"}
      </button>
    </div>
  );
}
