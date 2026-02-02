import { createEffect, onCleanup, onMount } from "solid-js";
import { EditorState } from "@codemirror/state";
import { EditorView, keymap } from "@codemirror/view";
import { basicSetup } from "@codemirror/basic-setup";
import { json } from "@codemirror/lang-json";
import { defaultKeymap, history, historyKeymap } from "@codemirror/commands";
import { bracketMatching } from "@codemirror/language";

type SpecEditorProps = {
  value: string;
  onChange: (next: string) => void;
  errors: string[];
  title?: string;
  heightClass?: string;
};

const editorTheme = EditorView.theme({
  "&": {
    backgroundColor: "transparent",
    height: "100%",
    fontFamily:
      "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace",
    fontSize: "12px",
    lineHeight: "1.6"
  },
  ".cm-content": {
    padding: "12px"
  },
  ".cm-gutters": {
    backgroundColor: "transparent",
    border: "none",
    color: "var(--tw-prose-muted, #6b7280)"
  },
  ".cm-activeLineGutter": {
    backgroundColor: "rgba(148, 163, 184, 0.12)"
  },
  ".cm-activeLine": {
    backgroundColor: "rgba(148, 163, 184, 0.12)"
  }
});

const statusClass = (hasErrors: boolean) =>
  hasErrors
    ? "border-red-500/20 bg-red-500/10 text-red-600"
    : "border-green-500/20 bg-green-500/10 text-green-600";

const statusLabel = (hasErrors: boolean) => (hasErrors ? "Needs fixes" : "JSON valid");

export default function SpecEditor(props: SpecEditorProps) {
  let containerRef: HTMLDivElement | undefined;
  let view: EditorView | undefined;
  let suppressChange = false;

  onMount(() => {
    if (!containerRef) return;
    const state = EditorState.create({
      doc: props.value,
      extensions: [
        basicSetup,
        history(),
        keymap.of([...defaultKeymap, ...historyKeymap]),
        bracketMatching(),
        json(),
        EditorView.lineWrapping,
        editorTheme,
        EditorView.updateListener.of((update) => {
          if (!update.docChanged || suppressChange) return;
          props.onChange(update.state.doc.toString());
        })
      ]
    });

    view = new EditorView({
      state,
      parent: containerRef
    });
  });

  createEffect(() => {
    if (!view) return;
    const nextValue = props.value ?? "";
    const currentValue = view.state.doc.toString();
    if (nextValue === currentValue) return;
    suppressChange = true;
    view.dispatch({
      changes: { from: 0, to: currentValue.length, insert: nextValue }
    });
    suppressChange = false;
  });

  onCleanup(() => {
    view?.destroy();
    view = undefined;
  });

  return (
    <div class="flex flex-col gap-2">
      <div class="flex items-center justify-between gap-3">
        <div class="space-y-1">
          <div class="text-xs text-muted-foreground uppercase tracking-wider">
            {props.title ?? "OpenSpec JSON"}
          </div>
          <div class="text-xs text-muted-foreground">Live validation updates the preview.</div>
        </div>
        <div
          class={`text-[11px] font-semibold uppercase tracking-wider rounded-full border px-2.5 py-1 ${statusClass(
            props.errors.length > 0
          )}`}
        >
          {statusLabel(props.errors.length > 0)}
        </div>
      </div>
      <div
        class={`bg-background border border-border rounded-xl overflow-hidden ${
          props.heightClass ?? "min-h-[320px]"
        }`}
      >
        <div ref={containerRef} class="h-full w-full" />
      </div>
      {props.errors.length > 0 ? (
        <div class="bg-red-500/10 border border-red-500/30 text-red-600 text-xs rounded-lg p-3 space-y-1">
          {props.errors.map((error) => (
            <div>{error}</div>
          ))}
        </div>
      ) : null}
    </div>
  );
}
