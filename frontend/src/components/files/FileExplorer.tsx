// FRONTEND_AGENT | 2026-05-10 | Tree view of generated project files
import { useState } from "react";
import type { FileTreeNode } from "@/types/files";

const fileIcon = (name: string) => {
  if (name.endsWith(".tsx") || name.endsWith(".ts")) return "📘";
  if (name.endsWith(".py")) return "🐍";
  if (name.endsWith(".json")) return "📋";
  if (name.endsWith(".md")) return "📝";
  if (name.endsWith(".yml") || name.endsWith(".yaml")) return "⚙️";
  if (name.startsWith("Dockerfile")) return "🐳";
  return "📄";
};

interface TreeNodeProps {
  node: FileTreeNode;
  depth: number;
  onSelectFile: (node: FileTreeNode) => void;
}

function TreeNode({ node, depth, onSelectFile }: TreeNodeProps) {
  const [open, setOpen] = useState(depth < 2);

  if (node.type === "directory") {
    return (
      <li>
        <button
          onClick={() => setOpen(!open)}
          className="flex items-center gap-1 w-full text-left py-0.5 text-sm text-gray-700 hover:text-gray-900"
          style={{ paddingLeft: `${depth * 12}px` }}
          aria-expanded={open}
        >
          <span aria-hidden="true">{open ? "📂" : "📁"}</span>
          <span className="font-medium">{node.name}</span>
        </button>
        {open && node.children && (
          <ul>
            {node.children.map((child) => (
              <TreeNode key={child.path} node={child} depth={depth + 1} onSelectFile={onSelectFile} />
            ))}
          </ul>
        )}
      </li>
    );
  }

  return (
    <li>
      <button
        onClick={() => onSelectFile(node)}
        className="flex items-center gap-1 w-full text-left py-0.5 text-sm text-gray-600 hover:text-blue-600"
        style={{ paddingLeft: `${depth * 12}px` }}
      >
        <span aria-hidden="true">{fileIcon(node.name)}</span>
        {node.name}
      </button>
    </li>
  );
}

interface Props {
  tree: FileTreeNode[];
  onSelectFile: (node: FileTreeNode) => void;
}

export function FileExplorer({ tree, onSelectFile }: Props) {
  if (tree.length === 0) {
    return <p className="text-xs text-gray-400 text-center py-4">No files generated yet</p>;
  }

  return (
    <nav aria-label="Generated files">
      <ul className="space-y-0.5">
        {tree.map((node) => (
          <TreeNode key={node.path} node={node} depth={0} onSelectFile={onSelectFile} />
        ))}
      </ul>
    </nav>
  );
}
