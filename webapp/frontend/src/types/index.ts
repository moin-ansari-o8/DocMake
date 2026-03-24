export type Theme = "light" | "dark";

export interface LayoutSummary {
  id: string;
  name: string;
  description?: string;
  immutable?: boolean;
  version?: number;
  base?: string;
}

export interface FontSpec {
  name: string;
  size: number;
}

export interface HeaderFooterConfig {
  height?: number;
  padding?: number;
  text?: string;
  logo?: string | null;
  align?: "left" | "center" | "right";
  color?: string;
}

export interface BarSpec {
  height?: number;
  color?: string;
}

export interface LayoutConfig {
  margins?: { left: number; right: number; top: number; bottom: number };
  fonts?: {
    body?: FontSpec;
    heading?: FontSpec;
    code?: FontSpec;
  };
  colors?: {
    body?: string;
    heading?: string;
    border?: string;
  };
  palette?: {
    primary?: string;
    muted?: string;
    surface?: string;
  };
  title?: {
    align?: "left" | "center" | "right";
    color?: string;
  };
  subtitle?: {
    align?: "left" | "center" | "right";
    color?: string;
  };
  body?: {
    paragraph?: { space_after?: number };
    list?: { indent?: number; item_spacing?: number; bullet?: string };
    code?: { padding?: number; bg?: string; border?: string };
    hr?: { thickness?: number; color?: string };
    layout?: { columns?: 1 | 2; gutter?: number };
  };
  header?: HeaderFooterConfig;
  footer?: HeaderFooterConfig;
  bars?: {
    top?: BarSpec;
    bottom?: BarSpec;
  };
  background?: {
    color?: string;
    image?: string | null;
    mode?: "cover" | "contain" | "tile";
  };
}

export interface LayoutDetail extends LayoutSummary {
  config: LayoutConfig;
  immutable?: boolean;
  version?: number;
  base?: string;
}

export interface PreflightResponse {
  valid: boolean;
  title: string;
  subtitle: string;
  blocks: Array<Record<string, unknown>>;
  warnings: string[];
}
