import { Loader2, Send, Sparkles } from "lucide-react";
import { useState } from "react";
import { aiService } from "../../services/api";

interface AIPanelProps {
  content: string;
  onContentUpdate: (content: string) => void;
}

export function AIPanel({ content, onContentUpdate }: AIPanelProps) {
  const [prompt, setPrompt] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const quickActions = [
    { label: "Expand", prompt: "Expand this content with more details and examples." },
    { label: "Summarize", prompt: "Summarize this content concisely." },
    { label: "Format", prompt: "Improve markdown structure with clean headings." },
    { label: "Sections", prompt: "Add relevant sections and subsections." },
  ];

  const handleEnhance = async () => {
    if (!prompt.trim()) return;
    setIsProcessing(true);
    setError(null);

    try {
      const enhanced = await aiService.enhance(content, prompt);
      onContentUpdate(enhanced);
      setPrompt("");
    } catch {
      setError("AI request failed. Check backend and API key.");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="border-t border-gray-200 bg-gray-50 p-3 dark:border-gray-700 dark:bg-gray-800">
      <div className="mb-2 flex items-center gap-2 text-sm font-medium">
        <Sparkles size={16} />
        AI Enhancement
      </div>

      <div className="mb-3 flex flex-wrap gap-2">
        {quickActions.map((action) => (
          <button
            key={action.label}
            onClick={() => setPrompt(action.prompt)}
            className="rounded border border-gray-300 bg-white px-2 py-1 text-xs hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-900 dark:hover:bg-gray-800"
          >
            {action.label}
          </button>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") void handleEnhance();
          }}
          placeholder="Instruction for AI..."
          className="flex-1 rounded border border-gray-300 bg-white px-3 py-2 text-sm outline-none focus:border-gray-500 dark:border-gray-600 dark:bg-gray-900"
        />
        <button
          onClick={() => void handleEnhance()}
          disabled={!prompt.trim() || isProcessing}
          className="inline-flex items-center gap-1 rounded border border-gray-900 bg-gray-900 px-3 py-2 text-sm text-white disabled:opacity-50 dark:border-gray-200 dark:bg-gray-100 dark:text-gray-900"
        >
          {isProcessing ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
        </button>
      </div>

      {error && <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">{error}</p>}
    </div>
  );
}
