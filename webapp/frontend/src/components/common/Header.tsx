import { Bot, Save } from "lucide-react";
import type { Theme } from "../../types";
import { ThemeToggle } from "./ThemeToggle";

interface HeaderProps {
  theme: Theme;
  onToggleTheme: () => void;
  aiMode: boolean;
  onToggleAI: () => void;
}

export function Header({ theme, onToggleTheme, aiMode, onToggleAI }: HeaderProps) {
  return (
    <header className="h-16 border-b border-gray-200 bg-white px-4 dark:border-gray-700 dark:bg-gray-900">
      <div className="mx-auto flex h-full max-w-[1800px] items-center justify-between">
        <div>
          <h1 className="text-base font-semibold tracking-wide">DocMake</h1>
          <p className="text-xs text-gray-500 dark:text-gray-400">Markdown to PDF Builder</p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={onToggleAI}
            className={`inline-flex items-center gap-2 rounded border px-3 py-1.5 text-sm ${
              aiMode
                ? "border-gray-900 bg-gray-900 text-white dark:border-gray-100 dark:bg-gray-100 dark:text-gray-900"
                : "border-gray-300 bg-white text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-900 dark:text-gray-100 dark:hover:bg-gray-800"
            }`}
          >
            <Bot size={16} />
            AI Mode
          </button>

          <ThemeToggle theme={theme} onToggle={onToggleTheme} />

          <button className="inline-flex items-center gap-2 rounded border border-gray-300 bg-white px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-900 dark:text-gray-100 dark:hover:bg-gray-800">
            <Save size={16} />
            Save
          </button>
        </div>
      </div>
    </header>
  );
}
