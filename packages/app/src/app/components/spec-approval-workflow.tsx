import { createSignal, Show } from "solid-js";
import { submitForReview, approveSpec, rejectSpec, getLatestSpecVersion, OpenSpec } from "../lib/forge";
import { Loader2, CheckCircle, XCircle, Send, AlertCircle } from "lucide-solid";
import Button from "./button";

export type ApprovalWorkflowProps = {
  requirementId: string;
  currentStatus: "draft" | "review" | "approved" | "archived";
  onStatusChange?: () => void;
};

export default function SpecApprovalWorkflow(props: ApprovalWorkflowProps) {
  const [loading, setLoading] = createSignal(false);
  const [showDialog, setShowDialog] = createSignal(false);
  const [dialogType, setDialogType] = createSignal<"submit" | "approve" | "reject" | null>(null);
  const [operatorName, setOperatorName] = createSignal("");
  const [reason, setReason] = createSignal("");

  const handleSubmitForReview = async () => {
    if (!operatorName().trim()) {
      alert("Please enter your name");
      return;
    }

    setLoading(true);
    try {
      await submitForReview(props.requirementId, operatorName(), reason());
      alert("Successfully submitted for review");
      setShowDialog(false);
      setOperatorName("");
      setReason("");
      props.onStatusChange?.();
    } catch (err) {
      alert(`Failed to submit: ${err instanceof Error ? err.message : "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async () => {
    if (!operatorName().trim()) {
      alert("Please enter approver name");
      return;
    }

    setLoading(true);
    try {
      const specData = await getLatestSpecVersion(props.requirementId);
      await approveSpec(props.requirementId, operatorName(), specData, reason());
      alert("Successfully approved. Version created.");
      setShowDialog(false);
      setOperatorName("");
      setReason("");
      props.onStatusChange?.();
    } catch (err) {
      alert(`Failed to approve: ${err instanceof Error ? err.message : "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  const handleReject = async () => {
    if (!operatorName().trim()) {
      alert("Please enter approver name");
      return;
    }

    if (!reason().trim()) {
      alert("Please provide a reason for rejection");
      return;
    }

    setLoading(true);
    try {
      await rejectSpec(props.requirementId, operatorName(), reason());
      alert("Successfully rejected. Spec returned to draft.");
      setShowDialog(false);
      setOperatorName("");
      setReason("");
      props.onStatusChange?.();
    } catch (err) {
      alert(`Failed to reject: ${err instanceof Error ? err.message : "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  const openDialog = (type: "submit" | "approve" | "reject") => {
    setDialogType(type);
    setShowDialog(true);
  };

  const handleConfirm = async () => {
    switch (dialogType()) {
      case "submit":
        await handleSubmitForReview();
        break;
      case "approve":
        await handleApprove();
        break;
      case "reject":
        await handleReject();
        break;
    }
  };

  const getDialogTitle = () => {
    switch (dialogType()) {
      case "submit":
        return "Submit for Review";
      case "approve":
        return "Approve Spec";
      case "reject":
        return "Reject Spec";
      default:
        return "";
    }
  };

  const getDialogIcon = () => {
    switch (dialogType()) {
      case "submit":
        return <Send class="w-6 h-6 text-blue-400" />;
      case "approve":
        return <CheckCircle class="w-6 h-6 text-green-400" />;
      case "reject":
        return <XCircle class="w-6 h-6 text-red-400" />;
      default:
        return null;
    }
  };

  const getConfirmButtonClass = () => {
    switch (dialogType()) {
      case "submit":
        return "bg-blue-500 hover:bg-blue-600";
      case "approve":
        return "bg-green-500 hover:bg-green-600";
      case "reject":
        return "bg-red-500 hover:bg-red-600";
      default:
        return "";
    }
  };

  return (
    <div class="bg-[var(--bg-secondary)] rounded-lg border border-[var(--border-primary)] p-6">
      <h3 class="text-lg font-semibold mb-4">Approval Workflow</h3>

      {/* Status Indicator */}
      <div class="mb-6">
        <div class="flex items-center gap-3">
          <div class={`w-3 h-3 rounded-full ${
            props.currentStatus === "draft" ? "bg-blue-500" :
            props.currentStatus === "review" ? "bg-yellow-500" :
            props.currentStatus === "approved" ? "bg-green-500" :
            "bg-gray-500"
          }`} />
          <div>
            <p class="text-sm font-medium">Current Status</p>
            <p class="text-xs text-[var(--text-secondary)] mt-0.5">
              {props.currentStatus.toUpperCase()}
            </p>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div class="space-y-3">
        <Show when={props.currentStatus === "draft"}>
          <div class="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
            <div class="flex items-start gap-3 mb-3">
              <Send class="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
              <div class="flex-1">
                <p class="text-sm font-medium text-blue-400">Ready to Submit?</p>
                <p class="text-xs text-[var(--text-secondary)] mt-1">
                  Submit this spec for review by an approver. Once submitted, you won't be able to edit until it's approved or rejected.
                </p>
              </div>
            </div>
            <Button
              onClick={() => openDialog("submit")}
              disabled={loading()}
              class="w-full bg-blue-500 hover:bg-blue-600"
            >
              <Send class="w-4 h-4 mr-2" />
              Submit for Review
            </Button>
          </div>
        </Show>

        <Show when={props.currentStatus === "review"}>
          <div class="space-y-3">
            <div class="p-4 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
              <div class="flex items-start gap-3 mb-3">
                <AlertCircle class="w-5 h-5 text-yellow-400 flex-shrink-0 mt-0.5" />
                <div class="flex-1">
                  <p class="text-sm font-medium text-yellow-400">Pending Review</p>
                  <p class="text-xs text-[var(--text-secondary)] mt-1">
                    This spec is waiting for approval. An approver can approve or reject it.
                  </p>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <Button
                onClick={() => openDialog("approve")}
                disabled={loading()}
                class="bg-green-500 hover:bg-green-600"
              >
                <CheckCircle class="w-4 h-4 mr-2" />
                Approve
              </Button>
              <Button
                onClick={() => openDialog("reject")}
                disabled={loading()}
                class="bg-red-500 hover:bg-red-600"
              >
                <XCircle class="w-4 h-4 mr-2" />
                Reject
              </Button>
            </div>
          </div>
        </Show>

        <Show when={props.currentStatus === "approved"}>
          <div class="p-4 bg-green-500/10 border border-green-500/30 rounded-lg">
            <div class="flex items-start gap-3">
              <CheckCircle class="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
              <div class="flex-1">
                <p class="text-sm font-medium text-green-400">Approved</p>
                <p class="text-xs text-[var(--text-secondary)] mt-1">
                  This spec has been approved and a version has been created. Development can now begin.
                </p>
              </div>
            </div>
          </div>
        </Show>

        <Show when={props.currentStatus === "archived"}>
          <div class="p-4 bg-gray-500/10 border border-gray-500/30 rounded-lg">
            <div class="flex items-start gap-3">
              <AlertCircle class="w-5 h-5 text-gray-400 flex-shrink-0 mt-0.5" />
              <div class="flex-1">
                <p class="text-sm font-medium text-gray-400">Archived</p>
                <p class="text-xs text-[var(--text-secondary)] mt-1">
                  This spec has been archived. Development is complete.
                </p>
              </div>
            </div>
          </div>
        </Show>
      </div>

      {/* Approval Dialog */}
      <Show when={showDialog()}>
        <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setShowDialog(false)}>
          <div class="bg-[var(--bg-secondary)] rounded-lg border border-[var(--border-primary)] w-full max-w-md p-6" onClick={(e) => e.stopPropagation()}>
            <div class="flex items-start gap-3 mb-4">
              {getDialogIcon()}
              <div class="flex-1">
                <h3 class="text-lg font-semibold">{getDialogTitle()}</h3>
                <p class="text-sm text-[var(--text-secondary)] mt-1">
                  <Show when={dialogType() === "submit"}>
                    Submit this spec for review. An approver will review and either approve or reject it.
                  </Show>
                  <Show when={dialogType() === "approve"}>
                    Approve this spec and create a new version. This will allow development to begin.
                  </Show>
                  <Show when={dialogType() === "reject"}>
                    Reject this spec and return it to draft status. Please provide a reason for rejection.
                  </Show>
                </p>
              </div>
            </div>

            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium mb-2">
                  {dialogType() === "submit" ? "Your Name" : "Approver Name"}
                </label>
                <input
                  type="text"
                  value={operatorName()}
                  onInput={(e) => setOperatorName(e.currentTarget.value)}
                  placeholder="Enter your name"
                  class="w-full px-3 py-2 bg-[var(--bg-primary)] border border-[var(--border-primary)] rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">
                  Reason {dialogType() === "reject" ? "(Required)" : "(Optional)"}
                </label>
                <textarea
                  value={reason()}
                  onInput={(e) => setReason(e.currentTarget.value)}
                  placeholder={
                    dialogType() === "submit" ? "Why are you submitting this?" :
                    dialogType() === "approve" ? "Any comments on approval?" :
                    "Why are you rejecting this?"
                  }
                  rows={3}
                  class="w-full px-3 py-2 bg-[var(--bg-primary)] border border-[var(--border-primary)] rounded focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                />
              </div>
            </div>

            <div class="flex gap-2 justify-end mt-6">
              <Button onClick={() => setShowDialog(false)} variant="secondary" disabled={loading()}>
                Cancel
              </Button>
              <Button
                onClick={handleConfirm}
                disabled={loading()}
                class={getConfirmButtonClass()}
              >
                <Show when={loading()} fallback={
                  dialogType() === "submit" ? "Submit" :
                  dialogType() === "approve" ? "Approve" :
                  "Reject"
                }>
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
