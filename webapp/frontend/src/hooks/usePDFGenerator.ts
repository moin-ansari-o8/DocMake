import { useCallback, useEffect, useRef, useState } from "react";
import { pdfService } from "../services/api";

export function usePDFGenerator() {
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const activeUrl = useRef<string | null>(null);

  const generatePDF = useCallback(async (content: string, layoutId: string) => {
    setIsGenerating(true);
    setError(null);

    try {
      const blob = await pdfService.generate(content, layoutId);
      const nextUrl = URL.createObjectURL(blob);

      if (activeUrl.current) {
        URL.revokeObjectURL(activeUrl.current);
      }

      activeUrl.current = nextUrl;
      setPdfUrl(nextUrl);
    } catch {
      setError("Failed to generate PDF. Please check the backend server.");
    } finally {
      setIsGenerating(false);
    }
  }, []);

  useEffect(() => {
    return () => {
      if (activeUrl.current) {
        URL.revokeObjectURL(activeUrl.current);
      }
    };
  }, []);

  return { pdfUrl, isGenerating, error, generatePDF };
}
