import { createSignal, onMount, Show, For } from "solid-js";
import { useParams, useNavigate } from "@solidjs/router";
import { getSpecLifecycle, submitForReview, approveSpec, rejectSpec, archiveSpec, getLatestSpecVersion, LifecycleInfo, OpenSpec, SpecStatus } from "../lib/forge";
import { Loader2, CheckCircle, Clock, Archive, XCircle, AlertCircle, ArrowRight } from "lucide-solid";
import Button from "../components/button";

export default function SpecLifecycleView() {
  const params = useParams<{ requirementId: string }>();
  const navigate = useNavigate();

  const [lifecycle, setLifecycle] = createSignal<LifecycleInfo | null>(null);
  const [loading, setLoading] = createSignal(true);
  const [error, setError] = createSignal<string | null>(null);
  const [actionLoading, setActionLoading] = createSignal(false);
  const [showApprovalDialog, setShowApprovalDialog] = createSignal(false);
  const [approvalAction, setApprovalAction] = createSignal<"approve" | "reject" | null>(null);
  const [approvalReason, setApprovalReason] = createSignal("");
  const [approverName, setApproverName] = createSignal("");

  onMount(async () => {
    await loadLifecycle();
  });

  const loadLifecycle = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getSpecLifecycle(params.requirementId);
      setLifecycle(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load lifecycle");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitForReview = async () => {
    setActionLoading(true);
    try {
      await submitForReview(params.requirementId, "current-user", "Ready for review");
      alert("Successfully submitted for review");
      await loadLifecycle();
    } catch (err) {
      alert(`Failed to submit: ${err instanceof Error ? err.message : "Unknown error"}`);
    } finally {
      setActionLoading(false);
    }
  };

  const handleApprovalAction = async () => {
    if (!approverName().trim()) {
      alert("Please enter approver name");
      return;
    }

    setActionLoading(true);
    try {
      if (approvalAction() === "approve") {
        // Get latest spec data for approval
        const specData = await getLatestSpecVersion(params.requirementId);
        await approveSpec(params.requirementId, approverName(), specData, approvalReason());
        alert("Successfully approved");
      } else if (approvalAction() === "reject") {
        await rejectSpec(params.requirementId, approverName(), approvalReason());
        alert("Successfully rejected");
      }
      setShowApprovalDialog(false);
      setApprovalReason("");
      setApproverName("");
      await loadLifecycle();
    } catch (err) {
      alert(`Failed to ${approvalAction()}: ${err instanceof Error ? err.message : "Unknown error"}`);
    } finally {
      setActionLoading(false);
    }
  };

  const handleArchive = async () => {
    if (!confirm("Are you sure you want to archive this spec?")) {
      return;
    }

    setActionLoading(true);
    try {
      await archiveSpec(params.requirementId, "current-user", "Development completed");
      alert("Successfully archived");
      await loadLifecycle();
    } catch (err) {
      alert(`Failed to archive: ${err instanceof Error ? err.message : "Unknown error"}`);
    } finally {
      setActionLoading(false);
    }
  };

  const getStatusIcon = (status: SpecStatus) => {
    switch (status) {
      case "draft":
        return <Clock class="w-5 h-5 text-blue-400" />;
      case "review":
        return <AlertCircle class="w-5 h-5 text-yellow-400" />;
      case "approved":
        return <CheckCircle class="w-5 h-5 text-green-400" />;
      case "archived":
        return <Archive class="w-5 h-5 text-gray-400" />;
      default:
        return <Clock class="w-5 h-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status: SpecStatus) => {
    switch (status) {
      case "draft":
        return "text-blue-400 bg-blue-500/20 border-blue-500/30";
      case "review":
        return "text-yellow-400 bg-yellow-500/20 border-yellow-500/30";
      case "approved":
        return "text-green-400 bg-green-500/20 border-green-500/30";
      case "archived":
        return "text-gray-400 bg-gray-500/20 border-gray-500/30";
      default:
        return "text-gray-400 bg-gray-500/20 border-gray-500/30";
    }
  };

  const getAvailableActions = (status: SpecStatus) => {
    switch (status) {
      case "draft":
        return [{ label: "Submit for Review", action: handleSubmitForReview, variant: "primary" as const }];
      case "review":
        return [
          { label: "Approve", action: () => { setApprovalAction("approve"); setShowApprovalDialog(true); }, variant: "primary" as const },
          { label: "Reject", action: () => { setApprovalAction("reject"); setShowApprovalDialog(true); }, variant: "secondary" as const }
        ];
      case "approved":
        return [{ label: "Archive", action: handleArchive, variant: "secondary" as const }];
      case "archived":
        return [];
      default:
        return [];
    }
  };

  return (
    <div class="flex flex-col h-full bg-[var(--bg-primary)] text-[var(--text-primary)]">
      {/* Header */}
      <div class="flex items-center justify-between px-6 py-4 border-b border-[var(--border-primary)]">
        <div>
          <h1 class="text-2xl font-semibold">Lifecycle Management</h1>
          <p class="text-sm text-[var(--text-secondary)] mt-1">
            Requirement ID: {params.requirementId}
          </p>
        </div>
        <Button onClick={() => navigate("/forge")} variant="secondary">
          Back to Forge
        </Button>
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

        <Show when={!loading() && !error() && lifecycle()}>
          <div class="space-y-6">
            {/* Current Status Card */}
            <div class="bg-[var(--bg-secondary)] rounded-lg border border-[var(--border-primary)] p-6">
              <h2 class="text-lg font-semibold mb-4">Current Status</h2>
              <div class="flex items-center gap-4 mb-6">
                {getStatusIcon(lifecycle()!.current_status)}
                <div class="flex-1">
                  <div class={`inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium border ${getStatusColor(lifecycle()!.current_status)}`}>
                    {lifecycle()!.current_status.toUpperCase()}
                  </div>
                  <Show when={lifecycle()!.current_version !== null}>
                    <p class="text-sm text-[var(--text-secondary)] mt-2">
                      Current Version: v{lifecycle()!.current_version}
                    </p>
                  </Show>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p class="text-[var(--text-secondary)]">Created At</p>
                  <p class="font-medium mt-1">{new Date(lifecycle()!.created_at).toLocaleString()}</p>
                </div>
                <div>
                  <p class="text-[var(--text-secondary)]">Last Updated</p>
                  <p class="font-medium mt-1">{new Date(lifecycle()!.updated_at).toLocaleString()}</p>
                </div>
              </div>

              {/* Available Actions */}
              <Show when={getAvailableActions(lifecycle()!.current_status).length > 0}>
                <div class="mt-6 pt-6 border-t border-[var(--border-primary)]">
                  <p class="text-sm text-[var(--text-secondary)] mb-3">Available Actions</p>
                  <div class="flex gap-2">
                    <For each={getAvailableActions(lifecycle()!.current_status)}>
                      {(action) => (
                        <Button
                          onClick={action.action}
                          variant={action.variant}
                          disabled={actionLoading()}
                        >
                          <Show when={actionLoading()} fallback={action.label}>
                            <Loader2 class="w-4 h-4 animate-spin" />
                          </Show>
                        </Button>
                      )}
                    </For>
                  </div>
                </div>
              </Show>
            </div>

            {/* Status Flow Visualization */}
            <div class="bg-[var(--bg-secondary)] rounded-lg border border-[var(--border-primary)] p-6">
              <h2 class="text-lg font-semibold mb-4">Status Flow</h2>
              <div class="flex items-center justify-between">
                <div class={`flex items-center gap-2 ${lifecycle()!.current_status === "draft" ? "opacity-100" : "opacity-50"}`}>
                  <Clock class="w-5 h-5 text-blue-400" />
                  <span class="text-sm font-medium">Draft</span>
                </div>
                <ArrowRight class="w-5 h-5 text-[var(--text-secondary)]" />
                <div class={`flex items-center gap-2 ${lifecycle()!.current_status === "review" ? "opacity-100" : "opacity-50"}`}>
                  <AlertCircle class="w-5 h-5 text-yellow-400" />
                  <span class="text-sm font-medium">Review</span>
                </div>
                <ArrowRight class="w-5 h-5 text-[var(--text-secondary)]" />
                <div class={`flex items-center gap-2 ${lifecycle()!.current_status === "approved" ? "opacity-100" : "opacity-50"}`}>
                  <CheckCircle class="w-5 h-5 text-green-400" />
                  <span class="text-sm font-medium">Approved</span>
                </div>
                <ArrowRight class="w-5 h-5 text-[var(--text-secondary)]" />
                <div class={`flex items-center gap-2 ${lifecycle()!.current_status === "archived" ? "opacity-100" : "opacity-50"}`}>
                  <Archive class="w-5 h-5 text-gray-400" />
                  <span class="text-sm font-medium">Archived</span>
                </div>
              </div>
            </div>

            {/* History Timeline */}
            <div class="bg-[var(--bg-secondary)] rounded-lg border border-[var(--border-primary)] p-6">
              <h2 class="text-lg font-semibold mb-4">Status Change History</h2>
              <Show when={lifecycle()!.history.length === 0}>
                <p class="text-sm text-[var(--text-secondary)]">No status changes yet</p>
              </Show>
              <Show when={lifecycle()!.history.length > 0}>
                <div class="space-y-4">
                  <For each={lifecycle()!.history}>
                    {(transition, index) => (
                      <div class="flex gap-4">
                        <div class="flex flex-col items-center">
                          <div class={`w-3 h-3 rounded-full ${index() === 0 ? "bg-blue-500" : "bg-[var(--border-primary)]"}`} />
                          <Show when={index() < lifecycle()!.history.length - 1}>
                            <div class="w-0.5 h-full bg-[var(--border-primary)] my-1" />
                          </Show>
                        </div>
                        <div class="flex-1 pb-4">
                          <div class="flex items-center gap-2 mb-1">
                            <span class="text-sm font-medium">
                              {transition.from_status} → {transition.to_status}
                            </span>
                            <span class="text-xs text-[var(--text-secondary)]">
                              {new Date(transition.timestamp).toLocaleString()}
                            </span>
                          </div>
                          <p class="text-sm text-[var(--text-secondary)]">
                            Operator: {transition.operator}
                          </p>
                          <Show when={transition.reason}>
                            <p class="text-sm text-[var(--text-secondary)] mt-1">
                              Reason: {transition.reason}
                            </p>
                          </Show>
                        </div>
                      </div>
                    )}
                  </For>
                </div>
              </Show>
            </div>

            {/* Version History */}
            <Show when={lifecycle()!.versions.length > 0}>
              <div class="bg-[var(--bg-secondary)] rounded-lg border border-[var(--border-primary)] p-6">
                <div class="flex items-center justify-between mb-4">
                  <h2 class="text-lg font-semibold">Version History</h2>
                  <Button onClick={() => navigate(`/spec/${params.requirementId}/versions`)} variant="secondary" size="sm">
                    View All Versions
                  </Button>
                </div>
                <div class="space-y-3">
                  <For each={lifecycle()!.versions.slice(0, 5)}>
                    {(version) => (
                      <div class="flex items-center justify-between p-3 bg-[var(--bg-primary)] rounded border border-[var(--border-primary)]">
                        <div>
                          <p class="text-sm font-medium font-mono">v{version.version}</p>
                          <p class="text-xs text-[var(--text-secondary)] mt-1">
                            {new Date(version.created_at).toLocaleString()}
                          </p>
                        </div>
                        <div class="text-right">
                          <p class="text-sm text-[var(--text-secondary)]">{version.approver}</p>
                          <Show when={version.change_summary}>
                            <p class="text-xs text-[var(--text-secondary)] mt-1 max-w-xs truncate">
                              {version.change_summary}
                            </p>
                          </Show>
                        </div>
                      </div>
                    )}
                  </For>
                </div>
              </div>
            </Show>
          </div>
        </Show>
      </div>

      {/* Approval Dialog */}
      <Show when={showApprovalDialog()}>
        <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div class="bg-[var(--bg-secondary)] rounded-lg border border-[var(--border-primary)] w-full max-w-md p-6">
            <h3 class="text-lg font-semibold mb-4">
              {approvalAction() === "approve" ? "Approve Spec" : "Reject Spec"}
            </h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium mb-2">Approver Name</label>
                <input
                  type="text"
                  value={approverName()}
                  onInput={(e) => setApproverName(e.currentTarget.value)}
                  placeholder="Enter your name"
                  class="w-full px-3 py-2 bg-[var(--bg-primary)] border border-[var(--border-primary)] rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium mb-2">Reason (Optional)</label>
                <textarea
                  value={approvalReason()}
                  onInput={(e) => setApprovalReason(e.currentTarget.value)}
                  placeholder="Enter reason for this action"
                  rows={3}
                  class="w-full px-3 py-2 bg-[var(--bg-primary)] border border-[var(--border-primary)] rounded focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                />
              </div>
            </div>
            <div class="flex gap-2 justify-end mt-6">
              <Button onClick={() => setShowApprovalDialog(false)} variant="secondary" disabled={actionLoading()}>
                Cancel
              </Button>
              <Button
                onClick={handleApprovalAction}
                disabled={actionLoading()}
                class={approvalAction() === "approve" ? "bg-green-500 hover:bg-green-600" : "bg-red-500 hover:bg-red-600"}
              >
                <Show when={actionLoading()} fallback={approvalAction() === "approve" ? "Approve" : "Reject"}>
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
