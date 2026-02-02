import { createSignal, Show } from "solid-js";
import { OpenSpec } from "../lib/forge";
import { Loader2, Download, FileText, Code, FileImage, Eye, X } from "lucide-solid";
import Button from "./button";

export type SpecExportModalProps = {
  spec: OpenSpec | null;
  isOpen: boolean;
  onClose: () => void;
};

type ExportFormat = "markdown" | "html" | "json";

export default function SpecExportModal(props: SpecExportModalProps) {
  const [format, setFormat] = createSignal<ExportFormat>("markdown");
  const [includeMetadata, setIncludeMetadata] = createSignal(true);
  const [includeDesign, setIncludeDesign] = createSignal(true);
  const [includeTasks, setIncludeTasks] = createSignal(true);
  const [showPreview, setShowPreview] = createSignal(false);
  const [exporting, setExporting] = createSignal(false);

  const generateMarkdown = () => {
    if (!props.spec) return "";

    let md = `# ${props.spec.project_name}\n\n`;

    if (includeMetadata()) {
      md += `**Spec Version**: ${props.spec.spec_version}\n\n`;
    }

    md += `## Requirement\n\n`;
    md += `### Summary\n${props.spec.requirement.summary}\n\n`;
    md += `### Description\n${props.spec.requirement.description}\n\n`;

    if (props.spec.requirement.acceptance_criteria.length > 0) {
      md += `### Acceptance Criteria\n`;
      props.spec.requirement.acceptance_criteria.forEach((criteria, i) => {
        md += `${i + 1}. ${criteria}\n`;
      });
      md += `\n`;
    }

    if (includeDesign() && props.spec.design) {
      md += `## Design\n\n`;
      md += `${JSON.stringify(props.spec.design, null, 2)}\n\n`;
    }

    if (includeTasks() && props.spec.tasks.length > 0) {
      md += `## Tasks\n\n`;
      props.spec.tasks.forEach((task, i) => {
        md += `### ${i + 1}. ${task.title}\n`;
        md += `- **ID**: ${task.id}\n`;
        md += `- **Status**: ${task.status}\n`;
        md += `- **Description**: ${task.description}\n\n`;
      });
    }

    return md;
  };

  const generateHTML = () => {
    if (!props.spec) return "";

    const md = generateMarkdown();
    // Simple markdown to HTML conversion
    let html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${props.spec.project_name}</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 800px;
      margin: 0 auto;
      padding: 2rem;
      line-height: 1.6;
      color: #333;
    }
    h1 { color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 0.5rem; }
    h2 { color: #1e40af; margin-top: 2rem; }
    h3 { color: #1e3a8a; }
    code { background: #f3f4f6; padding: 0.2rem 0.4rem; border-radius: 0.25rem; }
    pre { background: #f3f4f6; padding: 1rem; border-radius: 0.5rem; overflow-x: auto; }
    ul, ol { padding-left: 1.5rem; }
  </style>
</head>
<body>
${md
  .replace(/^# (.+)$/gm, '<h1>$1</h1>')
  .replace(/^## (.+)$/gm, '<h2>$1</h2>')
  .replace(/^### (.+)$/gm, '<h3>$1</h3>')
  .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
  .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  .replace(/\n\n/g, '</p><p>')
  .replace(/^(.+)$/gm, '<p>$1</p>')
}
</body>
</html>`;

    return html;
  };

  const generateJSON = () => {
    if (!props.spec) return "";

    const exportData: any = {
      spec_version: props.spec.spec_version,
      project_name: props.spec.project_name,
      requirement: props.spec.requirement,
    };

    if (includeDesign() && props.spec.design) {
      exportData.design = props.spec.design;
    }

    if (includeTasks()) {
      exportData.tasks = props.spec.tasks;
    }

    return JSON.stringify(exportData, null, 2);
  };

  const getExportContent = () => {
    switch (format()) {
      case "markdown":
        return generateMarkdown();
      case "html":
        return generateHTML();
      case "json":
        return generateJSON();
      default:
        return "";
    }
  };

  const getFileExtension = () => {
    switch (format()) {
      case "markdown":
        return "md";
      case "html":
        return "html";
      case "json":
        return "json";
      default:
        return "txt";
    }
  };

  const handleExport = async () => {
    if (!props.spec) return;

    setExporting(true);
    try {
      const content = getExportContent();
      const blob = new Blob([content], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${props.spec.project_name.replace(/\s+/g, "_")}.${getFileExtension()}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      setTimeout(() => {
        props.onClose();
      }, 500);
    } catch (err) {
      alert(`Export failed: ${err instanceof Error ? err.message : "Unknown error"}`);
    } finally {
      setExporting(false);
    }
  };

  if (!props.isOpen) return null;

  return (
    <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={props.onClose}>
      <div class="bg-[var(--bg-secondary)] rounded-lg border border-[var(--border-primary)] w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div class="flex items-center justify-between px-6 py-4 border-b border-[var(--border-primary)]">
          <h2 class="text-xl font-semibold">Export Spec</h2>
          <button onClick={props.onClose} class="text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors">
            <X class="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div class="flex-1 overflow-auto p-6">
          <Show when={!props.spec}>
            <div class="text-center py-12 text-[var(--text-secondary)]">
              <p>No spec available to export</p>
            </div>
          </Show>

          <Show when={props.spec}>
            <div class="space-y-6">
              {/* Format Selection */}
              <div>
                <label class="block text-sm font-medium mb-3">Export Format</label>
                <div class="grid grid-cols-3 gap-3">
                  <button
                    onClick={() => setFormat("markdown")}
                    class={`flex items-center gap-2 p-4 rounded-lg border transition-colors ${
                      format() === "markdown"
                        ? "border-blue-500 bg-blue-500/10 text-blue-400"
                        : "border-[var(--border-primary)] hover:border-[var(--border-secondary)]"
                    }`}
                  >
                    <FileText class="w-5 h-5" />
                    <div class="text-left">
                      <p class="font-medium">Markdown</p>
                      <p class="text-xs text-[var(--text-secondary)]">.md</p>
                    </div>
                  </button>

                  <button
                    onClick={() => setFormat("html")}
                    class={`flex items-center gap-2 p-4 rounded-lg border transition-colors ${
                      format() === "html"
                        ? "border-blue-500 bg-blue-500/10 text-blue-400"
                        : "border-[var(--border-primary)] hover:border-[var(--border-secondary)]"
                    }`}
                  >
                    <Code class="w-5 h-5" />
                    <div class="text-left">
                      <p class="font-medium">HTML</p>
                      <p class="text-xs text-[var(--text-secondary)]">.html</p>
                    </div>
                  </button>

                  <button
                    onClick={() => setFormat("json")}
                    class={`flex items-center gap-2 p-4 rounded-lg border transition-colors ${
                      format() === "json"
                        ? "border-blue-500 bg-blue-500/10 text-blue-400"
                        : "border-[var(--border-primary)] hover:border-[var(--border-secondary)]"
                    }`}
                  >
                    <FileImage class="w-5 h-5" />
                    <div class="text-left">
                      <p class="font-medium">JSON</p>
                      <p class="text-xs text-[var(--text-secondary)]">.json</p>
                    </div>
                  </button>
                </div>
              </div>

              {/* Export Options */}
              <div>
                <label class="block text-sm font-medium mb-3">Include Sections</label>
                <div class="space-y-2">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={includeMetadata()}
                      onChange={(e) => setIncludeMetadata(e.currentTarget.checked)}
                      class="w-4 h-4 rounded border-[var(--border-primary)] bg-[var(--bg-primary)] text-blue-500 focus:ring-2 focus:ring-blue-500"
                    />
                    <span class="text-sm">Metadata (version, timestamps)</span>
                  </label>

                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={includeDesign()}
                      onChange={(e) => setIncludeDesign(e.currentTarget.checked)}
                      class="w-4 h-4 rounded border-[var(--border-primary)] bg-[var(--bg-primary)] text-blue-500 focus:ring-2 focus:ring-blue-500"
                    />
                    <span class="text-sm">Design Section</span>
                  </label>

                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={includeTasks()}
                      onChange={(e) => setIncludeTasks(e.currentTarget.checked)}
                      class="w-4 h-4 rounded border-[var(--border-primary)] bg-[var(--bg-primary)] text-blue-500 focus:ring-2 focus:ring-blue-500"
                    />
                    <span class="text-sm">Tasks</span>
                  </label>
                </div>
              </div>

              {/* Preview */}
              <div>
                <div class="flex items-center justify-between mb-3">
                  <label class="block text-sm font-medium">Preview</label>
                  <button
                    onClick={() => setShowPreview(!showPreview())}
                    class="text-sm text-blue-400 hover:text-blue-300 flex items-center gap-1"
                  >
                    <Eye class="w-4 h-4" />
                    {showPreview() ? "Hide" : "Show"} Preview
                  </button>
                </div>

                <Show when={showPreview()}>
                  <div class="bg-[var(--bg-primary)] rounded-lg border border-[var(--border-primary)] p-4 max-h-64 overflow-auto">
                    <pre class="text-xs font-mono whitespace-pre-wrap break-words">
                      {getExportContent()}
                    </pre>
                  </div>
                </Show>
              </div>
            </div>
          </Show>
        </div>

        {/* Footer */}
        <div class="flex items-center justify-between px-6 py-4 border-t border-[var(--border-primary)]">
          <div class="text-sm text-[var(--text-secondary)]">
            <Show when={props.spec}>
              Export as: <span class="font-mono">{props.spec!.project_name.replace(/\s+/g, "_")}.{getFileExtension()}</span>
            </Show>
          </div>
          <div class="flex gap-2">
            <Button onClick={props.onClose} variant="secondary" disabled={exporting()}>
              Cancel
            </Button>
            <Button onClick={handleExport} disabled={exporting() || !props.spec}>
              <Show when={exporting()} fallback={
                <>
                  <Download class="w-4 h-4 mr-2" />
                  Export
                </>
              }>
                <Loader2 class="w-4 h-4 animate-spin mr-2" />
                Exporting...
              </Show>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
