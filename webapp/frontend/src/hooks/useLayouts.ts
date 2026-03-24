import { useCallback, useEffect, useState } from "react";
import { layoutService } from "../services/api";
import type { LayoutDetail, LayoutSummary } from "../types";

const fallbackLayouts: LayoutSummary[] = [
  { id: "default", name: "Default", description: "Standard document layout" },
  { id: "academic", name: "Academic", description: "Formal academic style" },
  { id: "religious", name: "Religious", description: "Traditional structured style" },
];

export function useLayouts() {
  const [layouts, setLayouts] = useState<LayoutSummary[]>(fallbackLayouts);
  const [isLoading, setIsLoading] = useState(false);

  const refresh = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await layoutService.getAll();
      if (Array.isArray(data) && data.length > 0) {
        setLayouts(data);
      }
    } catch {
      setLayouts(fallbackLayouts);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const createLayout = useCallback(async () => {
    const base: Omit<LayoutDetail, "id"> = {
      name: `Custom ${layouts.length + 1}`,
      description: "User-created layout",
      config: {
        margins: { left: 12, right: 12, top: 16, bottom: 16 },
        colors: { body: "#1f2937", heading: "#111111", border: "#9ca3af" },
      },
    };

    try {
      await layoutService.create(base);
      await refresh();
    } catch {
      return;
    }
  }, [layouts.length, refresh]);

  return { layouts, isLoading, refresh, createLayout };
}
