"use client";

import { useEffect, useRef, useState } from "react";
import { CodebaseVisualizer } from "./visualizer/codebase";

export default function Home() {
  const wsRef = useRef<WebSocket | null>(null);
  const [messages, setMessages] = useState<string[]>([]);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prev) => [...prev, data.message]);
    };

    return () => ws.close();
  }, []);

  const sendData = () => {
    console.log("readyState:", wsRef.current?.readyState);
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ message: "hello world" }));
    }
  };

  return (
    <div className="w-full min-h-screen flex flex-col justify-center items-center gap-2 bg-white">
      <p className="text-4xl font-bold">Hello world</p>
      <button onClick={sendData}>Send</button>

      {messages.map((msg, i) => (
        <p key={i}>{msg}</p>
      ))}

      <CodebaseVisualizer />
    </div>
  );
}
