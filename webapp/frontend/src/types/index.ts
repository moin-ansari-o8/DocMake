export type Theme = "light" | "dark";

export interface LayoutSummary {
  id: string;
  name: string;
  description?: string;
}

export interface LayoutConfig {
  margins?: { left: number; right: number; top: number; bottom: number };
  fonts?: {
    body?: { name: string; size: number };
    heading?: { name: string; size: number };
  };
  colors?: {
    body?: string;
    heading?: string;
    border?: string;
  };
}

export interface LayoutDetail extends LayoutSummary {
  config: LayoutConfig;
}
