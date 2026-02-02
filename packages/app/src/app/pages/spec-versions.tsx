import { createSignal, onMount, Show, For } from "solid-js";
import { useParams, useNavigate } from "@solidjs/router";
import { listSpecVersions, getSpecVersion, compareVersions, rollbackToVersion, VersionMetadata, OpenSpec } from "../lib/forge";
import { Loader2, Eye, GitCompare, RotateCcw, Archive, AlertCircle } from "lucide-solid";
import Button from "../components/button";

export default function SpecVersionsView() {
  const params = useParams<{ requirementId: string }>();
  const navigate = useNavigate();

  const [versions, setVersions] = createSignal<VersionMetadata[]>([]);
  const [loading, setLoading] = createSignal(true);
  const [error, setError] = createSignal<string | null>(null);
  const [selectedVersion, setSelectedVersion] = createSignal<OpenSpec | null>(null);
  const [showDetails, setShowDetails] = createSignal(false);
  const [compareMode, setCompareMode] = createSignal(false);
  const [selectedVersions, setSelectedVersions] = createSignal<number[]>([]);
  const [rollbackConfirm, setRollbackConfirm] = createSignal<number | null>(null);
  const [actionLoading, setActionLoading] = createSignal(false);

  onMount(async () => {
    await loadVersions();
  });

  const loadVersions = async () => {
    setLoading(true);
    setError(null);
    try {
      const versionList = await listSpecVersions(params.requirementId);
      setVersions(versionList);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load versions");
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = async (version: number) => {
    setActionLoading(true);
    try {
      const spec = await getSpecVersion(params.requirementId, version);
      setSelectedVersion(spec);
      setShowDetails(true);
    } catch (err) {
      alert(`Failed to load version ${version}: ${err instanceof Error ? err.message : "Unknown error"}`);
    } finally {
      setActionLoading(false);
    }
  };

  const handleCompare = () => {
    if (selectedVersions().length !== 2) {
      alert("Please select exactly 2 versions to compare");
      return;
    }
    const [v1, v2] = selectedVersions().sort((a, b) => a - b);
    navigate(`/spec/${params.requirementId}/compare?v1=${v1}&v2=${v2}`);
  };

  const handleRollback = async (version: number) => {
    setActionLoading(true);
    try {
      await rollbackToVersion(params.requirementId, version);
      alert(`Successfully rolled back to version ${version}`);
      setRollbackConfirm(null);
      await loadVersions();
    } catch (err) {
      alert(`Failed to rollback: ${err instanceof Error ? err.message : "Unknown error"}`);
    } finally {
      setActionLoading(false);
    }
  };

  const toggleVersionSelection = (version: number) => {
    const current = selectedVersions();
    if (current.includes(version)) {
      setSelectedVersions(current.filter(v => v !== version));
    } else {
      if (current.length >= 2) {
        alert("You can only select 2 versions for comparison");
        return;
      }
      setSelectedVersions([...current, version]);
    }
  };

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case "approved":
        return "bg-green-500/20 text-green-400 border-green-500/30";
      case "archived":
        return "bg-gray-500/20 text-gray-400 border-gray-500/30";
      default:
        return "bg-blue-500/20 text-blue-400 border-blue-500/30";
    }
  };

  return (
    <div class="flex flex-col h-full bg-[var(--bg-primary)] text-[var(--text-primary)]">
      {/* Header */}
      <div class="flex items-center justify-between px-6 py-4 border-b border-[var(--border-primary)]">
        <div>
          <h1 class="text-2xl font-semibold">Version Management</h1>
          <p class="text-sm text-[var(--text-secondary)] mt-1">
            Requirement ID: {params.requirementId}
          </p>
        </div>
        <div class="flex gap-2">
          <Show when={compareMode()}>
            <Button
              onClick={handleCompare}
              disabled={selectedVersions().length !== 2}
              class="flex items-center gap-2"
            >
              <GitCompare class="w-4 h-4" />
              Compare Selected ({selectedVersions().length}/2)
            </Button>
          </Show>
          <Button
            onClick={() => {
              setCompareMode(!compareMode());
              setSelectedVersions([]);
            }}
            variant={compareMode() ? "secondary" : "primary"}
          >
            {compareMode() ? "Cancel Compare" : "Compare Mode"}
          </Button>
          <Button onClick={() => navigate("/forge")} variant="secondary">
            Back to Forge
          </Button>
        </div>
      </div>

      {/* Content */}
      <div class="flex-1 overflow-auto p-6">
        <Show when={loading()}>
          <div class="flex items-center justify-center h-64">
            <Loader2 class="w-8 h-8 animate-spin text-[var(--text-secondary)]" />
          </div>
        </Show>

        <Show when={error()}>
          <div class="flex items-center gap-2 p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400">
            <AlertCircle class="w-5 h-5" />
            <span>{error()}</span>
          </div>
        </Show>

        <Show when={!loading() && !error()}>
          <Show when={versions().length === 0}>
            <div class="text-center py-12 text-[var(--text-secondary)]">
              <p>No versions found. Versions are created after approval.</p>
            </div>
          </Show>

          <Show when={versions().length > 0}>
            <div class="bg-[var(--bg-secondary)] rounded-lg border border-[var(--border-primary)] overflow-hidden">
              <table class="w-full">
                <thead class="bg-[var(--bg-tertiary)] border-b border-[var(--border-primary)]">
                  <tr>
                    <Show when={compareMode()}>
                      <th class="px-4 py-3 text-left text-sm font-medium">Select</th>
                    </Show>
                    <th class="px-4 py-3 text-left text-sm font-medium">Version</th>
                    <th class="px-4 py-3 text-left text-sm font-medium">Status</th>
                    <th class="px-4 py-3 text-left text-sm font-medium">Created At</th>
                    <th class="px-4 py-3 text-left text-sm font-medium">Approver</th>
                    <th class="px-4 py-3 text-left text-sm font-medium">Approval Time</th>
                    <th class="px-4 py-3 text-left text-sm font-medium">Change Summary</th>
                    <th class="px-4 py-3 text-right text-sm font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <For each={versions()}>
                    {(version) => (
                      <tr class="border-b border-[var(--border-primary)] hover:bg-[var(--bg-tertiary)] transition-colors">
                        <Show when={compareMode()}>
                          <td class="px-4 py-3">
                            <input
                              type="checkbox"
                              checked={selectedVersions().includes(version.version)}
                              onChange={() => toggleVersionSelection(version.version)}
                              class="w-4 h-4 rounded border-[var(--border-primary)] bg-[var(--bg-primary)] text-blue-500 focus:ring-2 focus:ring-blue-500"
                            />
                          </td>
                        </Show>
                        <td class="px-4 py-3 font-mono text-sm">v{version.version}</td>
                        <td class="px-4 py-3">
                          <span class={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${getStatusBadgeClass(version.status)}`}>
                            {version.status}
                          </span>
                        </td>
                        <td class="px-4 py-3 text-sm text-[var(--text-secondary)]">
                          {new Date(version.created_at).toLocaleString()}
                        </td>
                        <td class="px-4 py-3 text-sm">{version.approver}</td>
                        <td class="px-4 py-3 text-sm text-[var(--text-secondary)]">
                          {new Date(version.approval_time).toLocaleString()}
                        </td>
                        <td class="px-4 py-3 text-sm text-[var(--text-secondary)] max-w-xs truncate">
                          {version.change_summary || "—"}
                        </td>
                        <td class="px-4 py-3">
                          <div class="flex items-center justify-end gap-2">
                            <button
                              onClick={() => handleViewDetails(version.version)}
                              disabled={actionLoading()}
                              class="p-1.5 hover:bg-[var(--bg-primary)] rounded transition-colors"
                              title="View Details"
                            >
                              <Eye class="w-4 h-4" />
                            </button>
                            <button
                              onClick={() => setRollbackConfirm(version.version)}
                              disabled={actionLoading()}
                              class="p-1.5 hover:bg-[var(--bg-primary)] rounded transition-colors text-orange-400"
                              title="Rollback to this version"
                            >
                              <RotateCcw class="w-4 h-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    )}
                  </For>
                </tbody>
              </table>
            </div>
          </Show>
        </Show>
      </div>

      {/* Version Details Modal */}
      <Show when={showDetails() && selectedVersion()}>
        <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setShowDetails(false)}>
          <div class="bg-[var(--bg-secondary)] rounded-lg border border-[var(--border-primary)] w-full max-w-4xl max-h-[80vh] overflow-hidden" onClick={(e) => e.stopPropagation()}>
            <div class="flex items-center justify-between px-6 py-4 border-b border-[var(--border-primary)]">
              <h2 class="text-xl font-semibold">Version Details</h2>
              <button onClick={() => setShowDetails(false)} class="text-[var(--text-secondary)] hover:text-[var(--text-primary)]">
                ✕
              </button>
            </div>
            <div class="p-6 overflow-auto max-h-[calc(80vh-80px)]">
              <pre class="bg-[var(--bg-primary)] p-4 rounded-lg border border-[var(--border-primary)] overflow-x-auto text-sm">
                {JSON.stringify(selectedVersion(), null, 2)}
              </pre>
            </div>
          </div>
        </div>
      </Show>

      {/* Rollback Confirmation Modal */}
      <Show when={rollbackConfirm() !== null}>
        <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div class="bg-[var(--bg-secondary)] rounded-lg border border-[var(--border-primary)] w-full max-w-md p-6">
            <div class="flex items-start gap-3 mb-4">
              <AlertCircle class="w-6 h-6 text-orange-400 flex-shrink-0 mt-0.5" />
              <div>
                <h3 class="text-lg font-semibold mb-2">Confirm Rollback</h3>
                <p class="text-sm text-[var(--text-secondary)]">
                  Are you sure you want to rollback to version {rollbackConfirm()}? This will restore the OpenSpec to this version's state.
                </p>
              </div>
            </div>
            <div class="flex gap-2 justify-end">
              <Button onClick={() => setRollbackConfirm(null)} variant="secondary" disabled={actionLoading()}>
                Cancel
              </Button>
              <Button
                onClick={() => handleRollback(rollbackConfirm()!)}
                disabled={actionLoading()}
                class="bg-orange-500 hover:bg-orange-600"
              >
                <Show when={actionLoading()} fallback="Confirm Rollback">
                  <Loader2 class="w-4 h-4 animate-spin" />
                </Show>
              </Button>
            </div>
          </div>
        </div>
      </Show>
    </div>
  );
}
