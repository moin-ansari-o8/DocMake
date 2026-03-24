import axios from "axios";
import type { LayoutDetail, LayoutSummary, PreflightResponse } from "../types";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

export const pdfService = {
  generate: async (content: string, layoutId: string): Promise<Blob> => {
    const response = await api.post(
      "/pdf/generate",
      { content, layout_id: layoutId },
      { responseType: "blob" }
    );
    return response.data;
  },
  preflight: async (content: string, layoutId: string): Promise<PreflightResponse> => {
    const response = await api.post("/pdf/preflight", {
      content,
      layout_id: layoutId,
    });
    return response.data;
  },
};

export const aiService = {
  enhance: async (content: string, instruction: string): Promise<string> => {
    const response = await api.post("/ai/enhance", {
      content,
      instruction,
    });
    return response.data.enhanced_content;
  },
};

export const layoutService = {
  getAll: async (): Promise<LayoutSummary[]> => {
    const response = await api.get("/layouts");
    return response.data;
  },

  get: async (id: string): Promise<LayoutDetail> => {
    const response = await api.get(`/layouts/${id}`);
    return response.data;
  },

  create: async (layout: Omit<LayoutDetail, "id">): Promise<LayoutDetail> => {
    const response = await api.post("/layouts", layout);
    return response.data;
  },
  clone: async (
    sourceId: string,
    name?: string,
    description?: string
  ): Promise<LayoutDetail> => {
    const response = await api.post("/layouts/clone", {
      source_id: sourceId,
      name,
      description,
    });
    return response.data;
  },
  update: async (
    id: string,
    updates: Partial<Omit<LayoutDetail, "id">>
  ): Promise<LayoutDetail> => {
    const response = await api.put(`/layouts/${id}`, updates);
    return response.data;
  },
  remove: async (id: string): Promise<void> => {
    await api.delete(`/layouts/${id}`);
  },
};

export const assetService = {
  upload: async (
    file: File,
    kind: "logo" | "background",
    userId = "local-user"
  ): Promise<{ path: string; kind: string; size: number }> => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("kind", kind);
    formData.append("user_id", userId);
    const response = await api.post("/assets/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  },
};
