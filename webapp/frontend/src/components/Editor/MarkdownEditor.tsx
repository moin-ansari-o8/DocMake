import Editor from "@monaco-editor/react";
import type { Theme } from "../../types";

interface MarkdownEditorProps {
  value: string;
  onChange: (value: string) => void;
  theme: Theme;
}

export function MarkdownEditor({
  value,
  onChange,
  theme,
}: MarkdownEditorProps) {
  return (
    <Editor
      height="100%"
      language="markdown"
      theme={theme === "dark" ? "vs-dark" : "light"}
      value={value}
      onChange={(val) => onChange(val ?? "")}
      options={{
        minimap: { enabled: false },
        wordWrap: "on",
        fontSize: 14,
        lineHeight: 22,
        scrollBeyondLastLine: false,
        automaticLayout: true,
        padding: { top: 12, bottom: 12 },
        quickSuggestions: true,
        quickSuggestionsDelay: 0,
        suggestOnTriggerCharacters: true,
        acceptSuggestionOnEnter: "smart",
        tabCompletion: "on",
        snippetSuggestions: "inline",
        parameterHints: { enabled: false },
      }}
    />
  );
}
