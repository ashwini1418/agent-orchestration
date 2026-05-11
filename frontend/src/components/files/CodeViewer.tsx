// FRONTEND_AGENT | 2026-05-10 | Syntax-highlighted file content viewer
import { useState } from "react";
import { Highlight, themes, type Language } from "prism-react-renderer";
import { Button } from "@/components/common/Button";

const extToLang: Record<string, Language> = {
  ts: "typescript",
  tsx: "tsx",
  js: "javascript",
  jsx: "jsx",
  py: "python",
  json: "json",
  md: "markdown",
  yml: "yaml",
  yaml: "yaml",
  css: "css",
  html: "markup",
  sh: "bash",
};

interface Props {
  filePath: string;
  content: string;
  language?: string | null;
}

export function CodeViewer({ filePath, content, language }: Props) {
  const [copied, setCopied] = useState(false);
  const ext = filePath.split(".").pop() ?? "";
  const lang: Language = (language ? extToLang[language] : extToLang[ext]) ?? "plaintext";

  const handleCopy = async () => {
    await navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-4 py-2 bg-gray-800 rounded-t-lg">
        <span className="text-xs text-gray-300 font-mono">{filePath}</span>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => void handleCopy()}
          className="text-gray-300 hover:text-white"
          aria-label="Copy file content"
        >
          {copied ? "✓ Copied" : "Copy"}
        </Button>
      </div>
      <Highlight theme={themes.vsDark} code={content} language={lang}>
        {({ className, style, tokens, getLineProps, getTokenProps }) => (
          <pre
            className={`${className} overflow-auto text-xs p-4 rounded-b-lg flex-1 m-0`}
            style={style}
          >
            {tokens.map((line, i) => (
              <div key={i} {...getLineProps({ line })}>
                <span className="select-none text-gray-500 mr-4 text-right inline-block w-8">
                  {i + 1}
                </span>
                {line.map((token, key) => (
                  <span key={key} {...getTokenProps({ token })} />
                ))}
              </div>
            ))}
          </pre>
        )}
      </Highlight>
    </div>
  );
}
