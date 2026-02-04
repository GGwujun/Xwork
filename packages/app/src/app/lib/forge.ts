import { createClient, unwrap } from "./opencode";

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

export async function generateSpecViaOpenCode(
  requirement: SpecRequirement,
  client: ReturnType<typeof createClient>,
  model: { providerID: string; modelID: string },
  workspaceRoot?: string
): Promise<OpenSpec> {
  let sessionID: string | null = null;

  try {
    // 创建新的 session 用于生成规范
    console.log("[OpenCode] 创建 session...");
    const session = unwrap(
      await client.session.create({
        title: `Generate OpenSpec: ${requirement.summary}`,
        directory: workspaceRoot,
      })
    );

    sessionID = session.id;
    console.log("[OpenCode] Session 创建成功:", sessionID);

    // 构建 prompt
    const prompt = `请根据以下需求生成符合 OpenSpec v0.2.0 规范的技术文档：

## 需求概述
${requirement.summary}

## 详细描述
${requirement.description}

${requirement.acceptance_criteria.length > 0 ? `## 验收标准\n${requirement.acceptance_criteria.map((c, i) => `${i + 1}. ${c}`).join('\n')}` : ''}

请生成一个完整的 OpenSpec JSON 文档，包含以下部分：
1. spec_version: "0.2.0"
2. project_name: 基于需求概述生成项目名称
3. requirement: 包含 summary, description, acceptance_criteria
4. design: 包含架构设计、技术栈选择、数据模型等
5. tasks: 详细的任务分解列表，每个任务包含 id, title, description, status

请直接返回 JSON 格式的 OpenSpec 文档，不要包含任何其他说明文字。`;

    // 发送 prompt - 使用异步方法
    console.log("[OpenCode] 发送 prompt...");
    console.log("[OpenCode] 使用模型:", model);

    await client.session.promptAsync({
      sessionID,
      model,
      parts: [{ type: "text", text: prompt }],
    });
    console.log("[OpenCode] Prompt 已发送");

    // 等待一小段时间让 session 开始处理
    await new Promise(resolve => setTimeout(resolve, 2000));

    // 轮询 session 状态直到完成
    let attempts = 0;
    const maxAttempts = 300; // 5 分钟
    let lastState = "";

    console.log("[OpenCode] 开始轮询 session 状态...");
    while (attempts < maxAttempts) {
      await new Promise(resolve => setTimeout(resolve, 1000));

      // 获取所有 session 的状态
      const statusResult = await client.session.status();
      const allStatus = unwrap(statusResult);

      // allStatus 是一个对象，key 是 sessionID，value 是状态对象
      const sessionStatus = allStatus[sessionID];

      // 如果 session 不存在，说明已经完成并被清理
      if (!sessionStatus) {
        console.log("[OpenCode] Session 已完成（状态为空），获取消息...");
        break;
      }

      const currentState = sessionStatus.type;

      // 只在状态变化时打印日志
      if (currentState !== lastState) {
        console.log(`[OpenCode] 状态变化: ${lastState} -> ${currentState}`);
        lastState = currentState;
      }

      // 每 10 秒打印一次进度
      if (attempts % 10 === 0) {
        console.log(`[OpenCode] 轮询进度: ${attempts}/${maxAttempts} 秒, 当前状态: ${currentState}`);
      }

      if (currentState === "idle") {
        // Session 完成，获取消息
        console.log("[OpenCode] Session 状态为 idle，获取消息...");
        break;
      }

      if (currentState === "error") {
        throw new Error("OpenCode session encountered an error");
      }

      attempts++;
    }

    if (attempts >= maxAttempts) {
      throw new Error("Timeout waiting for OpenCode response");
    }

    // 获取完整消息
    console.log("[OpenCode] 获取完整消息...");
    const messagesResult = await client.session.messages({ sessionID });
    const messages = unwrap(messagesResult);

    // 从消息中提取 OpenSpec
    const assistantMessages = messages.filter((m: any) => m.info?.role === "assistant");
    console.log("[OpenCode] Assistant 消息数量:", assistantMessages.length);

    if (assistantMessages.length === 0) {
      throw new Error("No response from OpenCode");
    }

    const lastMessage = assistantMessages[assistantMessages.length - 1];
    const content = lastMessage.parts
      .filter((p: any) => p.type === "text")
      .map((p: any) => p.text)
      .join("\n");

    console.log("[OpenCode] 响应内容长度:", content.length);
    console.log("[OpenCode] 响应内容预览:", content.substring(0, 200));

    // 尝试解析 JSON - 支持 markdown 代码块
    let jsonText = content;

    // 尝试提取 markdown 代码块中的 JSON
    const codeBlockMatch = content.match(/```(?:json)?\s*\n([\s\S]*?)\n```/);
    if (codeBlockMatch) {
      jsonText = codeBlockMatch[1];
      console.log("[OpenCode] 从 markdown 代码块中提取 JSON");
    } else {
      // 尝试直接匹配 JSON 对象
      const jsonMatch = content.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        jsonText = jsonMatch[0];
        console.log("[OpenCode] 直接匹配到 JSON 对象");
      }
    }

    console.log("[OpenCode] 准备解析 JSON, 长度:", jsonText.length);
    const spec = JSON.parse(jsonText);

    // 验证 OpenSpec 格式
    if (!spec.spec_version || !spec.requirement || !spec.tasks) {
      throw new Error("Invalid OpenSpec format from OpenCode");
    }

    console.log("[OpenCode] OpenSpec 验证通过");

    // 删除临时 session
    if (sessionID) {
      try {
        console.log("[OpenCode] 删除临时 session...");
        // await client.session.delete({ sessionID });
        console.log("[OpenCode] Session 删除成功");
      } catch (deleteError) {
        console.warn("Failed to delete temporary session:", deleteError);
        // 不抛出错误，因为规范已经生成成功
      }
    }

    return spec;
  } catch (error) {
    // 发生错误时也尝试删除 session
    if (sessionID) {
      try {
        // await client.session.delete({ sessionID });
      } catch (deleteError) {
        console.warn("Failed to delete temporary session after error:", deleteError);
      }
    }

    console.error("OpenCode generation error:", error);
    throw new Error(
      error instanceof Error
        ? `OpenCode生成失败: ${error.message}`
        : "OpenCode生成失败: 未知错误"
    );
  }
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
