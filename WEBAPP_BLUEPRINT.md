# PDF Maker Web Application - System Blueprint

A comprehensive guide to building the PDF Maker web application with live preview, AI integration, and layout management.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Tech Stack](#tech-stack)
3. [Directory Structure](#directory-structure)
4. [UI/UX Design](#uiux-design)
5. [Frontend Implementation](#frontend-implementation)
6. [Backend Implementation](#backend-implementation)
7. [API Endpoints](#api-endpoints)
8. [AI Integration (Gemini)](#ai-integration-gemini)
9. [Layout Management System](#layout-management-system)
10. [Dark/Light Mode](#darklight-mode)
11. [Real-time Preview](#real-time-preview)
12. [Setup Instructions](#setup-instructions)
13. [Development Workflow](#development-workflow)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              WEB BROWSER                                │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                         React Frontend                            │  │
│  │  ┌─────────────────────────┐  ┌─────────────────────────────────┐ │  │
│  │  │      LEFT PANEL         │  │        RIGHT PANEL              │ │  │
│  │  │  ┌───────────────────┐  │  │  ┌────────────────────────────┐ │ │  │
│  │  │  │  Monaco Editor    │  │  │  │    PDF.js Viewer           │ │ │  │
│  │  │  │  (Markdown Input) │  │  │  │    (Live Preview)          │ │ │  │
│  │  │  └───────────────────┘  │  │  └────────────────────────────┘ │ │  │
│  │  │  ┌───────────────────┐  │  │  ┌────────────────────────────┐ │ │  │
│  │  │  │  Toolbar          │  │  │  │  Controls                  │ │ │  │
│  │  │  │  - AI Mode        │  │  │  │  - Download                │ │ │  │
│  │  │  │  - Layouts        │  │  │  │  - Zoom                    │ │ │  │
│  │  │  │  - Theme Toggle   │  │  │  │  - Page Nav                │ │ │  │
│  │  │  └───────────────────┘  │  │  └────────────────────────────┘ │ │  │
│  │  └─────────────────────────┘  └─────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP/WebSocket
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          FastAPI Backend                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐  │
│  │  PDF Generator  │  │  AI Service     │  │  Layout Manager         │  │
│  │  (reportlab)    │  │  (Gemini API)   │  │  (JSON configs)         │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           File System                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐  │
│  │  pdf-output/    │  │  layouts/       │  │  pdf-py/                │  │
│  │  (Generated)    │  │  (Saved configs)│  │  (Templates)            │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Frontend
| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | React 18 + Vite | Fast dev, modern React |
| Styling | TailwindCSS 3.x | Utility-first CSS, dark mode |
| Editor | Monaco Editor | VS Code-like Markdown editing |
| PDF Viewer | pdf.js (pdfjs-dist) | Browser PDF rendering |
| HTTP Client | Axios | API calls |
| State | Zustand | Lightweight state management |
| Icons | Lucide React | Clean icon set |

### Backend
| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | FastAPI | Async Python API |
| PDF Engine | reportlab | PDF generation (existing) |
| AI | Google Generative AI | Gemini API integration |
| CORS | FastAPI CORS | Cross-origin requests |
| File Handling | aiofiles | Async file operations |

---

## Directory Structure

```
pdf-maker/
├── pdf-py/                          # Existing Python templates
│   ├── pdf_template.py
│   └── generate_women_in_islam.py
│
├── pdf-output/                      # Generated PDFs
│
├── pdf-layout.skill                 # Style specification
│
├── webapp/                          # NEW: Web application
│   │
│   ├── frontend/                    # React application
│   │   ├── public/
│   │   │   └── pdf.worker.min.js   # PDF.js worker
│   │   │
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── Editor/
│   │   │   │   │   ├── MarkdownEditor.tsx
│   │   │   │   │   └── EditorToolbar.tsx
│   │   │   │   │
│   │   │   │   ├── Preview/
│   │   │   │   │   ├── PDFViewer.tsx
│   │   │   │   │   └── PreviewControls.tsx
│   │   │   │   │
│   │   │   │   ├── Layout/
│   │   │   │   │   ├── LayoutSelector.tsx
│   │   │   │   │   ├── LayoutEditor.tsx
│   │   │   │   │   └── LayoutList.tsx
│   │   │   │   │
│   │   │   │   ├── AI/
│   │   │   │   │   ├── AIPanel.tsx
│   │   │   │   │   └── AIPromptInput.tsx
│   │   │   │   │
│   │   │   │   ├── common/
│   │   │   │   │   ├── Button.tsx
│   │   │   │   │   ├── Modal.tsx
│   │   │   │   │   ├── Toggle.tsx
│   │   │   │   │   └── ThemeToggle.tsx
│   │   │   │   │
│   │   │   │   └── App.tsx
│   │   │   │
│   │   │   ├── hooks/
│   │   │   │   ├── useDebounce.ts
│   │   │   │   ├── usePDFGenerator.ts
│   │   │   │   ├── useLayouts.ts
│   │   │   │   └── useTheme.ts
│   │   │   │
│   │   │   ├── stores/
│   │   │   │   ├── editorStore.ts
│   │   │   │   ├── layoutStore.ts
│   │   │   │   └── themeStore.ts
│   │   │   │
│   │   │   ├── services/
│   │   │   │   ├── api.ts
│   │   │   │   └── pdfService.ts
│   │   │   │
│   │   │   ├── types/
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── styles/
│   │   │   │   └── globals.css
│   │   │   │
│   │   │   ├── App.tsx
│   │   │   ├── main.tsx
│   │   │   └── vite-env.d.ts
│   │   │
│   │   ├── index.html
│   │   ├── package.json
│   │   ├── tailwind.config.js
│   │   ├── postcss.config.js
│   │   ├── tsconfig.json
│   │   └── vite.config.ts
│   │
│   ├── backend/                     # FastAPI application
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py             # FastAPI entry point
│   │   │   ├── config.py           # Settings, env vars
│   │   │   │
│   │   │   ├── routers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── pdf.py          # PDF generation routes
│   │   │   │   ├── ai.py           # AI/Gemini routes
│   │   │   │   └── layouts.py      # Layout CRUD routes
│   │   │   │
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── pdf_generator.py
│   │   │   │   ├── ai_service.py
│   │   │   │   ├── layout_manager.py
│   │   │   │   └── markdown_parser.py
│   │   │   │
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── pdf_models.py
│   │   │   │   ├── ai_models.py
│   │   │   │   └── layout_models.py
│   │   │   │
│   │   │   └── utils/
│   │   │       ├── __init__.py
│   │   │       └── helpers.py
│   │   │
│   │   ├── requirements.txt
│   │   └── run.py                  # Server runner
│   │
│   └── layouts/                     # Saved layout configurations
│       ├── default.json
│       ├── academic.json
│       └── religious.json
│
├── HOW_TO_USE.md
├── WEBAPP_BLUEPRINT.md              # This file
├── requirements.txt
└── .gitignore
```

---

## UI/UX Design

### Main Layout (Desktop)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ┌─ Header ────────────────────────────────────────────────────────────────┐ │
│  │  [Logo] PDF Maker                              [AI Mode] [Theme] [Save] │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌─ Left Panel (50%) ─────────────────┐ ┌─ Right Panel (50%) ─────────────┐ │
│  │                                    │ │                                 │ │
│  │  ┌─ Toolbar ────────────────────┐  │ │  ┌─ Preview Header ──────────┐  │ │
│  │  │ [Layout: Default ▼] [+ New]  │  │ │  │ Page: [<] 1/3 [>]  [Zoom] │  │ │
│  │  └──────────────────────────────┘  │ │  └────────────────────────────┘  │ │
│  │                                    │ │                                 │ │
│  │  ┌─ Editor ─────────────────────┐  │ │  ┌─ PDF Viewer ──────────────┐  │ │
│  │  │                              │  │ │  │                           │  │ │
│  │  │  # My Document               │  │ │  │   ┌─────────────────────┐ │  │ │
│  │  │                              │  │ │  │   │                     │ │  │ │
│  │  │  ## Introduction             │  │ │  │   │   PDF PREVIEW       │ │  │ │
│  │  │                              │  │ │  │   │                     │ │  │ │
│  │  │  This is the content...      │  │ │  │   │   (Live rendered)   │ │  │ │
│  │  │                              │  │ │  │   │                     │ │  │ │
│  │  │  ## Section 2                │  │ │  │   │                     │ │  │ │
│  │  │                              │  │ │  │   └─────────────────────┘ │  │ │
│  │  │  More content here...        │  │ │  │                           │  │ │
│  │  │                              │  │ │  └───────────────────────────┘  │ │
│  │  │                              │  │ │                                 │ │
│  │  └──────────────────────────────┘  │ │  ┌─ Actions ─────────────────┐  │ │
│  │                                    │ │  │ [Generate PDF] [Download] │  │ │
│  │  ┌─ AI Panel (collapsible) ─────┐  │ │  └────────────────────────────┘  │ │
│  │  │ [Enhance with AI...]         │  │ │                                 │ │
│  │  └──────────────────────────────┘  │ │                                 │ │
│  │                                    │ │                                 │ │
│  └────────────────────────────────────┘ └─────────────────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Color Scheme

#### Light Mode
```css
--bg-primary: #FFFFFF;
--bg-secondary: #F9FAFB;
--bg-tertiary: #F3F4F6;
--text-primary: #111827;
--text-secondary: #4B5563;
--text-muted: #9CA3AF;
--border: #E5E7EB;
--accent: #3B82F6;
--accent-hover: #2563EB;
```

#### Dark Mode
```css
--bg-primary: #111827;
--bg-secondary: #1F2937;
--bg-tertiary: #374151;
--text-primary: #F9FAFB;
--text-secondary: #D1D5DB;
--text-muted: #6B7280;
--border: #374151;
--accent: #60A5FA;
--accent-hover: #3B82F6;
```

---

## Frontend Implementation

### 1. Package.json

```json
{
  "name": "pdf-maker-webapp",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@monaco-editor/react": "^4.6.0",
    "pdfjs-dist": "^4.0.379",
    "axios": "^1.6.0",
    "zustand": "^4.4.0",
    "lucide-react": "^0.294.0",
    "clsx": "^2.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  }
}
```

### 2. Tailwind Config (tailwind.config.js)

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eff6ff",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
        },
      },
    },
  },
  plugins: [],
};
```

### 3. Main App Component (App.tsx)

```tsx
import { useState } from "react";
import { MarkdownEditor } from "./components/Editor/MarkdownEditor";
import { PDFViewer } from "./components/Preview/PDFViewer";
import { Header } from "./components/common/Header";
import { LayoutSelector } from "./components/Layout/LayoutSelector";
import { AIPanel } from "./components/AI/AIPanel";
import { useTheme } from "./hooks/useTheme";
import { usePDFGenerator } from "./hooks/usePDFGenerator";

export default function App() {
  const { theme, toggleTheme } = useTheme();
  const [content, setContent] = useState<string>("");
  const [currentLayout, setCurrentLayout] = useState<string>("default");
  const [aiMode, setAiMode] = useState<boolean>(false);

  const { pdfUrl, isGenerating, generatePDF } = usePDFGenerator();

  return (
    <div className={`min-h-screen ${theme === "dark" ? "dark" : ""}`}>
      <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
        {/* Header */}
        <Header
          theme={theme}
          onToggleTheme={toggleTheme}
          aiMode={aiMode}
          onToggleAI={() => setAiMode(!aiMode)}
        />

        {/* Main Content */}
        <div className="flex h-[calc(100vh-64px)]">
          {/* Left Panel - Editor */}
          <div className="w-1/2 flex flex-col border-r border-gray-200 dark:border-gray-700">
            {/* Layout Selector */}
            <LayoutSelector
              currentLayout={currentLayout}
              onLayoutChange={setCurrentLayout}
            />

            {/* Markdown Editor */}
            <div className="flex-1 overflow-hidden">
              <MarkdownEditor
                value={content}
                onChange={setContent}
                theme={theme}
              />
            </div>

            {/* AI Panel (Collapsible) */}
            {aiMode && (
              <AIPanel
                content={content}
                onContentUpdate={setContent}
              />
            )}
          </div>

          {/* Right Panel - Preview */}
          <div className="w-1/2 flex flex-col bg-gray-50 dark:bg-gray-800">
            <PDFViewer
              pdfUrl={pdfUrl}
              isGenerating={isGenerating}
              onGenerate={() => generatePDF(content, currentLayout)}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
```

### 4. Monaco Editor Component (MarkdownEditor.tsx)

```tsx
import Editor from "@monaco-editor/react";

interface MarkdownEditorProps {
  value: string;
  onChange: (value: string) => void;
  theme: "light" | "dark";
}

export function MarkdownEditor({ value, onChange, theme }: MarkdownEditorProps) {
  return (
    <Editor
      height="100%"
      language="markdown"
      theme={theme === "dark" ? "vs-dark" : "light"}
      value={value}
      onChange={(val) => onChange(val || "")}
      options={{
        minimap: { enabled: false },
        wordWrap: "on",
        fontSize: 14,
        lineHeight: 24,
        padding: { top: 16, bottom: 16 },
        scrollBeyondLastLine: false,
        automaticLayout: true,
      }}
    />
  );
}
```

### 5. PDF Viewer Component (PDFViewer.tsx)

```tsx
import { useEffect, useRef, useState } from "react";
import * as pdfjsLib from "pdfjs-dist";
import { ChevronLeft, ChevronRight, ZoomIn, ZoomOut, Download, Loader2 } from "lucide-react";

// Configure PDF.js worker
pdfjsLib.GlobalWorkerOptions.workerSrc = "/pdf.worker.min.js";

interface PDFViewerProps {
  pdfUrl: string | null;
  isGenerating: boolean;
  onGenerate: () => void;
}

export function PDFViewer({ pdfUrl, isGenerating, onGenerate }: PDFViewerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [pdf, setPdf] = useState<pdfjsLib.PDFDocumentProxy | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [scale, setScale] = useState(1.2);

  // Load PDF when URL changes
  useEffect(() => {
    if (!pdfUrl) return;

    const loadPDF = async () => {
      const loadingTask = pdfjsLib.getDocument(pdfUrl);
      const pdfDoc = await loadingTask.promise;
      setPdf(pdfDoc);
      setTotalPages(pdfDoc.numPages);
      setCurrentPage(1);
    };

    loadPDF();
  }, [pdfUrl]);

  // Render current page
  useEffect(() => {
    if (!pdf || !canvasRef.current) return;

    const renderPage = async () => {
      const page = await pdf.getPage(currentPage);
      const viewport = page.getViewport({ scale });
      const canvas = canvasRef.current!;
      const context = canvas.getContext("2d")!;

      canvas.height = viewport.height;
      canvas.width = viewport.width;

      await page.render({
        canvasContext: context,
        viewport,
      }).promise;
    };

    renderPage();
  }, [pdf, currentPage, scale]);

  return (
    <div className="flex flex-col h-full">
      {/* Controls */}
      <div className="flex items-center justify-between p-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
        {/* Page Navigation */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={currentPage <= 1}
            className="p-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50"
          >
            <ChevronLeft size={18} />
          </button>
          <span className="text-sm">
            Page {currentPage} of {totalPages || "-"}
          </span>
          <button
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            disabled={currentPage >= totalPages}
            className="p-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50"
          >
            <ChevronRight size={18} />
          </button>
        </div>

        {/* Zoom Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setScale((s) => Math.max(0.5, s - 0.2))}
            className="p-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-800"
          >
            <ZoomOut size={18} />
          </button>
          <span className="text-sm w-16 text-center">{Math.round(scale * 100)}%</span>
          <button
            onClick={() => setScale((s) => Math.min(3, s + 0.2))}
            className="p-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-800"
          >
            <ZoomIn size={18} />
          </button>
        </div>

        {/* Download */}
        {pdfUrl && (
          <a
            href={pdfUrl}
            download="document.pdf"
            className="flex items-center gap-1.5 px-3 py-1.5 text-sm bg-primary-500 text-white rounded hover:bg-primary-600"
          >
            <Download size={16} />
            Download
          </a>
        )}
      </div>

      {/* PDF Canvas */}
      <div className="flex-1 overflow-auto p-4 flex justify-center">
        {isGenerating ? (
          <div className="flex items-center justify-center h-full">
            <Loader2 className="w-8 h-8 animate-spin text-primary-500" />
            <span className="ml-2">Generating PDF...</span>
          </div>
        ) : pdfUrl ? (
          <canvas
            ref={canvasRef}
            className="shadow-lg bg-white"
          />
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-gray-500">
            <p className="mb-4">No PDF generated yet</p>
            <button
              onClick={onGenerate}
              className="px-4 py-2 bg-primary-500 text-white rounded hover:bg-primary-600"
            >
              Generate PDF
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
```

### 6. Theme Toggle Component (ThemeToggle.tsx)

```tsx
import { Sun, Moon } from "lucide-react";

interface ThemeToggleProps {
  theme: "light" | "dark";
  onToggle: () => void;
}

export function ThemeToggle({ theme, onToggle }: ThemeToggleProps) {
  return (
    <button
      onClick={onToggle}
      className="relative w-14 h-7 rounded-full bg-gray-200 dark:bg-gray-700 transition-colors"
      aria-label="Toggle theme"
    >
      <span
        className={`absolute top-0.5 w-6 h-6 rounded-full bg-white shadow-md transition-transform flex items-center justify-center ${
          theme === "dark" ? "translate-x-7" : "translate-x-0.5"
        }`}
      >
        {theme === "dark" ? (
          <Moon size={14} className="text-gray-700" />
        ) : (
          <Sun size={14} className="text-yellow-500" />
        )}
      </span>
    </button>
  );
}
```

### 7. Layout Selector Component (LayoutSelector.tsx)

```tsx
import { useState } from "react";
import { ChevronDown, Plus, Settings } from "lucide-react";
import { useLayouts } from "../../hooks/useLayouts";

interface LayoutSelectorProps {
  currentLayout: string;
  onLayoutChange: (layoutId: string) => void;
}

export function LayoutSelector({ currentLayout, onLayoutChange }: LayoutSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const { layouts, createLayout } = useLayouts();

  return (
    <div className="flex items-center gap-2 p-3 border-b border-gray-200 dark:border-gray-700">
      {/* Layout Dropdown */}
      <div className="relative">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-2 px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-800"
        >
          <span className="text-sm">
            Layout: {layouts.find((l) => l.id === currentLayout)?.name || "Default"}
          </span>
          <ChevronDown size={16} />
        </button>

        {isOpen && (
          <div className="absolute top-full left-0 mt-1 w-48 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded shadow-lg z-10">
            {layouts.map((layout) => (
              <button
                key={layout.id}
                onClick={() => {
                  onLayoutChange(layout.id);
                  setIsOpen(false);
                }}
                className={`w-full text-left px-3 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 ${
                  currentLayout === layout.id ? "bg-primary-50 dark:bg-primary-900/20" : ""
                }`}
              >
                {layout.name}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* New Layout Button */}
      <button
        onClick={() => createLayout()}
        className="flex items-center gap-1 px-2 py-1.5 text-sm text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded"
      >
        <Plus size={16} />
        New
      </button>

      {/* Settings */}
      <button className="p-1.5 text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 rounded">
        <Settings size={18} />
      </button>
    </div>
  );
}
```

### 8. AI Panel Component (AIPanel.tsx)

```tsx
import { useState } from "react";
import { Sparkles, Send, Loader2 } from "lucide-react";
import { aiService } from "../../services/api";

interface AIPanelProps {
  content: string;
  onContentUpdate: (content: string) => void;
}

export function AIPanel({ content, onContentUpdate }: AIPanelProps) {
  const [prompt, setPrompt] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  const handleEnhance = async () => {
    if (!prompt.trim()) return;

    setIsProcessing(true);
    try {
      const enhanced = await aiService.enhance(content, prompt);
      onContentUpdate(enhanced);
      setPrompt("");
    } catch (error) {
      console.error("AI enhancement failed:", error);
    } finally {
      setIsProcessing(false);
    }
  };

  const quickActions = [
    { label: "Expand", prompt: "Expand this content with more details and examples" },
    { label: "Summarize", prompt: "Summarize this content concisely" },
    { label: "Format", prompt: "Format this content with proper headings and structure" },
    { label: "Add Sections", prompt: "Add relevant sections and subsections" },
  ];

  return (
    <div className="border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 p-3">
      <div className="flex items-center gap-2 mb-3">
        <Sparkles size={18} className="text-primary-500" />
        <span className="text-sm font-medium">AI Enhancement</span>
      </div>

      {/* Quick Actions */}
      <div className="flex flex-wrap gap-2 mb-3">
        {quickActions.map((action) => (
          <button
            key={action.label}
            onClick={() => setPrompt(action.prompt)}
            className="px-2 py-1 text-xs bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded hover:border-primary-500"
          >
            {action.label}
          </button>
        ))}
      </div>

      {/* Prompt Input */}
      <div className="flex gap-2">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter instruction for AI..."
          className="flex-1 px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 focus:outline-none focus:border-primary-500"
          onKeyDown={(e) => e.key === "Enter" && handleEnhance()}
        />
        <button
          onClick={handleEnhance}
          disabled={isProcessing || !prompt.trim()}
          className="flex items-center gap-1.5 px-3 py-2 bg-primary-500 text-white rounded hover:bg-primary-600 disabled:opacity-50"
        >
          {isProcessing ? (
            <Loader2 size={16} className="animate-spin" />
          ) : (
            <Send size={16} />
          )}
        </button>
      </div>
    </div>
  );
}
```

### 9. Theme Hook (useTheme.ts)

```typescript
import { create } from "zustand";
import { persist } from "zustand/middleware";

type Theme = "light" | "dark";

interface ThemeStore {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

export const useTheme = create<ThemeStore>()(
  persist(
    (set, get) => ({
      theme: "light",
      toggleTheme: () => {
        const newTheme = get().theme === "light" ? "dark" : "light";
        set({ theme: newTheme });
        document.documentElement.classList.toggle("dark", newTheme === "dark");
      },
      setTheme: (theme) => {
        set({ theme });
        document.documentElement.classList.toggle("dark", theme === "dark");
      },
    }),
    {
      name: "pdf-maker-theme",
      onRehydrateStorage: () => (state) => {
        if (state) {
          document.documentElement.classList.toggle("dark", state.theme === "dark");
        }
      },
    }
  )
);
```

### 10. API Service (api.ts)

```typescript
import axios from "axios";

const API_BASE = "http://localhost:8000/api";

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

  preview: async (content: string, layoutId: string): Promise<string> => {
    const blob = await pdfService.generate(content, layoutId);
    return URL.createObjectURL(blob);
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

  generateFromPrompt: async (prompt: string): Promise<string> => {
    const response = await api.post("/ai/generate", { prompt });
    return response.data.content;
  },
};

export const layoutService = {
  getAll: async () => {
    const response = await api.get("/layouts");
    return response.data;
  },

  get: async (id: string) => {
    const response = await api.get(`/layouts/${id}`);
    return response.data;
  },

  create: async (layout: any) => {
    const response = await api.post("/layouts", layout);
    return response.data;
  },

  update: async (id: string, layout: any) => {
    const response = await api.put(`/layouts/${id}`, layout);
    return response.data;
  },

  delete: async (id: string) => {
    await api.delete(`/layouts/${id}`);
  },
};
```

---

## Backend Implementation

### 1. Requirements (backend/requirements.txt)

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6
aiofiles>=23.2.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
google-generativeai>=0.3.0
reportlab>=4.0.0
arabic-reshaper>=3.0.0
python-bidi>=0.4.2
```

### 2. Main FastAPI App (app/main.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import pdf, ai, layouts
from app.config import settings

app = FastAPI(
    title="PDF Maker API",
    version="1.0.0",
    description="API for PDF generation with AI enhancement"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pdf.router, prefix="/api/pdf", tags=["PDF"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(layouts.router, prefix="/api/layouts", tags=["Layouts"])

# Serve PDF output files
app.mount("/pdf-output", StaticFiles(directory="../pdf-output"), name="pdf-output")


@app.get("/")
def root():
    return {"message": "PDF Maker API", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

### 3. Config (app/config.py)

```python
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    PDF_OUTPUT_DIR: Path = BASE_DIR / "pdf-output"
    LAYOUTS_DIR: Path = BASE_DIR / "layouts"
    PDF_PY_DIR: Path = BASE_DIR / "pdf-py"

    # API Keys
    GEMINI_API_KEY: str = ""

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()

# Ensure directories exist
settings.PDF_OUTPUT_DIR.mkdir(exist_ok=True)
settings.LAYOUTS_DIR.mkdir(exist_ok=True)
```

### 4. PDF Router (app/routers/pdf.py)

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.services.pdf_generator import PDFGenerator
from app.services.markdown_parser import MarkdownParser
from app.config import settings

router = APIRouter()


class GeneratePDFRequest(BaseModel):
    content: str
    layout_id: str = "default"
    title: str = "Document"


@router.post("/generate")
async def generate_pdf(request: GeneratePDFRequest):
    """Generate PDF from markdown content"""
    try:
        # Parse markdown to structured content
        parser = MarkdownParser()
        parsed = parser.parse(request.content)

        # Generate PDF
        generator = PDFGenerator(layout_id=request.layout_id)
        output_path = generator.generate(
            content=parsed,
            title=request.title
        )

        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename=f"{request.title}.pdf"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/preview")
async def preview_pdf(request: GeneratePDFRequest):
    """Generate preview PDF (same as generate but with temp file)"""
    return await generate_pdf(request)
```

### 5. AI Router (app/routers/ai.py)

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.ai_service import GeminiService
from app.config import settings

router = APIRouter()
ai_service = GeminiService(api_key=settings.GEMINI_API_KEY)


class EnhanceRequest(BaseModel):
    content: str
    instruction: str


class GenerateRequest(BaseModel):
    prompt: str


@router.post("/enhance")
async def enhance_content(request: EnhanceRequest):
    """Enhance content using Gemini AI"""
    try:
        enhanced = await ai_service.enhance(
            content=request.content,
            instruction=request.instruction
        )
        return {"enhanced_content": enhanced}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate")
async def generate_content(request: GenerateRequest):
    """Generate content from prompt using Gemini AI"""
    try:
        content = await ai_service.generate(prompt=request.prompt)
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 6. Layouts Router (app/routers/layouts.py)

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.services.layout_manager import LayoutManager

router = APIRouter()
layout_manager = LayoutManager()


class LayoutBase(BaseModel):
    name: str
    description: Optional[str] = ""
    config: Dict[str, Any]


class LayoutCreate(LayoutBase):
    pass


class LayoutUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


@router.get("")
async def list_layouts():
    """List all available layouts"""
    return layout_manager.list_all()


@router.get("/{layout_id}")
async def get_layout(layout_id: str):
    """Get a specific layout by ID"""
    layout = layout_manager.get(layout_id)
    if not layout:
        raise HTTPException(status_code=404, detail="Layout not found")
    return layout


@router.post("")
async def create_layout(layout: LayoutCreate):
    """Create a new layout"""
    return layout_manager.create(layout.model_dump())


@router.put("/{layout_id}")
async def update_layout(layout_id: str, layout: LayoutUpdate):
    """Update an existing layout"""
    updated = layout_manager.update(layout_id, layout.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Layout not found")
    return updated


@router.delete("/{layout_id}")
async def delete_layout(layout_id: str):
    """Delete a layout"""
    success = layout_manager.delete(layout_id)
    if not success:
        raise HTTPException(status_code=404, detail="Layout not found")
    return {"message": "Layout deleted"}
```

### 7. AI Service (app/services/ai_service.py)

```python
import google.generativeai as genai
from typing import Optional


class GeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-pro")
        else:
            self.model = None

    async def enhance(self, content: str, instruction: str) -> str:
        """Enhance content based on instruction"""
        if not self.model:
            raise ValueError("Gemini API key not configured")

        prompt = f"""You are a professional content editor.

INSTRUCTION: {instruction}

CONTENT TO ENHANCE:
{content}

Respond with ONLY the enhanced content. Do not include explanations or meta-commentary.
Keep the markdown format intact.
Do not use em dashes (—) or double hyphens (--). Use commas, semicolons, or colons instead.
"""

        response = await self.model.generate_content_async(prompt)
        return response.text

    async def generate(self, prompt: str) -> str:
        """Generate content from prompt"""
        if not self.model:
            raise ValueError("Gemini API key not configured")

        system_prompt = f"""You are a professional content writer.

USER REQUEST: {prompt}

Generate well-structured markdown content based on the request.
Use proper headings (# for main title, ## for sections, ### for subsections).
Keep paragraphs concise and well-organized.
Do not use em dashes (—) or double hyphens (--). Use commas, semicolons, or colons instead.
"""

        response = await self.model.generate_content_async(system_prompt)
        return response.text
```

### 8. Markdown Parser (app/services/markdown_parser.py)

```python
import re
from typing import List, Dict, Any


class MarkdownParser:
    """Parse Markdown content into structured format for PDF generation"""

    def parse(self, content: str) -> Dict[str, Any]:
        """Parse markdown into structured document"""
        lines = content.strip().split("\n")

        document = {
            "title": "",
            "subtitle": "",
            "sections": []
        }

        current_section = None
        current_content = []

        for line in lines:
            # Main title (# )
            if line.startswith("# "):
                document["title"] = line[2:].strip()

            # Subtitle (> ) after title
            elif line.startswith("> ") and not current_section:
                document["subtitle"] = line[2:].strip()

            # Section heading (## )
            elif line.startswith("## "):
                if current_section:
                    current_section["content"] = "\n".join(current_content)
                    document["sections"].append(current_section)

                current_section = {
                    "heading": line[3:].strip(),
                    "subsections": [],
                    "content": ""
                }
                current_content = []

            # Subsection heading (### )
            elif line.startswith("### "):
                if current_section:
                    current_section["subsections"].append({
                        "heading": line[4:].strip(),
                        "content": ""
                    })

            # Regular content
            else:
                current_content.append(line)

        # Add last section
        if current_section:
            current_section["content"] = "\n".join(current_content)
            document["sections"].append(current_section)

        return document
```

### 9. PDF Generator Service (app/services/pdf_generator.py)

```python
import sys
from pathlib import Path
from datetime import datetime

# Add pdf-py to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "pdf-py"))

from pdf_template import *
from app.services.layout_manager import LayoutManager
from app.config import settings


class PDFGenerator:
    def __init__(self, layout_id: str = "default"):
        self.layout_manager = LayoutManager()
        self.layout = self.layout_manager.get(layout_id) or self.layout_manager.get("default")

    def generate(self, content: dict, title: str) -> Path:
        """Generate PDF from parsed content"""
        story = []

        # Cover
        story.append(create_cover(
            title=content.get("title", title).upper(),
            subtitle=content.get("subtitle", ""),
            metadata=""
        ))
        story.append(sp(10))

        # Sections
        for sec in content.get("sections", []):
            # Section heading
            story.extend(section(sec["heading"]))

            # Section content
            if sec.get("content"):
                paragraphs = sec["content"].strip().split("\n\n")
                for para in paragraphs:
                    if para.strip():
                        # Clean up dashes
                        para = para.replace("—", ", ").replace("--", ", ")
                        story.append(p(para.strip()))
                        story.append(sp(6))

            # Subsections
            for subsec in sec.get("subsections", []):
                story.extend(subsection(subsec["heading"]))
                if subsec.get("content"):
                    story.append(p(subsec["content"].strip()))
                    story.append(sp(4))

            story.append(rule())

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{title.lower().replace(' ', '_')}_{timestamp}.pdf"
        output_path = settings.PDF_OUTPUT_DIR / filename

        # Build PDF
        build_pdf(
            str(output_path),
            content.get("title", title),
            story
        )

        return output_path
```

### 10. Layout Manager (app/services/layout_manager.py)

```python
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
import uuid

from app.config import settings


class LayoutManager:
    def __init__(self):
        self.layouts_dir = settings.LAYOUTS_DIR
        self._ensure_default_layout()

    def _ensure_default_layout(self):
        """Ensure default layout exists"""
        default_path = self.layouts_dir / "default.json"
        if not default_path.exists():
            default_layout = {
                "id": "default",
                "name": "Default",
                "description": "Standard document layout",
                "config": {
                    "margins": {"left": 10, "right": 10, "top": 12, "bottom": 13},
                    "fonts": {
                        "body": {"name": "Helvetica", "size": 10.5},
                        "heading": {"name": "Helvetica-Bold", "size": 13},
                    },
                    "colors": {
                        "body": "#333333",
                        "heading": "#111111",
                        "footer_bg": "#222222",
                    },
                }
            }
            self._save(default_path, default_layout)

    def _load(self, path: Path) -> Optional[Dict[str, Any]]:
        """Load layout from file"""
        try:
            with open(path, "r") as f:
                return json.load(f)
        except:
            return None

    def _save(self, path: Path, layout: Dict[str, Any]):
        """Save layout to file"""
        with open(path, "w") as f:
            json.dump(layout, f, indent=2)

    def list_all(self) -> List[Dict[str, Any]]:
        """List all layouts"""
        layouts = []
        for file in self.layouts_dir.glob("*.json"):
            layout = self._load(file)
            if layout:
                layouts.append({
                    "id": layout.get("id", file.stem),
                    "name": layout.get("name", file.stem),
                    "description": layout.get("description", ""),
                })
        return layouts

    def get(self, layout_id: str) -> Optional[Dict[str, Any]]:
        """Get layout by ID"""
        path = self.layouts_dir / f"{layout_id}.json"
        return self._load(path)

    def create(self, layout: Dict[str, Any]) -> Dict[str, Any]:
        """Create new layout"""
        layout_id = str(uuid.uuid4())[:8]
        layout["id"] = layout_id
        path = self.layouts_dir / f"{layout_id}.json"
        self._save(path, layout)
        return layout

    def update(self, layout_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update existing layout"""
        path = self.layouts_dir / f"{layout_id}.json"
        layout = self._load(path)
        if not layout:
            return None

        layout.update(updates)
        self._save(path, layout)
        return layout

    def delete(self, layout_id: str) -> bool:
        """Delete layout"""
        if layout_id == "default":
            return False  # Cannot delete default

        path = self.layouts_dir / f"{layout_id}.json"
        if path.exists():
            path.unlink()
            return True
        return False
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/pdf/generate` | Generate PDF from markdown |
| `POST` | `/api/pdf/preview` | Generate preview PDF |
| `POST` | `/api/ai/enhance` | Enhance content with AI |
| `POST` | `/api/ai/generate` | Generate content from prompt |
| `GET` | `/api/layouts` | List all layouts |
| `GET` | `/api/layouts/{id}` | Get specific layout |
| `POST` | `/api/layouts` | Create new layout |
| `PUT` | `/api/layouts/{id}` | Update layout |
| `DELETE` | `/api/layouts/{id}` | Delete layout |

### Request/Response Examples

#### Generate PDF
```bash
POST /api/pdf/generate
Content-Type: application/json

{
  "content": "# My Document\n\n## Introduction\n\nThis is the content...",
  "layout_id": "default",
  "title": "My Document"
}
```

#### AI Enhancement
```bash
POST /api/ai/enhance
Content-Type: application/json

{
  "content": "# My Notes\n\nSome rough notes here...",
  "instruction": "Expand this into a detailed document with proper structure"
}

Response:
{
  "enhanced_content": "# My Notes\n\n## Overview\n\nThese notes cover..."
}
```

---

## AI Integration (Gemini)

### Setup

1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create `.env` file in `webapp/backend/`:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### Features

1. **Content Enhancement**
   - Expand brief notes into detailed content
   - Summarize long content
   - Restructure and format
   - Add sections and headings

2. **Content Generation**
   - Generate full documents from prompts
   - Create outlines
   - Generate study guides

3. **Style Adherence**
   - AI follows PDF layout rules (no em dashes, proper structure)
   - Maintains markdown formatting

---

## Layout Management System

### Layout Configuration Structure

```json
{
  "id": "academic",
  "name": "Academic Paper",
  "description": "Layout for academic documents",
  "config": {
    "margins": {
      "left": 25,
      "right": 25,
      "top": 20,
      "bottom": 20
    },
    "fonts": {
      "body": {
        "name": "Times-Roman",
        "size": 12
      },
      "heading": {
        "name": "Times-Bold",
        "size": 14
      }
    },
    "colors": {
      "body": "#000000",
      "heading": "#000000",
      "footer_bg": "#333333"
    },
    "spacing": {
      "paragraph": 8,
      "section": 16
    }
  }
}
```

### Creating Layouts via Prompt

Users can create layouts using natural language:

```
"Create a layout for religious texts with larger Arabic text,
generous margins, and elegant serif fonts"
```

The AI parses this and generates appropriate JSON config.

---

## Dark/Light Mode

### Implementation

1. **CSS Variables** (globals.css):
```css
:root {
  --bg-primary: #ffffff;
  --text-primary: #111827;
}

.dark {
  --bg-primary: #111827;
  --text-primary: #f9fafb;
}
```

2. **Tailwind Classes**:
```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
```

3. **Toggle Logic**:
```typescript
document.documentElement.classList.toggle("dark", isDark);
```

4. **Persistence**:
   - Store preference in localStorage
   - Zustand with persist middleware

---

## Real-time Preview

### Approach: Debounced Generation

```typescript
// usePDFGenerator.ts
export function usePDFGenerator() {
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  // Debounce content changes (500ms)
  const debouncedContent = useDebounce(content, 500);

  useEffect(() => {
    if (debouncedContent) {
      generatePreview();
    }
  }, [debouncedContent]);

  const generatePreview = async () => {
    setIsGenerating(true);
    try {
      const blob = await pdfService.generate(content, layoutId);
      const url = URL.createObjectURL(blob);
      setPdfUrl(url);
    } finally {
      setIsGenerating(false);
    }
  };

  return { pdfUrl, isGenerating, generatePDF: generatePreview };
}
```

### Performance Optimization

1. **Debounce Input** - Wait 500ms after typing stops
2. **Cancel Previous Request** - Abort in-flight requests
3. **Loading State** - Show spinner during generation
4. **Caching** - Cache generated PDFs by content hash

---

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or pnpm

### Backend Setup

```bash
# Navigate to backend
cd pdf-maker/webapp/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env

# Run server
python run.py
```

### Frontend Setup

```bash
# Navigate to frontend
cd pdf-maker/webapp/frontend

# Install dependencies
npm install

# Copy PDF.js worker
cp node_modules/pdfjs-dist/build/pdf.worker.min.js public/

# Run dev server
npm run dev
```

### Access Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Development Workflow

### Adding New Features

1. **Backend First**
   - Add router in `app/routers/`
   - Add service in `app/services/`
   - Register router in `main.py`
   - Test with `/docs`

2. **Frontend Next**
   - Add API call in `services/api.ts`
   - Create component in `components/`
   - Add hook if needed in `hooks/`
   - Integrate in `App.tsx`

### Testing

```bash
# Backend
cd webapp/backend
pytest

# Frontend
cd webapp/frontend
npm run test
```

### Building for Production

```bash
# Frontend build
cd webapp/frontend
npm run build

# Serve with backend
# Copy dist/ to backend static files
```

---

## Summary

This webapp provides:

- ✅ **Split-panel interface** (Editor | Preview)
- ✅ **Monaco Editor** for Markdown editing
- ✅ **pdf.js** for live PDF preview
- ✅ **AI Integration** (Gemini) for content enhancement
- ✅ **Layout System** with save/load/create
- ✅ **Dark/Light Mode** toggle
- ✅ **FastAPI Backend** connecting existing PDF engine
- ✅ **Real-time Preview** with debouncing

Ready to start building! 🚀
