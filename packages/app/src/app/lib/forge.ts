
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
