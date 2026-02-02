
import { createSignal, onMount, Show, createEffect } from "solid-js";
import { useNavigate } from "@solidjs/router";
import { generateSpec, checkForgeHealth, getSpecLifecycle, OpenSpec, LifecycleInfo } from "../lib/forge";
import { Loader2, History, GitBranch, Download, Workflow } from "lucide-solid";
import Button from "../components/button";
import SpecVisualizer from "../components/spec-visualizer";
import SpecApprovalWorkflow from "../components/spec-approval-workflow";
import SpecExportModal from "../components/spec-export-modal";

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null;

const isOpenSpec = (value: unknown): value is OpenSpec => {
  if (!isRecord(value)) return false;
  const requirement = value.requirement;
  const tasks = value.tasks;
  if (!isRecord(requirement)) return false;
  if (typeof requirement.summary !== "string") return false;
  if (!Array.isArray(tasks)) return false;
  return true;
};

export default function ForgeView() {
  const navigate = useNavigate();
  const [healthy, setHealthy] = createSignal(false);
  const [loading, setLoading] = createSignal(false);
  const [spec, setSpec] = createSignal<OpenSpec | null>(null);
  const [requirement, setRequirement] = createSignal({ summary: "", description: "" });
  const [requirementId, setRequirementId] = createSignal<string | null>(null);
  const [lifecycle, setLifecycle] = createSignal<LifecycleInfo | null>(null);
  const [showExportModal, setShowExportModal] = createSignal(false);

  onMount(async () => {
    setHealthy(await checkForgeHealth());
  });

  // Load lifecycle info when spec is generated
  createEffect(() => {
    const id = requirementId();
    if (id) {
      loadLifecycle(id);
    }
  });

  const loadLifecycle = async (id: string) => {
    try {
      const data = await getSpecLifecycle(id);
      setLifecycle(data);
    } catch (err) {
      console.error("Failed to load lifecycle:", err);
    }
  };

  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    setLoading(true);
    try {
      const result = await generateSpec({
        ...requirement(),
        acceptance_criteria: []
      });
      setSpec(result);
      // Generate a requirement ID (in real implementation, this would come from backend)
      const id = `REQ-${Date.now()}`;
      setRequirementId(id);
    } catch (err) {
      console.error(err);
      alert("Failed to generate Spec");
    } finally {
      setLoading(false);
    }
  };

  const handleLifecycleChange = () => {
    const id = requirementId();
    if (id) {
      loadLifecycle(id);
    }
  };

  return (
    <div class="relative flex flex-col h-full w-full  mx-auto px-4 sm:px-6 lg:px-8 py-6 gap-8">
      <div class="pointer-events-none absolute -top-24 right-6 h-40 w-40 rounded-full bg-gradient-to-br from-gray-2/80 via-gray-1/40 to-transparent blur-2xl" />
      <div class="pointer-events-none absolute top-32 left-0 h-28 w-28 rounded-full bg-gradient-to-tr from-gray-2/70 via-gray-1/30 to-transparent blur-2xl" />

      <div class="relative flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="space-y-2">
          <div class="text-xs font-semibold text-gray-10 uppercase tracking-[0.18em]">Forge</div>
          <h1 class="text-2xl sm:text-3xl font-semibold text-gray-12">Enterprise Forge</h1>
          <p class="text-sm text-gray-10 max-w-xl">
            Turn a requirement into an OpenSpec contract you can edit and validate in real time.
          </p>
        </div>
        <div class="flex items-center gap-2 rounded-full border border-gray-6/60 bg-gray-2/50 px-3 py-1 text-xs font-semibold text-gray-11">
          <span
            class={`h-2 w-2 rounded-full ${
              healthy() ? "bg-green-9" : "bg-red-9"
            } shadow-[0_0_0_3px_rgba(0,0,0,0.04)]`}
          />
          <span>{healthy() ? "Forge connected" : "Forge offline"}</span>
        </div>
      </div>

      <div class="grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.1fr)]">
        {/* Input Column */}
        <div class="flex flex-col gap-4">
          <div class="rounded-2xl border border-gray-6/60 bg-gray-1/40 p-5 sm:p-6 shadow-[0_1px_0_0_rgba(16,24,40,0.04)]">
            <div class="flex items-start justify-between gap-3 mb-4">
              <div>
                <div class="text-xs font-semibold text-gray-11 uppercase tracking-wider">
                  New requirement
                </div>
                <div class="text-sm text-gray-10 mt-1">
                  Capture the summary and intent for the Forge engine.
                </div>
              </div>
              <div
                class={`rounded-full border px-2.5 py-1 text-[11px] font-semibold ${
                  healthy()
                    ? "border-green-7/40 bg-green-7/10 text-green-11"
                    : "border-red-7/40 bg-red-7/10 text-red-11"
                }`}
              >
                {healthy() ? "Engine ready" : "Engine offline"}
              </div>
            </div>
            <form onSubmit={handleSubmit} class="flex flex-col gap-4">
              <div class="flex flex-col gap-2">
                <label class="text-xs font-semibold text-gray-11 uppercase tracking-wider">Summary</label>
                <input
                  type="text"
                  class="h-11 rounded-xl bg-gray-1/60 border border-gray-6/60 px-3 text-sm text-gray-12 placeholder:text-gray-9 focus:border-gray-7 focus:ring-2 focus:ring-gray-6/20"
                  value={requirement().summary}
                  onInput={(e) =>
                    setRequirement({ ...requirement(), summary: e.currentTarget.value })
                  }
                  placeholder="e.g. Streamline monthly reporting for operations"
                  required
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-xs font-semibold text-gray-11 uppercase tracking-wider">Description</label>
                <textarea
                  class="rounded-xl bg-gray-1/60 border border-gray-6/60 px-3 py-2 text-sm text-gray-12 placeholder:text-gray-9 focus:border-gray-7 focus:ring-2 focus:ring-gray-6/20 min-h-[160px]"
                  value={requirement().description}
                  onInput={(e) =>
                    setRequirement({
                      ...requirement(),
                      description: e.currentTarget.value
                    })
                  }
                  placeholder="Describe the scope, constraints, and expected outcomes in plain language."
                  required
                />
              </div>
              <div class="flex items-center justify-between gap-3">
                <div class="text-xs text-gray-9">
                  {healthy()
                    ? "Ready to generate an OpenSpec contract."
                    : "Forge must be online to generate a spec."}
                </div>
                <Button type="submit" disabled={loading() || !healthy()}>
                  {loading() ? <Loader2 class="animate-spin h-4 w-4" /> : "Generate Spec"}
                </Button>
              </div>
            </form>
          </div>
        </div>

        {/* Output Column */}
        <div class="flex flex-col gap-4 h-full overflow-hidden">
          <div class="rounded-2xl border border-gray-6/60 bg-gray-1/40 p-5 sm:p-6 h-full overflow-y-auto shadow-[0_1px_0_0_rgba(16,24,40,0.04)]">
            <div class="flex items-start justify-between gap-3 mb-4">
              <div>
                <div class="text-xs font-semibold text-gray-11 uppercase tracking-wider">
                  OpenSpec contract
                </div>
                <div class="text-sm text-gray-10 mt-1">
                  Preview the tasks Forge proposes.
                </div>
              </div>
              {/* Action Buttons */}
              <Show when={spec() && requirementId()}>
                <div class="flex items-center gap-2">
                  <button
                    onClick={() => navigate(`/spec/${requirementId()}/versions`)}
                    class="p-2 hover:bg-gray-3 rounded-lg transition-colors"
                    title="Version History"
                  >
                    <History class="w-4 h-4 text-gray-11" />
                  </button>
                  <button
                    onClick={() => navigate(`/spec/${requirementId()}/lifecycle`)}
                    class="p-2 hover:bg-gray-3 rounded-lg transition-colors"
                    title="Lifecycle Management"
                  >
                    <Workflow class="w-4 h-4 text-gray-11" />
                  </button>
                  <button
                    onClick={() => setShowExportModal(true)}
                    class="p-2 hover:bg-gray-3 rounded-lg transition-colors"
                    title="Export Spec"
                  >
                    <Download class="w-4 h-4 text-gray-11" />
                  </button>
                </div>
              </Show>
            </div>
            <Show
              when={spec()}
              fallback={
                <div class="text-sm text-gray-9 border border-dashed border-gray-6/60 rounded-xl px-4 py-6">
                  Generated OpenSpec will appear here once Forge completes the run.
                </div>
              }
            >
              <div class="flex flex-col gap-5">
                {/* Lifecycle Status Badge */}
                <Show when={lifecycle()}>
                  <div class="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-2/50 border border-gray-6/60">
                    <div class={`w-2 h-2 rounded-full ${
                      lifecycle()!.current_status === "draft" ? "bg-blue-9" :
                      lifecycle()!.current_status === "review" ? "bg-yellow-9" :
                      lifecycle()!.current_status === "approved" ? "bg-green-9" :
                      "bg-gray-9"
                    }`} />
                    <span class="text-xs font-semibold text-gray-11 uppercase tracking-wider">
                      Status: {lifecycle()!.current_status}
                    </span>
                    <Show when={lifecycle()!.current_version !== null}>
                      <span class="text-xs text-gray-9">
                        • v{lifecycle()!.current_version}
                      </span>
                    </Show>
                  </div>
                </Show>

                <div class="rounded-xl border border-gray-6/60 bg-gray-1/30 p-4 sm:p-5 space-y-3">
                  <div class="flex items-center justify-between border-b border-gray-6/50 pb-2">
                    <div class="text-xs font-semibold text-gray-11 uppercase tracking-wider">
                      Forge preview
                    </div>
                    <div class="text-xs text-gray-9">
                      {(spec() as OpenSpec).tasks?.length ?? 0} task(s)
                    </div>
                  </div>
                  <SpecVisualizer spec={spec() as OpenSpec} />
                </div>

                {/* Approval Workflow */}
                <Show when={requirementId() && lifecycle()}>
                  <SpecApprovalWorkflow
                    requirementId={requirementId()!}
                    currentStatus={lifecycle()!.current_status}
                    onStatusChange={handleLifecycleChange}
                  />
                </Show>
              </div>
            </Show>
          </div>
        </div>
      </div>

      {/* Export Modal */}
      <SpecExportModal
        spec={spec()}
        isOpen={showExportModal()}
        onClose={() => setShowExportModal(false)}
      />
    </div>
  );
}
