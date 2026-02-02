import { For, Show } from "solid-js";
import type { OpenSpec, SpecTask } from "../lib/forge";

type SpecVisualizerProps = {
  spec: OpenSpec;
};

const statusClass = (status: SpecTask["status"]) => {
  switch (status) {
    case "completed":
      return "bg-green-500/10 text-green-600 border-green-500/20";
    case "failed":
      return "bg-red-500/10 text-red-600 border-red-500/20";
    case "in_progress":
      return "bg-blue-500/10 text-blue-600 border-blue-500/20";
    default:
      return "bg-amber-500/10 text-amber-600 border-amber-500/20";
  }
};

const statusDotClass = (status: SpecTask["status"]) => {
  switch (status) {
    case "completed":
      return "bg-green-500";
    case "failed":
      return "bg-red-500";
    case "in_progress":
      return "bg-blue-500";
    default:
      return "bg-amber-500";
  }
};

export default function SpecVisualizer(props: SpecVisualizerProps) {
  const designText = () =>
    props.spec.design ? JSON.stringify(props.spec.design, null, 2) : null;

  return (
    <div class="space-y-4">
      <div class="bg-background p-4 sm:p-5 rounded-xl border border-border grid gap-4 sm:grid-cols-2 shadow-[0_1px_0_0_rgba(15,23,42,0.04)]">
        <div>
          <div class="text-xs text-muted-foreground uppercase tracking-wider mb-1">Project</div>
          <div class="font-medium">{props.spec.project_name}</div>
          <div class="text-xs text-muted-foreground mt-1">Spec v{props.spec.spec_version}</div>
        </div>
        <div>
          <div class="text-xs text-muted-foreground uppercase tracking-wider mb-1">Scope</div>
          <div class="text-sm font-medium text-foreground">
            {props.spec.requirement.summary}
          </div>
          <div class="text-xs text-muted-foreground mt-1">
            {props.spec.tasks?.length ?? 0} task(s) proposed
          </div>
        </div>
      </div>

      <details open class="rounded-xl border border-border bg-background overflow-hidden">
        <summary class="cursor-pointer px-4 py-2.5 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Requirements
        </summary>
        <div class="px-4 pb-4 pt-1.5 text-sm space-y-2">
          <div class="font-medium">{props.spec.requirement.summary}</div>
          <div class="text-muted-foreground">{props.spec.requirement.description}</div>
          <Show when={props.spec.requirement.acceptance_criteria?.length}>
            <div class="pt-2">
              <div class="text-xs text-muted-foreground uppercase tracking-wider mb-2">
                Acceptance criteria
              </div>
              <ul class="list-disc pl-5 text-xs text-muted-foreground space-y-1">
                <For each={props.spec.requirement.acceptance_criteria}>
                  {(item) => <li>{item}</li>}
                </For>
              </ul>
            </div>
          </Show>
        </div>
      </details>

      <details open class="rounded-xl border border-border bg-background overflow-hidden">
        <summary class="cursor-pointer px-4 py-2.5 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Tasks
        </summary>
        <div class="px-4 pb-4 pt-1.5 space-y-2">
          <Show
            when={props.spec.tasks?.length}
            fallback={<div class="text-xs text-muted-foreground">No tasks yet.</div>}
          >
            <div class="flex flex-col gap-3">
              <For each={props.spec.tasks}>
                {(task) => (
                  <div class="border border-border rounded-xl p-3.5 flex items-start justify-between gap-3 bg-background/70 shadow-[0_1px_0_0_rgba(15,23,42,0.04)]">
                    <div class="flex items-start gap-3">
                      <span class={`mt-1 h-2.5 w-2.5 rounded-full ${statusDotClass(task.status)}`} />
                      <div class="space-y-1">
                        <div class="text-sm font-medium">{task.title}</div>
                        <div class="text-xs text-muted-foreground">{task.description}</div>
                      </div>
                    </div>
                    <span
                      class={`text-[10px] uppercase tracking-wider px-2.5 py-1 rounded-full border ${statusClass(
                        task.status
                      )}`}
                    >
                      {task.status.replace("_", " ")}
                    </span>
                  </div>
                )}
              </For>
            </div>
          </Show>
        </div>
      </details>

      <details class="rounded-xl border border-border bg-background overflow-hidden">
        <summary class="cursor-pointer px-4 py-2.5 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Design
        </summary>
        <div class="px-4 pb-4 pt-1.5">
          <Show
            when={designText()}
            fallback={<div class="text-xs text-muted-foreground">No design details yet.</div>}
          >
            <pre class="text-xs text-muted-foreground whitespace-pre-wrap break-words bg-sidebar-accent/10 border border-border rounded-md p-2.5">
              {designText()}
            </pre>
          </Show>
        </div>
      </details>
    </div>
  );
}
