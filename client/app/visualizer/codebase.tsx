"use client";
import { useEffect, useRef, useState } from "react";
import { ReactFlow, Background, Node, Edge } from "@xyflow/react";
import "@xyflow/react/dist/style.css";

export function CodebaseVisualizer() {
  const wsRef = useRef<WebSocket | null>(null);
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);

  useEffect(() => {
    if (!process.env.NEXT_PUBLIC_WEBSOCKET) return;

    try {
      const ws = new WebSocket(process.env.NEXT_PUBLIC_WEBSOCKET);
      wsRef.current = ws;

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setNodes(data.nodes);
        setEdges(data.edges);
      };

      return () => ws.close(); // cleanup on unmount
    } catch (e) {
      console.log(`WebSocket error: ${e}`);
    }
  }, []);

  const testSend = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(
        JSON.stringify({
          nodes: [
            {
              id: "n1",
              position: { x: 0, y: 0 },
              type: "fileNodes",
              data: { label: "Node 1" },
            },
            {
              id: "n2",
              position: { x: 100, y: 100 },
              data: { label: "Node 2" },
            },
          ],
          edges: [
            {
              id: "n1-n2",
              source: "n1",
              target: "n2",
              type: "step",
              label: "connects with",
            },
          ],
        }),
      );
    }
  };

  return (
    <div className="w-250 h-150 border border-black rounded-lg flex flex-col items-center gap-3.25">
      <ReactFlow nodes={nodes} edges={edges}>
        <Background />
      </ReactFlow>

      <div className="w-full h-16 border border-red-500">
        <p onClick={testSend}>Click me</p>
      </div>
    </div>
  );
}
