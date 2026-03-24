import { useCallback, useEffect, useState } from "react";
import { layoutService } from "../services/api";
import type { LayoutSummary } from "../types";

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
    try {
      const source = layouts.find((l) => l.id === "default")?.id ?? "default";
      await layoutService.clone(source, `Custom ${layouts.length + 1}`);
      await refresh();
    } catch {
      return;
    }
  }, [layouts, refresh]);

  return { layouts, isLoading, refresh, createLayout };
}
