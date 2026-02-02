
export const FORGE_API_URL = "http://127.0.0.1:8000";

export type SpecRequirement = {
  summary: string;
  description: string;
  acceptance_criteria: string[];
};

export type SpecTask = {
  id: string;
  title: string;
  description: string;
  status: "pending" | "in_progress" | "completed" | "failed";
};

export type OpenSpec = {
  spec_version: string;
  project_name: string;
  requirement: SpecRequirement;
  design?: any;
  tasks: SpecTask[];
};

export type SpecStatus = "draft" | "review" | "approved" | "archived";

export type VersionMetadata = {
  version: number;
  created_at: string;
  approver: string;
  approval_time: string;
  change_summary: string;
  status: string;
};

export type StatusTransition = {
  from_status: string;
  to_status: string;
  operator: string;
  timestamp: string;
  reason: string;
};

export type LifecycleInfo = {
  requirement_id: string;
  current_status: SpecStatus;
  current_version: number | null;
  created_at: string;
  updated_at: string;
  history: StatusTransition[];
  versions: VersionMetadata[];
};

export type SpecStatus = "draft" | "review" | "approved" | "archived";

export type VersionMetadata = {
  version: number;
  created_at: string;
  approver: string;
  approval_time: string;
  change_summary: string;
  status: string;
};

export type StatusTransition = {
  from_status: string;
  to_status: string;
  operator: string;
  timestamp: string;
  reason: string;
};

export type LifecycleInfo = {
  requirement_id: string;
  current_status: SpecStatus;
  current_version: number | null;
  created_at: string;
  updated_at: string;
  history: StatusTransition[];
  versions: VersionMetadata[];
};

export async function generateSpec(requirement: SpecRequirement): Promise<OpenSpec> {
  const response = await fetch(`${FORGE_API_URL}/spec/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requirement),
  });

  if (!response.ok) {
    throw new Error(`Forge Engine Error: ${response.statusText}`);
  }

  return response.json();
}

export async function checkForgeHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${FORGE_API_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}

// --- Spec Lifecycle API ---

export async function getSpecStatus(requirementId: string): Promise<SpecStatus> {
  const response = await fetch(`${FORGE_API_URL}/spec/${requirementId}/status`);
  if (!response.ok) throw new Error("Failed to get spec status");
  const data = await response.json();
  return data.status;
}

export async function getSpecLifecycle(requirementId: string): Promise<LifecycleInfo> {
  const response = await fetch(`${FORGE_API_URL}/spec/${requirementId}/lifecycle`);
  if (!response.ok) throw new Error("Failed to get spec lifecycle");
  return response.json();
}

export async function submitForReview(
  requirementId: string,
  submitter: string,
  reason: string = ""
): Promise<void> {
  const response = await fetch(`${FORGE_API_URL}/spec/${requirementId}/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ submitter, reason }),
  });
  if (!response.ok) throw new Error("Failed to submit for review");
}

export async function approveSpec(
  requirementId: string,
  approver: string,
  specData: OpenSpec,
  reason: string = ""
): Promise<void> {
  const response = await fetch(`${FORGE_API_URL}/spec/${requirementId}/approve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ approver, spec_data: specData, reason }),
  });
  if (!response.ok) throw new Error("Failed to approve spec");
}

export async function rejectSpec(
  requirementId: string,
  approver: string,
  reason: string
): Promise<void> {
  const response = await fetch(`${FORGE_API_URL}/spec/${requirementId}/reject`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ approver, reason }),
  });
  if (!response.ok) throw new Error("Failed to reject spec");
}

export async function archiveSpec(
  requirementId: string,
  operator: string,
  reason: string = ""
): Promise<void> {
  const response = await fetch(`${FORGE_API_URL}/spec/${requirementId}/archive`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ operator, reason }),
  });
  if (!response.ok) throw new Error("Failed to archive spec");
}

// --- Spec Versioning API ---

export async function listSpecVersions(requirementId: string): Promise<VersionMetadata[]> {
  const response = await fetch(`${FORGE_API_URL}/spec/${requirementId}/versions`);
  if (!response.ok) throw new Error("Failed to list versions");
  const data = await response.json();
  return data.versions;
}

export async function getSpecVersion(
  requirementId: string,
  version: number
): Promise<OpenSpec> {
  const response = await fetch(`${FORGE_API_URL}/spec/${requirementId}/version/${version}`);
  if (!response.ok) throw new Error("Failed to get version");
  return response.json();
}

export async function getLatestSpecVersion(requirementId: string): Promise<OpenSpec> {
  const response = await fetch(`${FORGE_API_URL}/spec/${requirementId}/version/latest`);
  if (!response.ok) throw new Error("Failed to get latest version");
  return response.json();
}

export async function compareVersions(
  requirementId: string,
  version1: number,
  version2: number
): Promise<any> {
  const response = await fetch(`${FORGE_API_URL}/spec/${requirementId}/compare`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ version1, version2 }),
  });
  if (!response.ok) throw new Error("Failed to compare versions");
  return response.json();
}

export async function rollbackToVersion(
  requirementId: string,
  version: number
): Promise<void> {
  const response = await fetch(`${FORGE_API_URL}/spec/${requirementId}/rollback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ version }),
  });
  if (!response.ok) throw new Error("Failed to rollback");
}
