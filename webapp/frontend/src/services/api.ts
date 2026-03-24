import axios from "axios";
import type { LayoutDetail, LayoutSummary } from "../types";

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
};
