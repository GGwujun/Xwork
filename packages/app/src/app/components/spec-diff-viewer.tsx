import { createSignal, createEffect, Show } from "solid-js";
import { OpenSpec } from "../lib/forge";
import { Loader2, Maximize2, Minimize2 } from "lucide-solid";
import Button from "./button";

export type SpecDiffViewerProps = {
  oldSpec: OpenSpec | null;
  newSpec: OpenSpec | null;
  oldLabel?: string;
  newLabel?: string;
  loading?: boolean;
};

type DiffMode = "side-by-side" | "unified";

export default function SpecDiffViewer(props: SpecDiffViewerProps) {
  const [mode, setMode] = createSignal<DiffMode>("side-by-side");
  const [expanded, setExpanded] = createSignal(false);
  const [stats, setStats] = createSignal({ added: 0, removed: 0, modified: 0 });

  createEffect(() => {
    if (props.oldSpec && props.newSpec) {
      calculateStats();
    }
  });

  const calculateStats = () => {
    const oldJson = JSON.stringify(props.oldSpec, null, 2);
    const newJson = JSON.stringify(props.newSpec, null, 2);
    const oldLines = oldJson.split("\n");
    const newLines = newJson.split("\n");

    let added = 0;
    let removed = 0;
    let modified = 0;

    // Simple line-based diff calculation
    const maxLen = Math.max(oldLines.length, newLines.length);
    for (let i = 0; i < maxLen; i++) {
      const oldLine = oldLines[i] || "";
      const newLine = newLines[i] || "";

      if (oldLine !== newLine) {
        if (!oldLine) added++;
        else if (!newLine) removed++;
        else modified++;
      }
    }

    setStats({ added, removed, modified });
  };

  const formatJson = (spec: OpenSpec | null) => {
    if (!spec) return "";
    return JSON.stringify(spec, null, 2);
  };

  const getDiffLines = () => {
    if (!props.oldSpec || !props.newSpec) return [];

    const oldJson = formatJson(props.oldSpec);
    const newJson = formatJson(props.newSpec);
    const oldLines = oldJson.split("\n");
    const newLines = newJson.split("\n");

    const maxLen = Math.max(oldLines.length, newLines.length);
    const diffLines: Array<{ type: "unchanged" | "added" | "removed" | "modified"; oldLine: string; newLine: string; lineNum: number }> = [];

    for (let i = 0; i < maxLen; i++) {
      const oldLine = oldLines[i] || "";
      const newLine = newLines[i] || "";

      if (oldLine === newLine) {
        diffLines.push({ type: "unchanged", oldLine, newLine, lineNum: i + 1 });
      } else if (!oldLine) {
        diffLines.push({ type: "added", oldLine: "", newLine, lineNum: i + 1 });
      } else if (!newLine) {
        diffLines.push({ type: "removed", oldLine, newLine: "", lineNum: i + 1 });
      } else {
        diffLines.push({ type: "modified", oldLine, newLine, lineNum: i + 1 });
      }
    }

    return diffLines;
  };

  const getLineClass = (type: string) => {
    switch (type) {
      case "added":
        return "bg-green-500/10 border-l-2 border-green-500";
      case "removed":
        return "bg-red-500/10 border-l-2 border-red-500";
      case "modified":
        return "bg-yellow-500/10 border-l-2 border-yellow-500";
      default:
        return "";
    }
  };

  return (
    <div class={`bg-[var(--bg-secondary)] rounded-lg border border-[var(--border-primary)] ${expanded() ? "fixed inset-4 z-50" : ""}`}>
      {/* Header */}
      <div class="flex items-center justify-between px-4 py-3 border-b border-[var(--border-primary)]">
        <div class="flex items-center gap-4">
          <h3 class="text-lg font-semibold">Spec Diff Viewer</h3>
          <Show when={!props.loading && props.oldSpec && props.newSpec}>
            <div class="flex items-center gap-3 text-sm">
              <span class="flex items-center gap-1">
                <span class="w-3 h-3 bg-green-500 rounded" />
                <span class="text-[var(--text-secondary)]">{stats().added} added</span>
              </span>
              <span class="flex items-center gap-1">
                <span class="w-3 h-3 bg-red-500 rounded" />
                <span class="text-[var(--text-secondary)]">{stats().removed} removed</span>
              </span>
              <span class="flex items-center gap-1">
                <span class="w-3 h-3 bg-yellow-500 rounded" />
                <span class="text-[var(--text-secondary)]">{stats().modified} modified</span>
              </span>
            </div>
          </Show>
        </div>

        <div class="flex items-center gap-2">
          <Show when={!props.loading && props.oldSpec && props.newSpec}>
            <div class="flex bg-[var(--bg-tertiary)] rounded p-1">
              <button
                onClick={() => setMode("side-by-side")}
                class={`px-3 py-1 text-sm rounded transition-colors ${
                  mode() === "side-by-side"
                    ? "bg-[var(--bg-primary)] text-[var(--text-primary)]"
                    : "text-[var(--text-secondary)] hover:text-[var(--text-primary)]"
                }`}
              >
                Side by Side
              </button>
              <button
                onClick={() => setMode("unified")}
                class={`px-3 py-1 text-sm rounded transition-colors ${
                  mode() === "unified"
                    ? "bg-[var(--bg-primary)] text-[var(--text-primary)]"
                    : "text-[var(--text-secondary)] hover:text-[var(--text-primary)]"
                }`}
              >
                Unified
              </button>
            </div>
          </Show>

          <button
            onClick={() => setExpanded(!expanded())}
            class="p-2 hover:bg-[var(--bg-tertiary)] rounded transition-colors"
            title={expanded() ? "Exit fullscreen" : "Enter fullscreen"}
          >
            {expanded() ? <Minimize2 class="w-4 h-4" /> : <Maximize2 class="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Content */}
      <div class={`overflow-auto ${expanded() ? "h-[calc(100%-60px)]" : "max-h-[600px]"}`}>
        <Show when={props.loading}>
          <div class="flex items-center justify-center h-64">
            <Loader2 class="w-8 h-8 animate-spin text-[var(--text-secondary)]" />
          </div>
        </Show>

        <Show when={!props.loading && (!props.oldSpec || !props.newSpec)}>
          <div class="flex items-center justify-center h-64 text-[var(--text-secondary)]">
            <p>No specs to compare</p>
          </div>
        </Show>

        <Show when={!props.loading && props.oldSpec && props.newSpec}>
          {/* Side by Side Mode */}
          <Show when={mode() === "side-by-side"}>
            <div class="grid grid-cols-2 divide-x divide-[var(--border-primary)]">
              {/* Old Version */}
              <div class="p-4">
                <div class="text-sm font-medium text-[var(--text-secondary)] mb-3">
                  {props.oldLabel || "Old Version"}
                </div>
                <pre class="text-xs font-mono leading-relaxed">
                  {getDiffLines().map((line) => (
                    <div class={`px-2 py-0.5 ${line.type === "removed" || line.type === "modified" ? getLineClass(line.type) : ""}`}>
                      <span class="text-[var(--text-secondary)] select-none mr-4">{line.lineNum}</span>
                      <span class={line.type === "removed" ? "text-red-400" : line.type === "modified" ? "text-yellow-400" : ""}>
                        {line.oldLine}
                      </span>
                    </div>
                  ))}
                </pre>
              </div>

              {/* New Version */}
              <div class="p-4">
                <div class="text-sm font-medium text-[var(--text-secondary)] mb-3">
                  {props.newLabel || "New Version"}
                </div>
                <pre class="text-xs font-mono leading-relaxed">
                  {getDiffLines().map((line) => (
                    <div class={`px-2 py-0.5 ${line.type === "added" || line.type === "modified" ? getLineClass(line.type) : ""}`}>
                      <span class="text-[var(--text-secondary)] select-none mr-4">{line.lineNum}</span>
                      <span class={line.type === "added" ? "text-green-400" : line.type === "modified" ? "text-yellow-400" : ""}>
                        {line.newLine}
                      </span>
                    </div>
                  ))}
                </pre>
              </div>
            </div>
          </Show>

          {/* Unified Mode */}
          <Show when={mode() === "unified"}>
            <div class="p-4">
              <div class="flex items-center justify-between mb-3">
                <div class="text-sm font-medium text-[var(--text-secondary)]">
                  {props.oldLabel || "Old"} → {props.newLabel || "New"}
                </div>
              </div>
              <pre class="text-xs font-mono leading-relaxed">
                {getDiffLines().map((line) => {
                  if (line.type === "unchanged") {
                    return (
                      <div class="px-2 py-0.5">
                        <span class="text-[var(--text-secondary)] select-none mr-4">{line.lineNum}</span>
                        <span>{line.oldLine}</span>
                      </div>
                    );
                  } else if (line.type === "removed") {
                    return (
                      <div class={`px-2 py-0.5 ${getLineClass("removed")}`}>
                        <span class="text-[var(--text-secondary)] select-none mr-4">-</span>
                        <span class="text-red-400">{line.oldLine}</span>
                      </div>
                    );
                  } else if (line.type === "added") {
                    return (
                      <div class={`px-2 py-0.5 ${getLineClass("added")}`}>
                        <span class="text-[var(--text-secondary)] select-none mr-4">+</span>
                        <span class="text-green-400">{line.newLine}</span>
                      </div>
                    );
                  } else {
                    // modified - show both lines
                    return (
                      <>
                        <div class={`px-2 py-0.5 ${getLineClass("removed")}`}>
                          <span class="text-[var(--text-secondary)] select-none mr-4">-</span>
                          <span class="text-red-400">{line.oldLine}</span>
                        </div>
                        <div class={`px-2 py-0.5 ${getLineClass("added")}`}>
                          <span class="text-[var(--text-secondary)] select-none mr-4">+</span>
                          <span class="text-green-400">{line.newLine}</span>
                        </div>
                      </>
                    );
                  }
                })}
              </pre>
            </div>
          </Show>
        </Show>
      </div>
    </div>
  );
}
