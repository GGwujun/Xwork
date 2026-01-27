
import { createSignal, onMount, Show, For } from "solid-js";
import { generateSpec, checkForgeHealth, SpecRequirement, OpenSpec } from "../lib/forge";
import { t } from "../../i18n";
import { Loader2, CheckCircle2, AlertCircle } from "lucide-solid";

export default function ForgeView() {
  const [healthy, setHealthy] = createSignal(false);
  const [loading, setLoading] = createSignal(false);
  const [spec, setSpec] = createSignal<OpenSpec | null>(null);
  const [requirement, setRequirement] = createSignal({ summary: "", description: "" });

  onMount(async () => {
    setHealthy(await checkForgeHealth());
  });

  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    setLoading(true);
    try {
      const result = await generateSpec({
        ...requirement(),
        acceptance_criteria: []
      });
      setSpec(result);
    } catch (err) {
      console.error(err);
      alert("Failed to generate Spec");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div class="flex flex-col h-full w-full max-w-4xl mx-auto p-6 gap-6">
      <div class="flex items-center justify-between">
        <h1 class="text-2xl font-bold">Enterprise Forge</h1>
        <div class="flex items-center gap-2 text-sm">
          Status: 
          <span class={healthy() ? "text-green-500 font-medium" : "text-red-500 font-medium"}>
           {healthy() ? "Connected" : "Disconnected"}
          </span>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 h-full">
        {/* Input Column */}
        <div class="flex flex-col gap-4">
          <div class="bg-sidebar-accent/10 p-4 rounded-lg border border-border">
            <h2 class="font-semibold mb-4">New Requirement</h2>
            <form onSubmit={handleSubmit} class="flex flex-col gap-4">
              <div class="flex flex-col gap-2">
                <label class="text-sm font-medium">Summary</label>
                <input 
                  type="text" 
                  class="bg-background border border-border rounded p-2"
                  value={requirement().summary}
                  onInput={(e) => setRequirement({...requirement(), summary: e.currentTarget.value})}
                  required
                />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-sm font-medium">Description</label>
                <textarea 
                  class="bg-background border border-border rounded p-2 min-h-[150px]"
                  value={requirement().description}
                  onInput={(e) => setRequirement({...requirement(), description: e.currentTarget.value})}
                  required
                />
              </div>
              <button 
                type="submit" 
                class="bg-primary text-primary-foreground py-2 px-4 rounded hover:opacity-90 disabled:opacity-50 flex items-center justify-center gap-2"
                disabled={loading() || !healthy()}
              >
                {loading() ? <Loader2 class="animate-spin h-4 w-4"/> : "Generate Spec"}
              </button>
            </form>
          </div>
        </div>

        {/* Output Column */}
        <div class="flex flex-col gap-4 h-full overflow-hidden">
          <div class="bg-sidebar-accent/10 p-4 rounded-lg border border-border h-full overflow-y-auto">
            <h2 class="font-semibold mb-4">OpenSpec Contract</h2>
            <Show when={spec()} fallback={<div class="text-muted-foreground text-sm">Generated spec will appear here...</div>}>
              <div class="space-y-4">
                <div class="bg-background p-3 rounded border border-border">
                  <div class="text-xs text-muted-foreground uppercase tracking-wider mb-1">Project</div>
                  <div class="font-medium">{spec()?.project_name}</div>
                </div>
                
                <div>
                  <div class="text-xs text-muted-foreground uppercase tracking-wider mb-2">Requirements</div>
                  <div class="bg-background p-3 rounded border border-border text-sm">
                    <p class="font-medium mb-1">{spec()?.requirement.summary}</p>
                    <p class="text-muted-foreground">{spec()?.requirement.description}</p>
                  </div>
                </div>

                <div>
                  <div class="text-xs text-muted-foreground uppercase tracking-wider mb-2">Tasks</div>
                  <div class="flex flex-col gap-2">
                    <For each={spec()?.tasks}>
                      {(task) => (
                        <div class="bg-background p-3 rounded border border-border flex items-start gap-3">
                          <Show when={task.status === "completed"} fallback={<AlertCircle class="h-4 w-4 text-yellow-500 mt-1"/>}>
                            <CheckCircle2 class="h-4 w-4 text-green-500 mt-1"/>
                          </Show>
                          <div>
                            <div class="text-sm font-medium">{task.title}</div>
                            <div class="text-xs text-muted-foreground">{task.description}</div>
                          </div>
                        </div>
                      )}
                    </For>
                  </div>
                </div>
              </div>
            </Show>
          </div>
        </div>
      </div>
    </div>
  );
}
