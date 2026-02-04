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
          <div class="text-xs text-muted-foreground uppercase tracking-wider mb-1">项目</div>
          <div class="font-medium">{props.spec.project_name}</div>
          <div class="text-xs text-muted-foreground mt-1">规范 v{props.spec.spec_version}</div>
        </div>
        <div>
          <div class="text-xs text-muted-foreground uppercase tracking-wider mb-1">开发计划</div>
          <div class="text-sm font-medium text-foreground">
            {props.spec.tasks?.length ?? 0} 个实现任务
          </div>
          <div class="text-xs text-muted-foreground mt-1">
            准备进入开发流程
          </div>
        </div>
      </div>

      <details open class="rounded-xl border border-border bg-background overflow-hidden">
        <summary class="cursor-pointer px-4 py-2.5 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          技术规范
        </summary>
        <div class="px-4 pb-4 pt-1.5 text-sm space-y-3">
          <div class="grid gap-3 sm:grid-cols-2">
            <div class="p-3 rounded-lg bg-blue-50/50 border border-blue-200/50">
              <div class="text-xs font-semibold text-blue-700 uppercase tracking-wider mb-1">
                需求概要
              </div>
              <div class="text-sm text-blue-900">{props.spec.requirement.summary}</div>
            </div>
            <div class="p-3 rounded-lg bg-green-50/50 border border-green-200/50">
              <div class="text-xs font-semibold text-green-700 uppercase tracking-wider mb-1">
                实现状态
              </div>
              <div class="text-sm text-green-900">
                {props.spec.tasks?.filter(t => t.status === 'completed').length ?? 0} / {props.spec.tasks?.length ?? 0} 已完成
              </div>
            </div>
          </div>
          <Show when={props.spec.requirement.acceptance_criteria?.length}>
            <div class="pt-2">
              <div class="text-xs text-muted-foreground uppercase tracking-wider mb-2">
                验收标准
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
          实现计划
        </summary>
        <div class="px-4 pb-4 pt-1.5 space-y-3">
          <Show
            when={props.spec.tasks?.length}
            fallback={<div class="text-xs text-muted-foreground">实现计划将自动生成。</div>}
          >
            <div class="grid gap-2 text-xs text-muted-foreground mb-3">
              <div class="flex justify-between">
                <span>总任务数：</span>
                <span class="font-medium">{props.spec.tasks?.length ?? 0}</span>
              </div>
              <div class="flex justify-between">
                <span>已完成：</span>
                <span class="font-medium text-green-600">{props.spec.tasks?.filter(t => t.status === 'completed').length ?? 0}</span>
              </div>
              <div class="flex justify-between">
                <span>进行中：</span>
                <span class="font-medium text-blue-600">{props.spec.tasks?.filter(t => t.status === 'in_progress').length ?? 0}</span>
              </div>
              <div class="flex justify-between">
                <span>待处理：</span>
                <span class="font-medium text-amber-600">{props.spec.tasks?.filter(t => t.status === 'pending').length ?? 0}</span>
              </div>
            </div>
            <div class="flex flex-col gap-2">
              <For each={props.spec.tasks}>
                {(task, index) => (
                  <div class="border border-border rounded-lg p-3 flex items-start gap-3 bg-background/70">
                    <div class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-xs font-semibold text-gray-600 mt-0.5">
                      {index() + 1}
                    </div>
                    <div class="flex-1 space-y-1">
                      <div class="flex items-start justify-between gap-2">
                        <div class="text-sm font-medium">{task.title}</div>
                        <span class={`text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-full border ${statusClass(task.status)}`}>
                          {task.status === 'pending' ? '待处理' :
                           task.status === 'in_progress' ? '进行中' :
                           task.status === 'completed' ? '已完成' :
                           task.status === 'failed' ? '失败' :
                           task.status}
                        </span>
                      </div>
                      <div class="text-xs text-muted-foreground">{task.description}</div>
                    </div>
                  </div>
                )}
              </For>
            </div>
          </Show>
        </div>
      </details>

      <details class="rounded-xl border border-border bg-background overflow-hidden">
        <summary class="cursor-pointer px-4 py-2.5 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          技术架构
        </summary>
        <div class="px-4 pb-4 pt-1.5">
          <Show
            when={designText()}
            fallback={
              <div class="space-y-3">
                <div class="text-xs text-muted-foreground">架构设计将基于需求自动生成。</div>
                <div class="grid gap-3 sm:grid-cols-2">
                  <div class="p-3 rounded-lg bg-purple-50/50 border border-purple-200/50">
                    <div class="text-xs font-semibold text-purple-700 uppercase tracking-wider mb-1">
                      技术栈
                    </div>
                    <div class="text-xs text-purple-900">由智能工坊引擎确定</div>
                  </div>
                  <div class="p-3 rounded-lg bg-orange-50/50 border border-orange-200/50">
                    <div class="text-xs font-semibold text-orange-700 uppercase tracking-wider mb-1">
                      架构模式
                    </div>
                    <div class="text-xs text-orange-900">将进行分析并提出建议</div>
                  </div>
                </div>
              </div>
            }
          >
            <div class="space-y-3">
              <div class="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
                设计规范
              </div>
              <pre class="text-xs text-muted-foreground whitespace-pre-wrap break-words bg-sidebar-accent/10 border border-border rounded-md p-2.5 max-h-64 overflow-y-auto">
                {designText()}
              </pre>
            </div>
          </Show>
        </div>
      </details>
    </div>
  );
}
