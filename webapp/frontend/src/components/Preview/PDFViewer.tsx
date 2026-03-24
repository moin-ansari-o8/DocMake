import { useEffect, useRef, useState } from "react";
import * as pdfjsLib from "pdfjs-dist";
import { ChevronLeft, ChevronRight, Download, Loader2, ZoomIn, ZoomOut } from "lucide-react";

pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  "pdfjs-dist/build/pdf.worker.min.mjs",
  import.meta.url
).toString();

interface PDFViewerProps {
  pdfUrl: string | null;
  isGenerating: boolean;
  error: string | null;
  onGenerate: () => void;
}

export function PDFViewer({ pdfUrl, isGenerating, error, onGenerate }: PDFViewerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [pdf, setPdf] = useState<pdfjsLib.PDFDocumentProxy | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [scale, setScale] = useState(1.1);

  useEffect(() => {
    if (!pdfUrl) {
      setPdf(null);
      setCurrentPage(1);
      setTotalPages(0);
      return;
    }

    let mounted = true;
    const load = async () => {
      const task = pdfjsLib.getDocument(pdfUrl);
      const doc = await task.promise;
      if (mounted) {
        setPdf(doc);
        setTotalPages(doc.numPages);
        setCurrentPage(1);
      }
    };

    void load();
    return () => {
      mounted = false;
    };
  }, [pdfUrl]);

  useEffect(() => {
    if (!pdf || !canvasRef.current) return;

    const render = async () => {
      const page = await pdf.getPage(currentPage);
      const viewport = page.getViewport({ scale });
      const canvas = canvasRef.current;
      if (!canvas) return;
      const context = canvas.getContext("2d");
      if (!context) return;

      canvas.width = viewport.width;
      canvas.height = viewport.height;

      await page.render({ canvasContext: context, viewport }).promise;
    };

    void render();
  }, [pdf, currentPage, scale]);

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-gray-200 bg-white p-3 dark:border-gray-700 dark:bg-gray-900">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={currentPage <= 1}
            className="rounded border border-gray-300 p-1.5 disabled:opacity-40 dark:border-gray-600"
          >
            <ChevronLeft size={16} />
          </button>
          <span className="text-sm">{totalPages ? `${currentPage}/${totalPages}` : "0/0"}</span>
          <button
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            disabled={currentPage >= totalPages}
            className="rounded border border-gray-300 p-1.5 disabled:opacity-40 dark:border-gray-600"
          >
            <ChevronRight size={16} />
          </button>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setScale((s) => Math.max(0.5, s - 0.1))}
            className="rounded border border-gray-300 p-1.5 dark:border-gray-600"
          >
            <ZoomOut size={16} />
          </button>
          <span className="w-14 text-center text-sm">{Math.round(scale * 100)}%</span>
          <button
            onClick={() => setScale((s) => Math.min(2.5, s + 0.1))}
            className="rounded border border-gray-300 p-1.5 dark:border-gray-600"
          >
            <ZoomIn size={16} />
          </button>
        </div>

        <div>
          {pdfUrl ? (
            <a
              href={pdfUrl}
              download="document.pdf"
              className="inline-flex items-center gap-1 rounded border border-gray-900 bg-gray-900 px-3 py-1.5 text-sm text-white dark:border-gray-200 dark:bg-gray-100 dark:text-gray-900"
            >
              <Download size={16} />
              Download
            </a>
          ) : (
            <button
              onClick={onGenerate}
              className="rounded border border-gray-900 bg-gray-900 px-3 py-1.5 text-sm text-white dark:border-gray-200 dark:bg-gray-100 dark:text-gray-900"
            >
              Generate PDF
            </button>
          )}
        </div>
      </div>

      <div className="flex-1 overflow-auto bg-gray-100 p-4 dark:bg-gray-800">
        {isGenerating ? (
          <div className="flex h-full items-center justify-center text-sm text-gray-600 dark:text-gray-300">
            <Loader2 className="mr-2 h-5 w-5 animate-spin" /> Generating PDF...
          </div>
        ) : error ? (
          <div className="flex h-full items-center justify-center text-sm text-gray-500 dark:text-gray-400">
            {error}
          </div>
        ) : pdfUrl ? (
          <div className="flex justify-center">
            <canvas ref={canvasRef} className="border border-gray-300 bg-white shadow-sm dark:border-gray-600" />
          </div>
        ) : (
          <div className="flex h-full items-center justify-center text-sm text-gray-500 dark:text-gray-400">
            No preview available yet.
          </div>
        )}
      </div>
    </div>
  );
}
