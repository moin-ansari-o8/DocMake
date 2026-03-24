import { ChevronDown, Plus, Settings } from "lucide-react";
import { useState } from "react";
import { useLayouts } from "../../hooks/useLayouts";

interface LayoutSelectorProps {
  currentLayout: string;
  onLayoutChange: (layoutId: string) => void;
}

export function LayoutSelector({ currentLayout, onLayoutChange }: LayoutSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const { layouts, createLayout, isLoading } = useLayouts();

  return (
    <div className="flex items-center gap-2 border-b border-gray-200 bg-gray-50 p-3 dark:border-gray-700 dark:bg-gray-800">
      <div className="relative">
        <button
          onClick={() => setIsOpen((v) => !v)}
          className="inline-flex items-center gap-2 rounded border border-gray-300 bg-white px-3 py-1.5 text-sm hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-900 dark:hover:bg-gray-800"
        >
          Layout: {layouts.find((l) => l.id === currentLayout)?.name ?? "Default"}
          <ChevronDown size={16} />
        </button>

        {isOpen && (
          <div className="absolute left-0 top-full z-10 mt-1 w-60 rounded border border-gray-300 bg-white p-1 shadow-sm dark:border-gray-600 dark:bg-gray-900">
            {layouts.map((layout) => (
              <button
                key={layout.id}
                onClick={() => {
                  onLayoutChange(layout.id);
                  setIsOpen(false);
                }}
                className={`block w-full rounded px-2 py-2 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-800 ${
                  currentLayout === layout.id ? "bg-gray-200 dark:bg-gray-700" : ""
                }`}
              >
                <div className="font-medium">{layout.name}</div>
                {layout.description && (
                  <div className="text-xs text-gray-500 dark:text-gray-400">{layout.description}</div>
                )}
              </button>
            ))}
          </div>
        )}
      </div>

      <button
        onClick={() => void createLayout()}
        disabled={isLoading}
        className="inline-flex items-center gap-1 rounded border border-gray-300 bg-white px-2.5 py-1.5 text-sm hover:bg-gray-50 disabled:opacity-60 dark:border-gray-600 dark:bg-gray-900 dark:hover:bg-gray-800"
      >
        <Plus size={16} />
        New
      </button>

      <button className="rounded border border-gray-300 bg-white p-1.5 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-900 dark:hover:bg-gray-800">
        <Settings size={16} />
      </button>
    </div>
  );
}
