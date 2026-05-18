"use client";
import { useEffect } from "react";
import { ReactFlow, Background } from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { initialNodes, initialEdges } from "./data";

export function CodebaseVisualizer() {
  return (
    <div className="w-250 h-150 border border-black rounded-lg">
      <ReactFlow
        nodes={initialNodes}
        edges={initialEdges}
        className="w-full h-full"
      >
        <Background />
      </ReactFlow>
    </div>
  );
}
