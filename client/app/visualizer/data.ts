interface FileNode {
  id: string;
  position: { x: number; y: number };
  data: { label: string };
}

const initialNodes = [
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
];

const initialEdges = [
  {
    id: "n1-n2",
    source: "n1",
    target: "n2",
    type: "step",
    label: "connects with",
  },
];

export { initialEdges, initialNodes, type FileNode };
