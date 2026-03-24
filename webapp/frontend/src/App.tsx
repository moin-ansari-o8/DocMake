import { useEffect, useState } from "react";
import { AIPanel } from "./components/AI/AIPanel";
import { MarkdownEditor } from "./components/Editor/MarkdownEditor";
import { LayoutSelector } from "./components/Layout/LayoutSelector";
import { PDFViewer } from "./components/Preview/PDFViewer";
import { Header } from "./components/common/Header";
import { useDebounce } from "./hooks/useDebounce";
import { usePDFGenerator } from "./hooks/usePDFGenerator";
import { useTheme } from "./hooks/useTheme";

const INITIAL_CONTENT = `# Document Title
> Brief subtitle

## Introduction
Write your content here.

## Main Section
Add more details with clean markdown.
`;

export default function App() {
  const { theme, toggleTheme } = useTheme();
  const [content, setContent] = useState(INITIAL_CONTENT);
  const [currentLayout, setCurrentLayout] = useState("default");
  const [aiMode, setAiMode] = useState(false);

  const debouncedContent = useDebounce(content, 900);
  const { pdfUrl, isGenerating, error, generatePDF } = usePDFGenerator();

  useEffect(() => {
    if (!debouncedContent.trim()) return;
    void generatePDF(debouncedContent, currentLayout);
  }, [debouncedContent, currentLayout, generatePDF]);

  return (
    <div className={theme === "dark" ? "dark" : ""}>
      <div className="min-h-screen bg-white text-gray-900 dark:bg-gray-900 dark:text-gray-100">
        <Header
          theme={theme}
          onToggleTheme={toggleTheme}
          aiMode={aiMode}
          onToggleAI={() => setAiMode((v) => !v)}
        />

        <main className="mx-auto flex h-[calc(100vh-64px)] max-w-[1800px]">
          <section className="flex w-1/2 flex-col border-r border-gray-200 dark:border-gray-700">
            <LayoutSelector currentLayout={currentLayout} onLayoutChange={setCurrentLayout} />
            <div className="flex-1 overflow-hidden">
              <MarkdownEditor value={content} onChange={setContent} theme={theme} />
            </div>
            {aiMode && <AIPanel content={content} onContentUpdate={setContent} />}
          </section>

          <section className="w-1/2 bg-gray-50 dark:bg-gray-800">
            <PDFViewer
              pdfUrl={pdfUrl}
              isGenerating={isGenerating}
              error={error}
              onGenerate={() => void generatePDF(content, currentLayout)}
            />
          </section>
        </main>
      </div>
    </div>
  );
}
