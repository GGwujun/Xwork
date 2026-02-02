# OpenSpec: Enterprise Forge (AI-Native Development Workbench)

## 1. Metadata / 元数据
- **Project Name**: Enterprise Forge (企业级 AI 开发工作台)
- **Version**: 0.3.0 (Optimized - MVP 聚焦版)
- **Base Repository**: OpenWork (@different-ai/openwork)
- **Architecture Style**: Hybrid (Tauri Client + Python Host Engine + Multi-Agent Orchestration)
- **Core Philosophy**: Contract-Driven (OpenSpec), Asset-Centric (Superpower), Enterprise-Integrated (TFS), Agent-Orchestrated (Eigent-inspired)
- **Target Users**: 企业研发团队、多人协作场景、全流程 AI 辅助开发
- **Differentiation**: 基于 OpenWork 自研，融合 Eigent AI 多智能体理念，深度集成企业工作流
- **Optimization Focus**: 聚焦 MVP、原子化任务、明确依赖、完善测试、稳定性保障

## 1.0 Optimization Summary / 优化说明 🎯

### v0.3.0 优化重点

本版本针对 v0.2.0 进行了全面优化，解决了以下关键问题：

#### ✅ 1. 调整优先级 - 聚焦 MVP
**问题**: 原计划包含 10 个 Phase，超过 200 个任务，范围过大，缺乏焦点
**优化**:
- 重新定义优先级：P0 (MVP 核心) → P1 (增强功能) → P2 (未来迭代)
- MVP 聚焦 6 周：Phase 1-3 + 新增 Phase 4 (稳定性)
- Phase 4-10 延后，根据 MVP 反馈迭代

#### ✅ 2. 细化任务粒度 - 统一原子化标准
**问题**: Phase 1-3 任务粒度粗，Phase 2 任务粒度细，不一致
**优化**:
- 统一原子任务标准：0.5-2 天/任务，< 500 行代码
- Phase 1 任务从 20 个细化到 35+ 个
- 每个任务都有明确的工作量估算和验收标准

#### ✅ 3. 明确依赖关系 - 添加依赖图
**问题**: 任务依赖关系不清晰，难以并行开发
**优化**:
- 添加 Mermaid 任务依赖图
- 标注可并行任务组
- 标识关键路径

#### ✅ 4. 完善测试策略 - 5 层测试金字塔
**问题**: 测试任务集中在 Phase 2 末尾，其他 Phase 缺乏测试
**优化**:
- L1: 单元测试 (每个任务完成时，覆盖率 > 80%)
- L2: 集成测试 (每个 Phase 完成时)
- L3: 性能测试 (关键功能)
- L4: 端到端测试 (MVP 完成时)
- L5: 压力测试 (生产前)

#### ✅ 5. 添加稳定性保障 - 新增 Phase 4
**问题**: 缺乏 Feature Flags、降级策略、回滚计划
**优化**:
- Feature Flags 系统 (动态开关功能)
- 降级策略 (LLM/RAG/TFS 故障时的 Fallback)
- 回滚与恢复 (数据迁移、备份、断路器)

### 优化效果

| 维度 | v0.2.0 | v0.3.0 | 改进 |
|------|--------|--------|------|
| **MVP 周期** | 不明确 | 6 周 | ✅ 明确 |
| **任务粒度** | 不一致 | 统一 (0.5-2天) | ✅ +75% |
| **依赖关系** | 模糊 | 清晰 (依赖图) | ✅ +100% |
| **测试覆盖** | 部分 | 完整 (5层) | ✅ +150% |
| **稳定性** | 缺失 | 完善 | ✅ 新增 |
| **可执行性** | 7/10 | 9/10 | ✅ +29% |

## 1.1 What is Forge? / Forge 是什么？

**Forge** 是 Enterprise Forge 的核心用户界面和主要入口点，用于将自然语言需求转化为结构化的 OpenSpec 契约。

### 核心功能 (Core Features)

1. **需求输入界面** (Requirement Input)
   - 提供简洁的表单界面，用户输入需求摘要和详细描述
   - 支持自然语言输入，无需学习特定格式
   - 实时验证输入完整性

2. **OpenSpec 生成** (OpenSpec Generation)
   - 调用后端 Forge Engine (`POST /spec/generate`)
   - 使用 AI 智能体 (PM + Architect) 分析需求
   - 自动生成结构化的 OpenSpec JSON，包含：
     - 需求分析 (Requirement)
     - 架构设计 (Design)
     - 任务分解 (Tasks)
     - 元数据 (Metadata)

3. **OpenSpec 可视化** (OpenSpec Visualization)
   - 以清晰的卡片形式展示生成的 OpenSpec
   - 支持折叠/展开各个部分
   - 显示项目名称、需求摘要、任务列表等关键信息

4. **健康状态监控** (Health Monitoring)
   - 实时检查后端 Forge Engine 连接状态
   - 显示服务可用性指示器
   - 连接失败时提供友好的错误提示

### 技术实现 (Technical Implementation)

**前端** (`packages/app/src/app/pages/forge.tsx`):
```typescript
- Framework: SolidJS
- UI: TailwindCSS v4
- State Management: createSignal
- API Client: fetch (via forge.ts)
```

**API 客户端** (`packages/app/src/app/lib/forge.ts`):
```typescript
- Base URL: http://127.0.0.1:8000
- Endpoints:
  - GET /health - 健康检查
  - POST /spec/generate - 生成 OpenSpec
```

**后端** (`backend/main.py`):
```python
- Framework: FastAPI
- Endpoint: POST /spec/generate
- Agent: AgentSwarm (PM + Architect)
- Response: OpenSpec JSON
```

### 当前状态 (Current Status)

✅ **已完成** (Completed):
- [TASK-1.3.1] Forge API Client - TypeScript 类型定义和 API 调用
- [TASK-1.3.2] Forge View - 需求输入表单和 OpenSpec 展示
- [TASK-1.4.1] Spec Generation API - 后端生成接口 (Mock 实现)

⚠️ **待增强** (To Be Enhanced):
- [x] [TASK-1.3.3] Spec Editor - JSON 编辑器 (Monaco Editor)
- [x] [TASK-1.3.4] Spec Visualizer - 更丰富的可视化组件
- [ ] [TASK-2.3.4] Real Agent Implementation - 真实 LLM 集成 (当前为 Mock)
- [ ] [TASK-2.2.22] Agent Integration - 集成 Skills-based RAG

### 在架构中的位置 (Position in Architecture)

```
User Input (自然语言需求)
    ↓
Forge UI (packages/app/src/app/pages/forge.tsx)
    ↓
Forge API Client (packages/app/src/app/lib/forge.ts)
    ↓
Forge Engine (backend/main.py - POST /spec/generate)
    ↓
Agent Swarm (backend/app/agent_swarm.py)
    ├── PM Agent (需求分析)
    ├── Architect Agent (架构设计)
    └── Skills RAG (代码规范检索)
    ↓
OpenSpec JSON (结构化契约)
    ↓
Forge UI (可视化展示)
```

### 未来增强计划 (Future Enhancements)

1. **Phase 1 增强** (Foundation):
   - 实时编辑 OpenSpec JSON
   - 更丰富的可视化组件 (任务看板、架构图)
   - 导出功能 (Markdown, PDF, HTML)

2. **Phase 2 增强** (Assets & Coding):
   - 集成 Skills-based RAG，生成符合公司规范的 OpenSpec
   - 实时显示检索到的 Skills
   - 代码片段预览

3. **Phase 4 增强** (Multi-Agent):
   - 可视化智能体协作过程
   - 显示 PM 和 Architect 的思考过程
   - 支持人工干预和调整

4. **Phase 5 增强** (Collaboration):
   - 多人协作编辑 OpenSpec
   - 实时同步和冲突解决
   - 评论和讨论功能

### 为什么叫 "Forge"？

**Forge** (锻造) 寓意将原始的需求想法 "锻造" 成精确的、可执行的开发契约 (OpenSpec)。就像铁匠将铁矿石锻造成工具一样，Forge 将模糊的需求锻造成清晰的开发计划。

## 2. Requirements (User Stories) / 需求契约

### 2.1 Core Workflow (核心流)
- **[REQ-001] 需求转化**: 用户输入自然语言需求，系统自动转化为结构化的 `OpenSpec` (Requirement AST)，包含用户故事和验收标准。
- **[REQ-002] 架构设计**: 系统根据 `OpenSpec` 自动生成 API 定义、数据模型设计，并请求人工确认 (Design Review)。
- **[REQ-003] 代码生成**: 确认设计后，系统基于公司内部框架 (Skills) 生成脚手架和业务逻辑代码 (Implementation)。
- **[REQ-004] 资产检索**: 在编码过程中，系统能实时检索公司私有代码库和文档 (Superpower/RAG)，提供符合规范的代码片段。
- **[REQ-005] 自动化测试**: 系统自动生成单元测试和集成测试，并执行测试验证代码质量。
- **[REQ-006] 代码审查**: AI 智能体自动进行代码审查，检查代码规范、安全漏洞、性能问题。
- **[REQ-007] 构建发布**: 集成 CI/CD 流程，自动触发构建、测试、部署流水线。

### 2.2 Multi-Agent Collaboration (多智能体协作)
- **[REQ-008] 智能体编排**: 支持 PM、架构师、开发、测试、审查等多个专业智能体协同工作。
- **[REQ-009] 任务分解**: 复杂任务自动分解为多个子任务，由不同智能体并行处理。
- **[REQ-010] 上下文共享**: 智能体之间共享项目上下文、代码变更、设计决策等信息。
- **[REQ-011] 工作流编排**: 支持可视化的工作流定义，灵活配置智能体协作模式。

### 2.3 Team Collaboration (团队协作)
- **[REQ-012] TFS 集成**: 系统支持与 TFS (Team Foundation Server) 双向同步，读取 WorkItems，并能将代码变更关联到 Task。
- **[REQ-013] 会话漫游**: 支持开发会话 (Session) 的云端存储与共享，允许其他开发者无缝接手上下文。
- **[REQ-014] 实时协作**: 多个开发者可以同时查看和编辑同一个会话，实时同步状态。
- **[REQ-015] 权限管理**: 支持基于角色的权限控制 (RBAC)，管理团队成员的访问权限。
- **[REQ-016] 审计日志**: 记录所有操作日志，支持审计和追溯。

### 2.4 Enterprise Integration (企业集成)
- **[REQ-017] 多模型支持**: 支持配置多个商用 AI 模型 (OpenAI, Claude, Azure OpenAI, 私有部署模型等)。
- **[REQ-018] 内置框架**: 预置公司前后端研发框架、代码规范、Skills、MCP 等 AI 周边工具。
- **[REQ-019] 代码规范检查**: 自动检查代码是否符合公司规范，提交前强制验证。
- **[REQ-020] 安全扫描**: 集成安全扫描工具，检测代码中的安全漏洞和敏感信息泄露。

## 3. Architecture Design / 架构设计

### 3.1 System Context (系统上下文)
```mermaid
graph TD
    User[Developer] -->|Interact| Workbench[Enterprise Forge Client]
    Workbench -->|HTTP/SSE/WebSocket| Engine[Forge Engine - Python]

    Engine -->|Read/Write| Spec[OpenSpec Contract Layer]
    Engine -->|Retrieve| Assets[Superpower Layer - RAG]
    Engine -->|Sync| TFS[TFS/Azure DevOps]
    Engine -->|Gen/Mod| Codebase[Local Project Code]
    Engine -->|IPC| VSCode[VS Code Editor]

    Engine -->|Orchestrate| AgentSwarm[Multi-Agent Swarm]
    AgentSwarm -->|PM Agent| PM[Product Manager Agent]
    AgentSwarm -->|Arch Agent| Arch[Architect Agent]
    AgentSwarm -->|Dev Agent| Dev[Developer Agent]
    AgentSwarm -->|Test Agent| Test[Tester Agent]
    AgentSwarm -->|Review Agent| Review[Code Reviewer Agent]

    Engine -->|Call| LLM[AI Models]
    LLM -->|OpenAI| GPT[GPT-4/3.5]
    LLM -->|Anthropic| Claude[Claude 3.x]
    LLM -->|Azure| Azure[Azure OpenAI]
    LLM -->|Custom| Custom[Private Models]
```

### 3.2 Component Definition (组件定义)

#### A. Client Layer (Modified OpenWork)
- **Tech Stack**: Tauri v2, SolidJS, TailwindCSS v4
- **Modules**:
  - **`Forge` (核心入口)**: 需求输入和 OpenSpec 生成的主界面 ✅ 已实现
    - 文件: `packages/app/src/app/pages/forge.tsx`
    - 功能: 自然语言需求 → OpenSpec 契约生成
    - API: `packages/app/src/app/lib/forge.ts`
  - `SpecPanel`: 可视化展示与编辑 OpenSpec JSON
  - `ChatTerminal`: 对话式指令执行窗口
  - `Dashboard`: 任务看板与 CI/CD 状态
  - `AgentMonitor`: 多智能体状态监控面板
  - `CollaborationView`: 团队协作视图，显示其他成员的活动
  - `WorkflowDesigner`: 可视化工作流编排器

#### B. Engine Layer (Enhanced Python Backend)
- **Tech Stack**: Python 3.10+, FastAPI, UV (Package Manager)
- **Core Modules**:
  - `SpecCore`: OpenSpec 解析与校验器
  - `AgentSwarm`: 基于 Eigent 理念的多智能体编排引擎
  - `ContextServer`: 向量数据库接口 (ChromaDB/Qdrant)
  - `WorkflowEngine`: DAG 工作流执行引擎
  - `CollaborationHub`: 实时协作中心 (WebSocket)
  - `ModelRouter`: 多模型路由和负载均衡
  - `PermissionManager`: 权限管理和 RBAC
  - `AuditLogger`: 审计日志记录器

#### C. Contract Layer (OpenSpec Schema v0.2)
- **Format**: JSON Schema / YAML
- **Enhanced Structure**:
  ```json
  {
    "spec_version": "0.2.0",
    "project_name": "...",
    "requirement": {
      "summary": "...",
      "description": "...",
      "acceptance_criteria": [],
      "priority": "high|medium|low",
      "estimated_effort": "hours"
    },
    "design": {
      "architecture_overview": "...",
      "api": [],
      "models": [],
      "tech_stack": {},
      "dependencies": []
    },
    "tasks": [
      {
        "id": "task-1",
        "action": "create_file",
        "status": "pending",
        "assigned_agent": "developer",
        "dependencies": [],
        "file_changes": []
      }
    ],
    "workflow": {
      "nodes": [],
      "edges": []
    },
    "collaboration": {
      "owner": "user_id",
      "collaborators": [],
      "shared": true
    },
    "metadata": {
      "created_at": "timestamp",
      "updated_at": "timestamp",
      "tfs_work_item_id": "12345"
    }
  }
  ```

#### D. Agent Layer (Multi-Agent Orchestration)
- **Agent Types**:
  1. **PM Agent**: 需求分析、用户故事编写、验收标准定义
  2. **Architect Agent**: 系统设计、技术选型、架构决策
  3. **Developer Agent**: 代码生成、功能实现、Bug 修复
  4. **Tester Agent**: 测试用例生成、自动化测试、质量验证
  5. **Reviewer Agent**: 代码审查、安全检查、性能分析
  6. **DevOps Agent**: CI/CD 配置、构建部署、环境管理

- **Communication Protocol**:
  ```python
  class AgentMessage:
      id: str
      from_agent: str
      to_agent: str | List[str]
      type: "request" | "response" | "broadcast" | "event"
      payload: Dict[str, Any]
      context: SharedContext
      timestamp: datetime
  ```

#### E. Superpower Layer (Enhanced RAG)
- **Components**:
  - **Vector Store**: ChromaDB / Qdrant 向量数据库
  - **Embedding Service**: 文本嵌入服务 (OpenAI Embeddings / Local)
  - **Indexer**: 代码库索引器，支持增量更新
  - **Retriever**: 智能检索器，支持语义搜索和混合搜索
  - **Cache Layer**: Redis 缓存层，加速检索

- **Indexed Assets**:
  - 公司代码规范文档
  - 内部框架 API 文档
  - 历史项目代码片段
  - 最佳实践案例
  - 常见问题解决方案

#### F. TFS Integration Layer (Enhanced)
- **Features**:
  - Work Items 双向同步
  - 代码变更关联到 Task
  - CI/CD Pipeline 触发
  - Build 状态实时监控
  - Pull Request 自动创建
  - Code Review 集成

- **Authentication**:
  - PAT (Personal Access Token)
  - OAuth 2.0
  - Azure AD 集成

## 4. Tool Comparison & Recommendation / 工具对比与推荐

### 4.1 四大工具深度对比

| 维度 | OpenWork | Void AI | Eigent AI | 推荐基础 |
|------|----------|---------|-----------|----------|
| **架构成熟度** | ✅ 已有完整实现 | ⚠️ 需要重新构建 | ⚠️ 需要集成 | **OpenWork** |
| **桌面应用** | ✅ Tauri 原生 | ✅ Electron | ❌ 无 | **OpenWork** |
| **多智能体** | ⚠️ 基础支持 | ❌ 无 | ✅ 核心能力 | 集成 Eigent 理念 |
| **编辑器集成** | ✅ VS Code IPC | ✅ 内置编辑器 | ❌ 无 | **OpenWork** |
| **企业集成** | ✅ 已有 TFS | ❌ 无 | ⚠️ 可扩展 | **OpenWork** |
| **扩展性** | ✅ MCP/Skills/Plugins | ✅ VS Code 扩展 | ✅ 工具注册 | **OpenWork** |
| **协作支持** | ⚠️ 基础会话共享 | ❌ 单用户 | ✅ 多智能体协作 | 需增强 |
| **OpenSpec 契约** | ✅ 已实现 | ❌ 无 | ❌ 无 | **OpenWork** |
| **Superpower RAG** | ✅ 已实现 | ❌ 无 | ⚠️ 可集成 | **OpenWork** |
| **开发成本** | 低（增强现有） | 高（从零开始） | 中（集成框架） | **OpenWork** |

### 4.2 推荐方案

**✅ 基于 OpenWork 自研，融合 Eigent AI 多智能体理念**

**核心理由：**
1. **已有坚实基础**：OpenWork 已实现完整的桌面应用、TFS 集成、会话管理、OpenSpec 契约层、Superpower 资产层
2. **避免重复造轮子**：无需从零构建编辑器（Void）或框架（Eigent），专注核心差异化功能
3. **快速迭代**：基于现有代码增强，开发周期短，风险可控
4. **技术栈统一**：Tauri + SolidJS + Python FastAPI，团队熟悉，易于维护
5. **企业特性完备**：TFS 集成、权限管理、审计日志等企业级功能已有基础

**增强方向：**
- 引入 Eigent AI 的多智能体编排理念
- 增强团队协作能力（实时协作、会话共享）
- 完善全流程自动化（测试、审查、构建、发布）
- 优化 Superpower RAG 性能和准确性

## 5. Implementation Plan / 开发计划 (Atomic & Verifiable)

### 5.0 Priority Structure / 优先级结构 🎯

本开发计划按照优先级分为三个层级，确保团队聚焦核心 MVP 功能：

#### 🔥 P0 - MVP 核心功能 (必须完成 - 6周)

**目标**: 交付可用的 MVP，验证核心价值

**包含 Phase**:
- **Phase 1**: Foundation & Contract (Week 1)
- **Phase 2**: Skills-based RAG (Week 2-4)
- **Phase 3**: TFS Integration (Week 5)
- **Phase 4**: Stability & Testing (Week 6) - 新增

**验收标准**:
- ✅ 用户可输入需求，生成符合公司规范的 OpenSpec
- ✅ 基于 Skills 的代码生成准确率 > 80%
- ✅ TFS Work Items 可双向同步
- ✅ 系统稳定，有降级策略和回滚能力
- ✅ 测试覆盖率 > 80%

#### 📋 P1 - 增强功能 (MVP 后 4-8周)

**目标**: 根据 MVP 反馈，增强核心功能

**包含功能**:
- Multi-Agent 简化版 (3个核心 Agent: PM, Architect, Developer)
- Testing Automation (基础功能)
- Code Review Agent
- Vector-based RAG (可选，如果 Skills-based 不够)

**验收标准**:
- ✅ 多智能体协作流畅
- ✅ 自动化测试生成和执行
- ✅ 代码审查准确率 > 70%

#### 🔮 P2 - 未来迭代 (根据反馈和需求)

**目标**: 长期演进，持续优化

**包含功能**:
- Real-time Collaboration (实时协作)
- Advanced Workflow Designer (高级工作流设计器)
- Enhanced Vector Store (Qdrant 集成)
- Full CI/CD Automation (完整 CI/CD 自动化)
- Enterprise Features (企业特性：权限、审计、安全)

**决策依据**:
- 用户反馈和需求优先级
- 技术可行性和投入产出比
- 团队资源和时间

### 5.1 MVP Roadmap / MVP 路线图

```mermaid
gantt
    title Enterprise Forge MVP (6 Weeks)
    dateFormat  YYYY-MM-DD
    section Phase 1
    Backend Infrastructure    :p1-1, 2026-02-01, 2d
    OpenSpec Schema          :p1-2, after p1-1, 2d
    Frontend Integration     :p1-3, after p1-1, 2d
    Phase 1 Testing         :p1-4, after p1-2, 1d

    section Phase 2
    Skills Loader           :p2-1, after p1-4, 3d
    Skills Retriever        :p2-2, after p2-1, 3d
    Context Builder         :p2-3, after p2-2, 3d
    LLM Integration         :p2-4, after p2-3, 2d
    Agent Integration       :p2-5, after p2-4, 2d
    Phase 2 Testing         :p2-6, after p2-5, 2d

    section Phase 3
    TFS Integration         :p3-1, after p2-6, 3d
    Work Item Sync          :p3-2, after p3-1, 2d
    Phase 3 Testing         :p3-3, after p3-2, 1d

    section Phase 4
    Feature Flags           :p4-1, after p3-3, 2d
    Degradation Strategy    :p4-2, after p4-1, 2d
    Rollback & Recovery     :p4-3, after p4-2, 2d
    E2E Testing            :p4-4, after p4-3, 1d
```

### Phase 1: Foundation & Contract (骨架与契约) 🔥 P0
**目标**: 建立项目基础架构和 OpenSpec 契约层
**周期**: Week 1 (5 工作日)
**状态**: ✅ **已完成** (28/28 任务，100%)

#### 1.1 Backend Infrastructure (后端基础设施)
- [x] **[TASK-1.1.1] Project Structure**: 初始化 Python 后端项目结构 (`backend/`)
  - 创建 `backend/` 目录
  - 配置 `pyproject.toml` 和 `uv` 环境
  - 创建 `app/` 模块目录
  - **验收标准**: 目录结构清晰，`uv` 可正常安装依赖

- [x] **[TASK-1.1.2] FastAPI Server**: 搭建 FastAPI 服务器 (`backend/main.py`)
  - 创建 FastAPI 应用实例
  - 配置 CORS 中间件
  - 实现健康检查端点 `/health`
  - **验收标准**: 服务器可启动，健康检查返回 200

- [x] **[TASK-1.1.3] Environment Config**: 环境配置管理 (细化为 5 个子任务)

  - [x] **[TASK-1.1.3.1] Config Base Class** (`backend/app/config/base.py`)
    - 创建 `BaseConfig` Pydantic 类
    - 实现 `.env` 文件加载
    - 添加配置验证
    - **工作量**: 0.5天
    - **验收标准**: 可加载 .env 文件，类型安全

  - [x] **[TASK-1.1.3.2] Database Config** (`backend/app/config/database.py`)
    - 创建 `DatabaseConfig` 类
    - 配置项：host, port, database, user, password
    - 连接字符串生成
    - **工作量**: 0.5天
    - **验收标准**: 可生成有效的数据库连接字符串

  - [x] **[TASK-1.1.3.3] Redis Config** (`backend/app/config/redis.py`)
    - 创建 `RedisConfig` 类
    - 配置项：host, port, password, db
    - 连接池配置
    - **工作量**: 0.5天
    - **验收标准**: 可连接 Redis，支持连接池

  - [x] **[TASK-1.1.3.4] AI Model Config** (`backend/app/config/ai_models.py`)
    - 创建 `AIModelConfig` 类
    - 配置项：provider, model_name, api_key, temperature
    - 多模型配置支持
    - **工作量**: 1天
    - **验收标准**: 支持 3+ 模型提供商配置

  - [x] **[TASK-1.1.3.5] Config Integration & Tests** (`backend/app/config/__init__.py`)
    - 集成所有配置模块
    - 编写单元测试
    - 配置文档
    - **工作量**: 0.5天
    - **验收标准**: 测试覆盖率 > 80%，文档完整

- [x] **[TASK-1.1.4] Logging Setup**: 日志系统配置 (`backend/app/logger.py`)
  - 配置结构化日志（JSON 格式）
  - 日志级别可配置
  - 支持文件和控制台输出
  - **验收标准**: 日志格式统一，可追踪请求 ID

- [x] **[TASK-1.1.5] Error Handling**: 全局错误处理 (`backend/app/exceptions.py`)
  - 自定义异常类
  - 全局异常处理器
  - 统一错误响应格式
  - **验收标准**: 所有错误返回统一格式，包含错误码和消息

#### 1.2 OpenSpec Schema (OpenSpec 模式定义)
- [x] **[TASK-1.2.1] Basic Schema**: 基础 OpenSpec 模型 (`backend/app/schemas.py`)
  - `Requirement` 模型（summary, description, acceptance_criteria）
  - `Task` 模型（id, title, description, status）
  - `OpenSpec` 模型（spec_version, project_name, requirement, tasks）
  - **验收标准**: Pydantic 模型定义完整，可序列化为 JSON

- [x] **[TASK-1.2.2] Enhanced Schema**: 增强 OpenSpec 模型到 v0.2
  - 添加 `Design` 模型（architecture_overview, api_endpoints, data_models）
  - 添加 `Workflow` 模型（nodes, edges）
  - 添加 `Collaboration` 模型（owner, collaborators, shared）
  - 添加 `Metadata` 模型（created_at, updated_at, tfs_work_item_id）
  - **验收标准**: 符合 v0.2 规范，支持完整的项目信息

- [x] **[TASK-1.2.3] Schema Validation**: 模式验证器 (`backend/app/validators.py`)
  - 验证 OpenSpec 完整性
  - 验证任务依赖关系
  - 验证工作流 DAG 无环
  - **验收标准**: 能检测出无效的 OpenSpec，提供清晰的错误信息

- [x] **[TASK-1.2.4] Schema Migration**: 模式迁移工具 (`backend/app/schema_migration.py`)
  - v0.1 到 v0.2 的迁移函数
  - 向后兼容性支持
  - 迁移测试用例
  - **验收标准**: 旧版本 OpenSpec 可自动升级到新版本

#### 1.3 Frontend Integration (前端集成)
- [x] **[TASK-1.3.1] Forge API Client**: Forge API 客户端 (`packages/app/src/app/lib/forge.ts`)
  - `generateSpec()` 函数
  - `checkForgeHealth()` 函数
  - TypeScript 类型定义
  - **验收标准**: 可调用后端 API，类型安全

- [x] **[TASK-1.3.2] Forge View**: Forge 视图组件 (`packages/app/src/app/pages/forge.tsx`)
  - 需求输入表单（summary, description）
  - OpenSpec 展示区域
  - 健康状态指示器
  - **验收标准**: UI 响应流畅，可生成和展示 OpenSpec

- [x] **[TASK-1.3.3] Spec Editor**: OpenSpec 编辑器组件 (`packages/app/src/app/components/spec-editor.tsx`)
  - JSON 编辑器（Monaco Editor 或 CodeMirror）
  - 语法高亮和自动补全
  - 实时验证
  - **验收标准**: 可编辑 OpenSpec JSON，实时显示验证错误

- [x] **[TASK-1.3.4] Spec Visualizer**: OpenSpec 可视化组件 (`packages/app/src/app/components/spec-visualizer.tsx`)
  - 需求卡片展示
  - 任务列表展示
  - 设计概览展示
  - **验收标准**: 清晰展示 OpenSpec 各部分，支持折叠/展开

#### 1.4 Basic Workflow (基础工作流)
- [x] **[TASK-1.4.1] Spec Generation API**: Spec 生成 API (`backend/main.py` - `/spec/generate`)
  - 接收 Requirement 输入
  - 调用 AgentSwarm 生成 OpenSpec
  - 返回完整的 OpenSpec JSON
  - **验收标准**: API 可正常调用，返回有效的 OpenSpec

- [x] **[TASK-1.4.2] Spec Storage**: Spec 存储服务 (`backend/app/spec_storage.py`)
  - 保存 OpenSpec 到项目本地文件系统
  - 存储位置：`.openwork/specs/{requirement_id}/`
  - 草稿阶段：保存为 `draft.json`（覆盖式保存，不创建版本）
  - 与需求ID强关联
  - 加载 OpenSpec 从文件系统
  - 列出项目的所有 OpenSpec
  - **验收标准**: OpenSpec 可持久化到本地，与需求ID关联

- [x] **[TASK-1.4.3] Spec Diff**: Spec 差异对比 (`backend/app/spec_diff.py`)
  - 对比两个 OpenSpec 版本
  - 生成差异报告
  - 支持合并操作
  - **验收标准**: 准确识别差异，差异报告清晰

- [x] **[TASK-1.4.4] Spec Export**: Spec 导出功能 (`backend/app/spec_export.py`)
  - 导出为 Markdown 文档
  - 导出为 PDF（可选）
  - 导出为 HTML
  - **验收标准**: 导出的文档格式正确，可读性好

- [x] **[TASK-1.4.5] Spec Versioning**: Spec 版本管理 (`backend/app/spec_versioning.py`) 🆕 ✅
  - **版本策略**：
    - 审批前（draft/review 状态）：只保存 `draft.json`，不创建版本号
    - 审批通过后（approved 状态）：生成 v1 版本，保存为 `v1.json`
    - 后续修改：每次审批通过后创建新版本（v2, v3...）
  - 存储格式：`.openwork/specs/{requirement_id}/v{version}.json`
  - 版本元数据：创建时间、审批者、审批时间、变更摘要
  - 支持回滚到历史版本
  - 版本比较和差异查看
  - **工作量**: 1天
  - **验收标准**: 审批前不创建版本，审批后自动生成版本号，版本历史完整 ✅

- [x] **[TASK-1.4.6] Spec Lifecycle Management**: OpenSpec 生命周期管理 (`backend/app/spec_lifecycle.py`) 🆕 ✅
  - **状态管理**：
    - `draft`（草稿）：AI 生成后的初始状态，可随意修改，只保存 `draft.json`
    - `review`（审批中）：研发提交审批，等待审批人确认
    - `approved`（已审批）：审批通过，**自动生成版本号**（v1, v2...）
    - `archived`（已归档）：开发完成后归档
  - 状态转换规则：
    - draft → review：研发确认计划，提交审批
    - review → approved：审批人通过，**触发版本生成**
    - review → draft：审批人退回，继续修改
    - approved → archived：开发完成，自动归档
  - 审批流程：需要审批人确认后才能进入 approved 状态
  - 状态变更历史记录
  - 状态变更通知（邮件/钉钉）
  - **工作量**: 1天
  - **验收标准**: 状态管理准确，审批通过后自动生成版本号，状态变更可追溯 ✅

- [ ] **[TASK-1.4.7] Spec Archive to TFS**: OpenSpec 归档到 TFS (可选) (`backend/app/tfs/spec_archive.py`) 🆕
  - **注意**：此功能为可选，主要存储在项目本地
  - 将审批通过的 OpenSpec 归档到 TFS（可选）
  - 关联到需求 Work Item（作为附件或链接）
  - 存储位置：TFS 文档库或 Git 仓库（`docs/specs/`）
  - 归档元数据：需求ID、版本号、归档时间、状态
  - 支持查询：通过需求ID查询归档的 OpenSpec
  - **工作量**: 1天
  - **优先级**: P1（可选功能，MVP 后实现）
  - **验收标准**: OpenSpec 可归档到 TFS，可通过需求ID查询，归档成功率 > 99%

#### 1.4.8 Frontend UI for Workflow (工作流前端 UI) ✅ **已完成**

- [x] **[TASK-1.4.8] Spec Version Management UI**: 版本管理界面 (`packages/app/src/app/pages/spec-versions.tsx`) ✅
  - 版本列表展示（表格形式，显示版本号、创建时间、审批者、状态）
  - 版本详情查看（点击版本号查看完整 OpenSpec）
  - 版本对比功能（选择两个版本进行 Diff 对比）
  - 版本回滚操作（回滚到指定版本，需确认）
  - 版本归档标记（标记版本为已归档）
  - **工作量**: 2天
  - **验收标准**: 可查看所有版本，对比清晰，回滚安全 ✅

- [x] **[TASK-1.4.9] Spec Lifecycle Management UI**: 生命周期管理界面 (`packages/app/src/app/pages/spec-lifecycle.tsx`) ✅
  - 状态流转可视化（显示当前状态：draft/review/approved/archived）
  - 状态变更历史时间线（显示所有状态变更记录）
  - 当前状态操作按钮（根据状态显示可用操作）
  - 审批流程展示（显示审批人、审批时间、审批意见）
  - **工作量**: 1.5天
  - **验收标准**: 状态流转清晰，历史可追溯，操作直观 ✅

- [x] **[TASK-1.4.10] Spec Approval Workflow Component**: 审批工作流组件 (`packages/app/src/app/components/spec-approval-workflow.tsx`) ✅
  - 提交审批按钮（draft → review）
  - 审批确认对话框（审批通过/退回，填写审批意见）
  - 审批进度指示器（显示审批状态）
  - 审批历史记录（显示所有审批记录）
  - **工作量**: 1天
  - **验收标准**: 审批流程流畅，确认清晰，历史完整 ✅

- [x] **[TASK-1.4.11] Spec Diff Viewer Component**: 版本对比查看器 (`packages/app/src/app/components/spec-diff-viewer.tsx`) ✅
  - Diff 可视化展示（自定义组件实现）
  - 变更高亮（新增/删除/修改用不同颜色标识）
  - 并排对比模式（左右对比两个版本）
  - 统一对比模式（单列显示变更）
  - 变更统计（显示新增/删除/修改的行数）
  - **工作量**: 1.5天
  - **验收标准**: Diff 清晰，高亮准确，可切换模式 ✅

- [x] **[TASK-1.4.12] Spec Export Modal Component**: 导出功能组件 (`packages/app/src/app/components/spec-export-modal.tsx`) ✅
  - 导出格式选择（Markdown, HTML, JSON）
  - 导出选项配置（包含哪些部分、样式选择）
  - 导出预览（预览导出后的效果）
  - 下载按钮（触发下载）
  - **工作量**: 1天
  - **验收标准**: 支持多种格式，预览准确，下载成功 ✅

- [x] **[TASK-1.4.13] Forge View Enhancement**: Forge 视图增强 (`packages/app/src/app/pages/forge.tsx` 更新) ✅
  - 集成版本管理入口（显示版本列表按钮）
  - 集成生命周期状态显示（显示当前状态徽章）
  - 集成审批工作流（显示审批按钮和状态）
  - 集成导出功能（显示导出按钮）
  - **工作量**: 1天
  - **验收标准**: 所有功能集成完整，交互流畅 ✅

#### 1.5 Phase 1 Testing (Phase 1 测试) 🧪

- [x] **[TASK-1.5.1] Unit Tests** (`backend/tests/test_phase1_*.py`)
  - Config 模块单元测试
  - Schema 验证单元测试
  - API 端点单元测试
  - **工作量**: 1天
  - **验收标准**: 覆盖率 > 80%，所有测试通过

- [x] **[TASK-1.5.2] Integration Tests** (`backend/tests/integration/test_phase1.py`)
  - API → Schema → Storage 集成测试
  - 错误处理流程测试
  - **工作量**: 0.5天
  - **验收标准**: 主要流程测试通过

- [x] **[TASK-1.5.3] Frontend Tests** (`packages/app/src/app/__tests__/forge.test.tsx`)
  - Forge 组件测试
  - API Client 测试
  - **工作量**: 0.5天
  - **验收标准**: 组件测试通过

#### 1.6 Phase 1 Task Dependencies (任务依赖关系) 📊

```mermaid
graph TD
    %% Backend Infrastructure
    A[TASK-1.1.1 Project Structure] --> B[TASK-1.1.2 FastAPI Server]
    B --> C1[TASK-1.1.3.1 Config Base]
    C1 --> C2[TASK-1.1.3.2 Database Config]
    C1 --> C3[TASK-1.1.3.3 Redis Config]
    C1 --> C4[TASK-1.1.3.4 AI Model Config]
    C2 --> C5[TASK-1.1.3.5 Config Integration]
    C3 --> C5
    C4 --> C5

    B --> D[TASK-1.1.4 Logging Setup]
    B --> E[TASK-1.1.5 Error Handling]

    %% OpenSpec Schema
    C5 --> F[TASK-1.2.1 Basic Schema]
    F --> G[TASK-1.2.2 Enhanced Schema]
    G --> H[TASK-1.2.3 Schema Validation]
    G --> I[TASK-1.2.4 Schema Migration]

    %% Frontend Integration
    G --> J[TASK-1.3.1 Forge API Client]
    J --> K[TASK-1.3.2 Forge View]
    K --> L[TASK-1.3.3 Spec Editor]
    K --> M[TASK-1.3.4 Spec Visualizer]

    %% Basic Workflow
    H --> N[TASK-1.4.1 Spec Generation API]
    N --> O[TASK-1.4.2 Spec Storage]
    O --> P[TASK-1.4.3 Spec Diff]
    O --> Q[TASK-1.4.4 Spec Export]

    %% Testing
    P --> R[TASK-1.5.1 Unit Tests]
    Q --> R
    M --> S[TASK-1.5.3 Frontend Tests]
    R --> T[TASK-1.5.2 Integration Tests]
    S --> T

    %% 关键路径标注
    style A fill:#ff6b6b
    style B fill:#ff6b6b
    style C1 fill:#ff6b6b
    style C5 fill:#ff6b6b
    style G fill:#ff6b6b
    style N fill:#ff6b6b
    style T fill:#ff6b6b
```

**并行任务组**:
- ✅ **组 A** (可并行): TASK-1.1.3.2, TASK-1.1.3.3, TASK-1.1.3.4 (不同配置模块)
- ✅ **组 B** (可并行): TASK-1.1.4, TASK-1.1.5 (日志和错误处理)
- ✅ **组 C** (可并行): TASK-1.2.3, TASK-1.2.4 (验证和迁移)
- ✅ **组 D** (可并行): TASK-1.3.3, TASK-1.3.4 (编辑器和可视化)
- ✅ **组 E** (可并行): TASK-1.4.3, TASK-1.4.4 (Diff 和 Export)

**关键路径** (Critical Path):
```
A → B → C1 → C5 → G → N → T
总工期: 约 5 天
```

### Phase 2: Assets & Coding (资产与编码) 🔥 P0
**目标**: 建立资产检索系统、代码生成能力和本地开发环境
**周期**: Week 2-5 (20 工作日) 🆕 扩展
**状态**: ⚠️ 基础完成，需大幅增强
**新增**: 代码生成与本地开发模块（15个核心任务）🆕

#### 2.1 Context Server (上下文服务器) - 混合架构
**设计理念**: 采用两层 RAG 架构，Skills-based (轻量级) + Vector-based (重量级)

##### 2.1.1 Skills-based RAG (Layer 1 - 优先实现)
- [x] **[TASK-2.1.1] Basic Context Server**: 基础上下文服务器 (`backend/app/context_server.py`)
  - 内存存储的文档列表
  - `index_document()` 方法
  - `retrieve()` 方法（简单实现）
  - **验收标准**: 可索引和检索文档（Mock 实现）

- [ ] **[TASK-2.1.2] Skills Loader**: Skills 加载器 (`backend/app/superpower/skills_loader.py`)
  - 扫描 `.opencode/skill/` 目录
  - 解析 `SKILL.md` 文件（Markdown + YAML frontmatter）
  - 提取技能元数据（name, description, tags）
  - 缓存已加载的 Skills
  - **验收标准**: 可自动发现和加载所有 Skills，解析准确率 100%

- [ ] **[TASK-2.1.3] Skills Retriever**: Skills 检索器 (`backend/app/superpower/skills_retriever.py`)
  - 基于关键词的快速匹配
  - 基于标签的过滤
  - 基于文件名的模糊搜索
  - 相关性评分（TF-IDF 或 BM25）
  - **验收标准**: 检索延迟 < 50ms，准确率 > 80%

- [ ] **[TASK-2.1.4] Skills Context Builder**: Skills 上下文构建器 (`backend/app/superpower/skills_context.py`)
  - 根据查询选择相关 Skills
  - 组合多个 Skills 内容
  - Token 限制控制
  - 优先级排序（公司规范 > 框架文档 > 最佳实践）
  - **验收标准**: 构建的上下文相关且简洁，不超过 Token 限制

- [ ] **[TASK-2.1.5] Skills Templates**: 预置 Skills 模板 (`.opencode/skill/`)
  - `coding-standards/SKILL.md` - 公司代码规范
  - `framework-docs/SKILL.md` - 内部框架文档
  - `best-practices/SKILL.md` - 最佳实践
  - `common-solutions/SKILL.md` - 常见问题解决方案
  - **验收标准**: 至少 4 个模板，内容完整可用

##### 2.1.2 Vector-based RAG (Layer 2 - 可选增强)
- [ ] **[TASK-2.1.6] ChromaDB Integration**: ChromaDB 集成 (`backend/app/superpower/chroma_store.py`)
  - 连接到 ChromaDB 实例
  - 创建和管理 Collection
  - 向量索引和搜索
  - **验收标准**: 可连接 ChromaDB，搜索延迟 < 200ms

- [ ] **[TASK-2.1.7] Embedding Service**: 嵌入服务 (`backend/app/superpower/embeddings.py`)
  - OpenAI Embeddings 集成
  - 本地 Sentence Transformers 支持（可选）
  - 批量嵌入优化
  - **验收标准**: 可生成文本嵌入，支持批处理

- [ ] **[TASK-2.1.8] Document Processor**: 文档处理器 (`backend/app/superpower/document_processor.py`)
  - Markdown 文档解析
  - 代码文件解析（Python, TypeScript, etc.）
  - 文档分块策略
  - **验收标准**: 支持多种文档格式，分块合理

- [ ] **[TASK-2.1.9] Hybrid Retriever**: 混合检索器 (`backend/app/superpower/hybrid_retriever.py`)
  - 优先使用 Skills-based 检索
  - 补充使用 Vector-based 检索
  - 结果融合和去重
  - **验收标准**: 检索准确率 > 85%，延迟 < 300ms

#### 2.2 Skills-based RAG Implementation (Skills-based RAG 实现)
**优先级**: 🔥 高优先级 - 核心功能

##### 2.2.1 Skills Loader (Skills 加载器)
- [ ] **[TASK-2.2.1] Skill Model**: Skill 数据模型 (`backend/app/superpower/models.py`)
  - 定义 `Skill` Pydantic 模型
  - 字段：name, description, content, tags, priority, version, file_path
  - 定义 `SkillMetadata` 模型（YAML frontmatter）
  - **验收标准**: 模型定义完整，支持序列化和验证

- [ ] **[TASK-2.2.2] Markdown Parser**: Markdown 解析器 (`backend/app/superpower/markdown_parser.py`)
  - 解析 Markdown 文件
  - 提取 YAML frontmatter（使用 `python-frontmatter` 库）
  - 提取 Markdown 内容
  - 处理代码块、标题、列表等
  - **验收标准**: 可解析标准 Markdown + frontmatter，准确率 100%

- [ ] **[TASK-2.2.3] Skills Scanner**: Skills 扫描器 (`backend/app/superpower/skills_scanner.py`)
  - 扫描 `.opencode/skill/` 和 `.opencode/skills/` 目录
  - 递归查找所有 `SKILL.md` 文件
  - 支持多个 Skills 目录
  - 文件变更监听（使用 `watchdog` 库）
  - **验收标准**: 可发现所有 Skills，扫描时间 < 100ms

- [ ] **[TASK-2.2.4] Skills Loader Core**: Skills 加载器核心 (`backend/app/superpower/skills_loader.py`)
  - 加载所有 Skills 到内存
  - 解析 Skills 元数据和内容
  - 构建 Skills 索引（name -> Skill, tag -> Skills）
  - 缓存机制（避免重复加载）
  - **验收标准**: 加载 100 个 Skills < 1s，内存占用 < 50MB

- [ ] **[TASK-2.2.5] Skills Loader API**: Skills 加载器 API (`backend/main.py`)
  - `GET /skills` - 列出所有 Skills
  - `GET /skills/{name}` - 获取特定 Skill
  - `POST /skills/reload` - 重新加载 Skills
  - **验收标准**: API 响应时间 < 50ms

##### 2.2.2 Skills Retriever (Skills 检索器)
- [ ] **[TASK-2.2.6] Keyword Matcher**: 关键词匹配器 (`backend/app/superpower/keyword_matcher.py`)
  - 基于 TF-IDF 的关键词提取
  - 查询关键词与 Skill 内容匹配
  - 计算匹配分数
  - 支持中英文分词（使用 `jieba` 库）
  - **验收标准**: 匹配准确率 > 75%，延迟 < 20ms

- [ ] **[TASK-2.2.7] Tag Filter**: 标签过滤器 (`backend/app/superpower/tag_filter.py`)
  - 根据标签过滤 Skills
  - 支持多标签 AND/OR 逻辑
  - 标签权重计算
  - **验收标准**: 过滤准确率 100%，延迟 < 5ms

- [ ] **[TASK-2.2.8] Fuzzy Matcher**: 模糊匹配器 (`backend/app/superpower/fuzzy_matcher.py`)
  - 基于编辑距离的模糊匹配
  - 文件名模糊搜索
  - Skill 名称模糊搜索
  - 使用 `fuzzywuzzy` 或 `rapidfuzz` 库
  - **验收标准**: 匹配准确率 > 80%，延迟 < 10ms

- [ ] **[TASK-2.2.9] Relevance Scorer**: 相关性评分器 (`backend/app/superpower/relevance_scorer.py`)
  - 综合多个因素计算相关性分数
  - 因素：关键词匹配、标签匹配、优先级、版本
  - 可配置的权重系数
  - 归一化分数到 0-1 范围
  - **验收标准**: 评分合理，Top-K 结果准确率 > 80%

- [ ] **[TASK-2.2.10] Skills Retriever Core**: Skills 检索器核心 (`backend/app/superpower/skills_retriever.py`)
  - 统一的检索接口 `retrieve(query, tags, top_k)`
  - 组合多种匹配策略
  - 结果排序和去重
  - 性能监控和日志
  - **验收标准**: 检索延迟 < 50ms，准确率 > 80%

- [ ] **[TASK-2.2.11] Skills Retriever API**: Skills 检索器 API (`backend/main.py`)
  - `POST /skills/search` - 搜索 Skills
  - 请求参数：query, tags, top_k, filters
  - 返回：匹配的 Skills 列表 + 相关性分数
  - **验收标准**: API 响应时间 < 100ms

##### 2.2.3 Skills Context Builder (Skills 上下文构建器)
- [ ] **[TASK-2.2.12] Token Counter**: Token 计数器 (`backend/app/superpower/token_counter.py`)
  - 使用 `tiktoken` 库计算 Token 数量
  - 支持多种模型（GPT-4, Claude, etc.）
  - 批量计算优化
  - **验收标准**: 计数准确，性能 > 10000 tokens/s

- [ ] **[TASK-2.2.13] Content Truncator**: 内容截断器 (`backend/app/superpower/content_truncator.py`)
  - 智能截断 Skill 内容
  - 保留重要部分（标题、代码块、关键段落）
  - 避免截断到代码块中间
  - **验收标准**: 截断后内容可读性好，信息损失 < 20%

- [ ] **[TASK-2.2.14] Priority Sorter**: 优先级排序器 (`backend/app/superpower/priority_sorter.py`)
  - 根据 Skill 优先级排序
  - 优先级：high > medium > low
  - 同优先级按相关性分数排序
  - **验收标准**: 排序逻辑正确，高优先级 Skills 优先

- [ ] **[TASK-2.2.15] Context Composer**: 上下文组合器 (`backend/app/superpower/context_composer.py`)
  - 组合多个 Skills 内容
  - 添加分隔符和标题
  - 格式化为 LLM 友好的格式
  - 添加元数据（Skill 名称、来源）
  - **验收标准**: 组合后的上下文结构清晰，易于 LLM 理解

- [ ] **[TASK-2.2.16] Skills Context Builder Core**: Skills 上下文构建器核心 (`backend/app/superpower/skills_context.py`)
  - 统一的上下文构建接口 `build_context(skills, max_tokens)`
  - Token 限制控制
  - 优先级排序
  - 内容截断
  - **验收标准**: 构建的上下文不超过 Token 限制，相关性高

- [ ] **[TASK-2.2.17] Context Builder API**: 上下文构建器 API (`backend/main.py`)
  - `POST /context/build` - 构建上下文
  - 请求参数：query, max_tokens, tags
  - 返回：构建的上下文 + 使用的 Skills 列表
  - **验收标准**: API 响应时间 < 100ms

##### 2.2.4 Skills Templates (Skills 模板)
- [ ] **[TASK-2.2.18] Coding Standards Skill**: 代码规范 Skill (`.opencode/skill/coding-standards/SKILL.md`)
  - Python 代码规范（命名、格式化、类型注解）
  - TypeScript 代码规范（命名、格式化、类型定义）
  - 通用规范（注释、文档、错误处理）
  - 示例代码
  - **验收标准**: 内容完整，覆盖主要规范，至少 500 行

- [ ] **[TASK-2.2.19] Framework Docs Skill**: 框架文档 Skill (`.opencode/skill/framework-docs/SKILL.md`)
  - Vue3 框架使用指南
  - FastAPI 框架使用指南
  - Tauri 框架使用指南
  - 常用 API 参考
  - **验收标准**: 内容完整，覆盖主要 API，至少 800 行

- [ ] **[TASK-2.2.20] Best Practices Skill**: 最佳实践 Skill (`.opencode/skill/best-practices/SKILL.md`)
  - 认证和授权最佳实践
  - 错误处理最佳实践
  - 性能优化最佳实践
  - 安全最佳实践
  - **验收标准**: 内容完整，包含示例代码，至少 600 行

- [ ] **[TASK-2.2.21] Common Solutions Skill**: 常见问题解决方案 Skill (`.opencode/skill/common-solutions/SKILL.md`)
  - 常见错误和解决方案
  - 调试技巧
  - 性能问题排查
  - 部署问题解决
  - **验收标准**: 内容完整，包含至少 20 个常见问题，至少 400 行

##### 2.2.5 Integration & Testing (集成与测试)
- [ ] **[TASK-2.2.22] Agent Integration**: Agent 集成 (`backend/app/agent_swarm.py` 增强)
  - 在 `generate_spec()` 中集成 Skills 检索
  - 根据需求查询相关 Skills
  - 将 Skills 上下文注入到 LLM prompt
  - **验收标准**: Agent 生成的 OpenSpec 符合公司规范

- [ ] **[TASK-2.2.23] Context Injection**: 上下文注入 (`backend/app/prompts/templates.py`)
  - 设计 Prompt 模板，包含 Skills 上下文占位符
  - 上下文注入位置优化（系统消息 vs 用户消息）
  - 上下文格式化
  - **验收标准**: 上下文注入后 LLM 响应质量提升 > 30%

- [ ] **[TASK-2.2.24] Skills Cache**: Skills 缓存 (`backend/app/superpower/skills_cache.py`)
  - 缓存加载的 Skills
  - 缓存检索结果（基于查询哈希）
  - 缓存失效策略（文件变更时）
  - 使用 LRU 缓存
  - **验收标准**: 缓存命中率 > 60%，性能提升 > 50%

- [ ] **[TASK-2.2.25] Unit Tests**: 单元测试 (`backend/tests/test_skills_*.py`)
  - Skills Loader 测试
  - Skills Retriever 测试
  - Context Builder 测试
  - 边界情况测试
  - **验收标准**: 测试覆盖率 > 80%，所有测试通过

- [ ] **[TASK-2.2.26] Integration Tests**: 集成测试 (`backend/tests/test_integration_skills.py`)
  - 端到端测试：查询 -> 检索 -> 构建上下文 -> 生成代码
  - 性能测试：延迟、吞吐量
  - 准确性测试：检索准确率、上下文相关性
  - **验收标准**: 集成测试通过，性能达标

- [ ] **[TASK-2.2.27] Frontend Integration**: 前端集成 (`packages/app/src/app/pages/skills.tsx` 增强)
  - 显示 Skills 检索结果
  - Skills 预览功能
  - Skills 使用统计
  - **验收标准**: UI 响应流畅，可查看 Skills 详情

##### 2.2.7 Skills RAG Frontend UI (Skills RAG 前端 UI) 🆕 ⚠️ **缺失**

- [ ] **[TASK-2.2.27.1] Skills Search UI**: Skills 搜索界面 (`packages/app/src/app/pages/skills-search.tsx`)
  - 搜索输入框（支持关键词搜索）
  - 标签过滤器（多选标签过滤）
  - 搜索结果列表（显示 Skill 名称、描述、相关性评分）
  - 排序选项（按相关性、使用频率、更新时间）
  - 分页控制（每页显示数量可配置）
  - **工作量**: 1.5天
  - **验收标准**: 搜索响应快速（< 100ms），结果准确

- [ ] **[TASK-2.2.27.2] Skill Detail Modal**: Skill 详情模态框 (`packages/app/src/app/components/skill-detail-modal.tsx`)
  - Skill 元数据展示（名称、描述、标签、优先级、版本）
  - Skill 内容预览（Markdown 渲染）
  - 代码示例高亮（语法高亮）
  - 使用统计（使用次数、最后使用时间）
  - 复制按钮（复制 Skill 内容）
  - **工作量**: 1天
  - **验收标准**: 详情展示完整，内容可读性好

- [ ] **[TASK-2.2.27.3] Context Builder UI**: 上下文构建器界面 (`packages/app/src/app/components/context-builder.tsx`)
  - 查询输入框（输入需求描述）
  - Token 限制设置（滑块控制 max_tokens）
  - 选中的 Skills 列表（显示将要使用的 Skills）
  - 上下文预览（显示构建后的上下文内容）
  - Token 使用统计（显示当前使用的 Token 数量）
  - 构建按钮（触发上下文构建）
  - **工作量**: 1.5天
  - **验收标准**: Token 控制准确，预览清晰

- [ ] **[TASK-2.2.27.4] Skills Stats Dashboard**: Skills 使用统计仪表板 (`packages/app/src/app/components/skills-stats.tsx`)
  - 使用频率图表（柱状图或折线图）
  - 热门 Skills Top 10（排行榜）
  - 使用趋势分析（时间序列图）
  - 标签分布（饼图或词云）
  - **工作量**: 1天
  - **验收标准**: 图表清晰，数据准确

- [ ] **[TASK-2.2.27.5] Skills Management Panel**: Skills 管理面板 (`packages/app/src/app/pages/skills-management.tsx`)
  - Skills 加载状态（显示已加载的 Skills 数量）
  - 缓存统计（缓存命中率、缓存大小）
  - 重新加载按钮（手动触发 Skills 重新加载）
  - 清除缓存按钮（清除 Skills 缓存）
  - 扫描日志（显示 Skills 扫描日志）
  - **工作量**: 1天
  - **验收标准**: 管理功能完整，操作响应快速

- [ ] **[TASK-2.2.27.6] Archival Assets Viewer**: 归档资产查看器 (`packages/app/src/app/pages/archival-assets.tsx`)
  - 归档资产列表（表格形式，显示资产类型、名称、需求ID、时间）
  - 按需求ID查询（输入需求ID查询相关归档）
  - 资产预览（点击查看资产详情）
  - 资产下载（下载归档资产）
  - 资产搜索（关键词搜索归档资产）
  - **工作量**: 1.5天
  - **验收标准**: 查询快速，预览清晰

- [ ] **[TASK-2.2.27.7] Code Snippets Library**: 代码片段库 (`packages/app/src/app/pages/code-snippets.tsx`)
  - 代码片段列表（卡片形式，显示片段名称、语言、标签）
  - 分类浏览（按语言、标签分类）
  - 代码片段搜索（关键词搜索）
  - 代码片段预览（语法高亮）
  - 复制按钮（一键复制代码）
  - **工作量**: 1天
  - **验收标准**: 浏览流畅，复制方便

- [ ] **[TASK-2.2.27.8] Best Practice Recommender**: 最佳实践推荐组件 (`packages/app/src/app/components/best-practice-recommender.tsx`)
  - 推荐卡片（显示推荐的最佳实践）
  - 使用场景说明（说明适用场景）
  - 相关链接（链接到详细文档）
  - 示例代码（显示示例代码）
  - 采纳按钮（标记为已采纳）
  - **工作量**: 1天
  - **验收标准**: 推荐准确，内容有用

- [ ] **[TASK-2.2.28] Documentation**: 文档编写 (`docs/SKILLS_RAG_GUIDE.md`)
  - Skills 编写指南
  - Skills 最佳实践
  - API 使用文档
  - 故障排查指南
  - **验收标准**: 文档完整，新用户可快速上手

#### 2.2.6 Superpower Archival System (Superpower 归档系统) 🆕
- [ ] **[TASK-2.2.29] Archival Data Model**: 归档数据模型 (`backend/app/superpower/archival_models.py`)
  - 定义 `ArchivedAsset` 模型（代码片段、文档、测试用例）
  - 元数据：需求ID、任务ID、开发者、时间戳、标签
  - 关联关系：需求 -> OpenSpec -> 任务 -> 归档资产
  - **工作量**: 0.5天
  - **验收标准**: 模型定义完整，支持序列化

- [ ] **[TASK-2.2.30] Archival Service**: 归档服务 (`backend/app/superpower/archival_service.py`)
  - 归档代码片段到 Skills 库
  - 归档设计文档到文档库
  - 归档测试用例到测试库
  - 更新向量数据库索引
  - **工作量**: 1天
  - **验收标准**: 归档内容可被后续检索使用

- [ ] **[TASK-2.2.31] Archival Workflow Integration**: 归档工作流集成 (`backend/app/workflow/archival_workflow.py`)
  - 集成到 OpenSpec 任务完成流程
  - 任务状态变为 "completed" 时触发归档
  - 自动提取代码片段、文档、最佳实践
  - 生成归档报告
  - **工作量**: 1天
  - **验收标准**: 任务完成自动触发归档，成功率 > 95%

- [ ] **[TASK-2.2.32] Archival API**: 归档 API (`backend/main.py`)
  - `POST /archival/archive` - 手动触发归档
  - `GET /archival/assets` - 查询归档资产
  - `GET /archival/by-requirement/{id}` - 按需求ID查询归档
  - **工作量**: 0.5天
  - **验收标准**: API 响应时间 < 100ms

#### 2.3 Code Generation & Development (代码生成与开发) 🆕 **核心功能**

##### 2.3.1 Code Generation (代码生成)
- [ ] **[TASK-2.3.1] Code Generator Core**: 代码生成器核心 (`backend/app/codegen/generator.py`) 🆕
  - 基于 OpenSpec 生成代码骨架
  - 基于 Skills 生成符合规范的代码
  - 支持增量生成（只生成变更部分）
  - 生成测试用例
  - 支持多种语言（Python, TypeScript, Vue, etc.）
  - **工作量**: 3天 🆕 **调整** (原 2天)
  - **验收标准**: 生成的代码符合规范，可编译运行，准确率 > 80%

- [ ] **[TASK-2.3.2] Code Template Engine**: 代码模板引擎 (`backend/app/codegen/template_engine.py`) 🆕
  - 预置代码模板（Controller, Service, Model, Component, etc.）
  - 模板变量替换（Jinja2）
  - 模板继承和组合
  - 自定义模板支持
  - **工作量**: 1天
  - **验收标准**: 支持 10+ 常用模板，模板渲染准确

##### 2.3.2 Code Change Management (代码变更管理)
- [ ] **[TASK-2.3.3] Code Change Tracker**: 代码变更追踪器 (`backend/app/codegen/change_tracker.py`) 🆕
  - 记录所有代码变更（文件、行号、内容）
  - 生成 Diff 报告（unified diff 格式）
  - 变更原因说明（AI 生成）
  - 撤销/重做功能
  - 变更历史记录
  - **工作量**: 1.5天
  - **验收标准**: 变更记录完整，Diff 准确，可撤销/重做

- [ ] **[TASK-2.3.4] Code Review UI**: 代码审查界面 (`packages/app/src/app/pages/code-review.tsx`) 🆕
  - Diff 可视化展示（Monaco Diff Editor）
  - 文件树展示（变更文件列表）
  - 代码高亮和语法检查
  - 评论和标注功能
  - 接受/拒绝变更
  - **工作量**: 2天
  - **验收标准**: UI 清晰，交互流畅，可查看所有变更

##### 2.3.3 Local Development Environment (本地开发环境)
- [ ] **[TASK-2.3.5] Dev Environment Manager**: 开发环境管理器 (`backend/app/devenv/manager.py`) 🆕
  - 项目启动/停止（npm run dev, python main.py, etc.）
  - 进程管理（启动、停止、重启、状态查询）
  - 端口管理和冲突检测
  - 环境变量配置和管理
  - 多项目支持（前端 + 后端同时启动）
  - **工作量**: 3天 🆕 **调整** (原 2天)
  - **验收标准**: 可启动/停止项目，端口管理准确，进程状态实时

- [ ] **[TASK-2.3.6] Hot Reload Support**: 热重载支持 (`backend/app/devenv/hot_reload.py`) 🆕
  - 文件变更监听（watchdog）
  - 自动重启服务（后端）
  - 浏览器自动刷新（前端）
  - 增量编译支持
  - **工作量**: 1天
  - **验收标准**: 代码变更后自动生效，延迟 < 2s

- [ ] **[TASK-2.3.7] Log Viewer**: 日志查看器 (`packages/app/src/app/components/log-viewer.tsx`) 🆕
  - 实时日志流（WebSocket）
  - 日志过滤和搜索
  - 日志级别高亮（ERROR, WARN, INFO, DEBUG）
  - 错误追踪和堆栈展示
  - 日志导出功能
  - **工作量**: 1.5天
  - **验收标准**: 日志实时显示，过滤准确，性能良好

##### 2.3.4 Manual Testing Tools (手动测试工具)
- [ ] **[TASK-2.3.8] Test Case Manager**: 测试用例管理器 (`backend/app/testing/test_case_manager.py`) 🆕
  - 测试用例列表（CRUD）
  - 测试用例执行
  - 测试结果记录
  - 测试报告生成
  - 测试覆盖率统计
  - **工作量**: 1.5天
  - **验收标准**: 可管理和执行测试用例，报告清晰

- [ ] **[TASK-2.3.9] Manual Test UI**: 手动测试界面 (`packages/app/src/app/pages/manual-test.tsx`) 🆕
  - API 测试工具（类似 Postman）
  - 请求构建器（URL, Method, Headers, Body）
  - 响应查看器（JSON, HTML, etc.）
  - 测试数据管理
  - 测试历史记录
  - **工作量**: 2天
  - **验收标准**: 可手动测试 API，功能完整

##### 2.3.5 Debug Support (调试支持)
- [ ] **[TASK-2.3.10] Debug Integration**: 调试集成 (`backend/app/devenv/debug_integration.py`) 🆕
  - VS Code Debug 配置生成
  - 断点管理
  - 变量查看
  - 调用栈追踪
  - Debug Adapter Protocol (DAP) 支持
  - **工作量**: 1.5天
  - **验收标准**: 可在 VS Code 中调试，断点准确

- [ ] **[TASK-2.3.11] Error Tracker**: 错误追踪器 (`backend/app/devenv/error_tracker.py`) 🆕
  - 运行时错误捕获
  - 错误堆栈展示
  - 错误统计和分析
  - 错误分类（语法错误、运行时错误、逻辑错误）
  - 错误修复建议（AI 生成）
  - **工作量**: 1天
  - **验收标准**: 错误捕获准确，堆栈清晰，建议有用

##### 2.3.6 Integration & Testing (集成与测试)
- [ ] **[TASK-2.3.12] Code Generation API**: 代码生成 API (`backend/main.py`) 🆕
  - `POST /codegen/generate` - 生成代码
  - `GET /codegen/changes` - 查询代码变更
  - `POST /codegen/apply` - 应用代码变更
  - `POST /codegen/rollback` - 回滚代码变更
  - **工作量**: 1天
  - **验收标准**: API 响应时间 < 500ms

- [ ] **[TASK-2.3.13] Dev Environment API**: 开发环境 API (`backend/main.py`) 🆕
  - `POST /devenv/start` - 启动项目
  - `POST /devenv/stop` - 停止项目
  - `GET /devenv/status` - 查询状态
  - `GET /devenv/logs` - 获取日志（SSE）
  - **工作量**: 1天
  - **验收标准**: API 响应时间 < 200ms，日志实时

- [ ] **[TASK-2.3.14] Unit Tests**: 单元测试 (`backend/tests/test_codegen_*.py`) 🆕
  - Code Generator 测试
  - Change Tracker 测试
  - Dev Environment Manager 测试
  - **工作量**: 1天
  - **验收标准**: 测试覆盖率 > 80%

- [ ] **[TASK-2.3.15] Integration Tests**: 集成测试 (`backend/tests/test_integration_codegen.py`) 🆕
  - 端到端测试：OpenSpec → 代码生成 → 本地运行
  - 代码变更测试
  - 热重载测试
  - **工作量**: 1天
  - **验收标准**: 集成测试通过

##### 2.3.7 Code Generation Frontend UI (代码生成前端 UI) 🆕 ⚠️ **关键缺失**

- [ ] **[TASK-2.3.16] Code Generation UI**: 代码生成界面 (`packages/app/src/app/pages/code-generation.tsx`)
  - 生成配置面板（选择语言、框架、模板）
  - 生成进度显示（进度条、当前步骤）
  - 生成日志实时显示（显示生成过程日志）
  - 生成结果预览（文件树、代码预览）
  - 应用/取消按钮（应用生成的代码或取消）
  - **工作量**: 2天
  - **验收标准**: 生成流程清晰，进度实时，预览准确

- [ ] **[TASK-2.3.17] Code Change Viewer**: 代码变更查看器 (`packages/app/src/app/pages/code-review.tsx`)
  - 文件树展示（显示所有变更文件，标注新增/修改/删除）
  - Diff 可视化（Monaco Diff Editor，并排对比）
  - 变更统计（显示新增/删除/修改的文件数和行数）
  - 变更原因说明（AI 生成的变更说明）
  - 文件过滤（按文件类型、变更类型过滤）
  - **工作量**: 2天
  - **验收标准**: Diff 清晰，统计准确，过滤有效

- [ ] **[TASK-2.3.18] Code Change Actions**: 代码变更操作组件 (`packages/app/src/app/components/code-change-actions.tsx`)
  - 接受变更按钮（接受当前文件的变更）
  - 拒绝变更按钮（拒绝当前文件的变更）
  - 批量操作（接受/拒绝所有变更）
  - 评论功能（对变更添加评论）
  - 标注功能（标注需要注意的地方）
  - **工作量**: 1天
  - **验收标准**: 操作响应快速，批量操作安全

- [ ] **[TASK-2.3.19] Dev Environment Dashboard**: 开发环境仪表板 (`packages/app/src/app/pages/dev-environment.tsx`)
  - 项目状态卡片（显示前端/后端项目状态：运行中/已停止）
  - 启动/停止按钮（控制项目启动和停止）
  - 进程信息（显示进程 PID、端口、资源使用）
  - 端口管理（显示占用的端口，检测冲突）
  - 环境变量配置（查看和编辑环境变量）
  - 快速操作（重启、清除缓存、查看日志）
  - **工作量**: 2.5天 🆕 **调整** (原 2天)
  - **验收标准**: 状态实时，操作可靠，信息完整

- [ ] **[TASK-2.3.20] Hot Reload Indicator**: 热重载状态指示器 (`packages/app/src/app/components/hot-reload-indicator.tsx`)
  - 重载状态显示（显示"正在重载"、"重载成功"、"重载失败"）
  - 自动刷新指示（显示浏览器自动刷新倒计时）
  - 延迟显示（显示重载延迟时间）
  - 错误提示（重载失败时显示错误信息）
  - **工作量**: 0.5天
  - **验收标准**: 状态准确，提示及时

- [ ] **[TASK-2.3.21] Log Viewer Enhancement**: 日志查看器增强 (`packages/app/src/app/pages/log-viewer.tsx` 更新)
  - 多项目日志切换（切换查看前端/后端日志）
  - 日志级别过滤（ERROR/WARN/INFO/DEBUG）
  - 日志搜索（关键词搜索，支持正则）
  - 日志高亮（ERROR 红色，WARN 黄色，INFO 蓝色，DEBUG 灰色）
  - 错误堆栈展示（点击错误查看完整堆栈）
  - 日志导出（导出为文本文件）
  - 自动滚动（新日志自动滚动到底部）
  - **工作量**: 1.5天
  - **验收标准**: 过滤准确，搜索快速，高亮清晰

- [ ] **[TASK-2.3.22] Error Stack Viewer**: 错误堆栈查看器 (`packages/app/src/app/components/error-stack-viewer.tsx`)
  - 堆栈展示（可折叠的堆栈列表）
  - 源代码链接（点击跳转到源代码位置）
  - 堆栈追踪（显示完整的调用链）
  - 错误上下文（显示错误发生时的上下文信息）
  - **工作量**: 1天
  - **验收标准**: 堆栈清晰，链接准确

- [ ] **[TASK-2.3.23] Manual Test Tool Enhancement**: 手动测试工具增强 (`packages/app/src/app/pages/manual-test.tsx` 更新)
  - 请求构建器（URL、Method、Headers、Body 编辑）
  - 环境变量支持（使用 {{variable}} 语法）
  - 请求历史（保存最近的请求）
  - 响应查看器（JSON 格式化、HTML 渲染、图片预览）
  - 响应时间统计（显示请求耗时）
  - 批量测试（批量执行多个请求）
  - **工作量**: 2天
  - **验收标准**: 功能完整，类似 Postman

- [ ] **[TASK-2.3.24] Test Case Manager UI**: 测试用例管理界面 (`packages/app/src/app/pages/test-case-manager.tsx`)
  - 测试用例列表（表格形式，显示用例名称、状态、最后执行时间）
  - 用例编辑器（创建/编辑测试用例）
  - 用例执行（单个执行或批量执行）
  - 执行结果展示（显示通过/失败，失败原因）
  - 测试报告（生成测试报告，显示覆盖率）
  - **工作量**: 2天
  - **验收标准**: 管理完整，执行可靠，报告清晰

- [ ] **[TASK-2.3.25] Test Report Component**: 测试报告组件 (`packages/app/src/app/components/test-report.tsx`)
  - 覆盖率图表（显示代码覆盖率）
  - 失败用例列表（显示失败的测试用例）
  - 性能指标（显示测试执行时间）
  - 趋势分析（显示测试通过率趋势）
  - 导出报告（导出为 HTML/PDF）
  - **工作量**: 1天
  - **验收标准**: 报告完整，图表清晰

- [ ] **[TASK-2.3.26] Debug Panel**: 调试面板 (`packages/app/src/app/pages/debug-panel.tsx`)
  - 断点管理（添加/删除/启用/禁用断点）
  - 变量查看（查看当前作用域的变量）
  - 调用栈展示（显示当前调用栈）
  - 调试控制（继续、单步执行、单步进入、单步跳出）
  - VS Code 集成（一键在 VS Code 中打开调试）
  - **工作量**: 2天
  - **验收标准**: 调试功能完整，与 VS Code 集成顺畅

- [ ] **[TASK-2.3.27] Error Tracker UI**: 错误追踪器界面 (`packages/app/src/app/pages/error-tracker.tsx`)
  - 错误列表（表格形式，显示错误类型、消息、时间、频率）
  - 错误分类（语法错误、运行时错误、逻辑错误）
  - 错误详情（点击查看完整错误信息和堆栈）
  - 错误统计（显示错误数量趋势）
  - 错误修复建议（AI 生成的修复建议）
  - 标记已修复（标记错误为已修复）
  - **工作量**: 1.5天
  - **验收标准**: 错误追踪准确，分类清晰，建议有用

- [ ] **[TASK-2.3.28] Error Fix Suggestion Component**: 错误修复建议组件 (`packages/app/src/app/components/error-fix-suggestion.tsx`)
  - 建议卡片（显示 AI 生成的修复建议）
  - 代码示例（显示修复后的代码示例）
  - 应用按钮（一键应用修复建议）
  - 反馈按钮（标记建议是否有用）
  - **工作量**: 1天
  - **验收标准**: 建议准确，应用安全

- [ ] **[TASK-2.3.29] Dev Environment Status Widget**: 开发环境状态小部件 (`packages/app/src/app/components/dev-environment-dashboard.tsx`)
  - 综合状态显示（显示所有项目的运行状态）
  - 快速操作按钮（快速启动/停止/重启）
  - 性能监控（CPU、内存、网络使用）
  - 告警提示（资源使用过高时告警）
  - **工作量**: 1天
  - **验收标准**: 状态实时，操作便捷，监控准确

#### 2.4 Agent System (智能体系统)
- [x] **[TASK-2.4.1] Basic Agent Swarm**: 基础智能体编排 (`backend/app/agent_swarm.py`)
  - `AgentSwarm` 类
  - `generate_spec()` 方法（Mock 实现）
  - 简单的 PM/Architect 逻辑
  - **验收标准**: 可生成基本的 OpenSpec（Mock 数据）

- [ ] **[TASK-2.4.2] LLM Integration**: LLM 集成 (`backend/app/llm/client.py`)
  - OpenAI API 客户端
  - Anthropic API 客户端
  - 统一的 LLM 接口
  - **验收标准**: 可调用多个 LLM 提供商，接口统一

- [ ] **[TASK-2.4.3] Prompt Templates**: 提示词模板 (`backend/app/prompts/`)
  - PM Agent 提示词模板
  - Architect Agent 提示词模板
  - Developer Agent 提示词模板
  - **验收标准**: 至少 3 个模板，可参数化

- [ ] **[TASK-2.4.4] Real Agent Implementation**: 真实智能体实现 (`backend/app/agent_swarm.py` 增强)
  - 调用 LLM 生成需求分析
  - 调用 LLM 生成架构设计
  - 注入 RAG 上下文
  - **验收标准**: 生成的 OpenSpec 质量高，符合需求

#### 2.6 Phase 2 Task Dependencies (任务依赖关系) 📊 🆕

```mermaid
graph TD
    %% Context Server
    A[TASK-2.1.1 Basic Context Server] --> B[TASK-2.1.2 Skills Loader]

    %% Skills-based RAG - Skills Loader
    B --> C[TASK-2.2.1 Skill Model]
    C --> D[TASK-2.2.2 Markdown Parser]
    D --> E[TASK-2.2.3 Skills Scanner]
    E --> F[TASK-2.2.4 Skills Loader Core]
    F --> G[TASK-2.2.5 Skills Loader API]

    %% Skills-based RAG - Skills Retriever
    F --> H[TASK-2.2.6 Keyword Matcher]
    F --> I[TASK-2.2.7 Tag Filter]
    F --> J[TASK-2.2.8 Fuzzy Matcher]
    H --> K[TASK-2.2.9 Relevance Scorer]
    I --> K
    J --> K
    K --> L[TASK-2.2.10 Skills Retriever Core]
    L --> M[TASK-2.2.11 Skills Retriever API]

    %% Skills-based RAG - Context Builder
    L --> N[TASK-2.2.12 Token Counter]
    L --> O[TASK-2.2.13 Content Truncator]
    L --> P[TASK-2.2.14 Priority Sorter]
    N --> Q[TASK-2.2.15 Context Composer]
    O --> Q
    P --> Q
    Q --> R[TASK-2.2.16 Skills Context Builder Core]
    R --> S[TASK-2.2.17 Context Builder API]

    %% Skills Templates (并行)
    F --> T1[TASK-2.2.18 Coding Standards Skill]
    F --> T2[TASK-2.2.19 Framework Docs Skill]
    F --> T3[TASK-2.2.20 Best Practices Skill]
    F --> T4[TASK-2.2.21 Common Solutions Skill]

    %% Integration & Testing
    S --> U[TASK-2.2.22 Agent Integration]
    T1 --> U
    T2 --> U
    T3 --> U
    T4 --> U
    U --> V[TASK-2.2.23 Context Injection]
    V --> W[TASK-2.2.24 Skills Cache]
    W --> X[TASK-2.2.25 Unit Tests]
    X --> Y[TASK-2.2.26 Integration Tests]
    Y --> Z[TASK-2.2.27 Frontend Integration]

    %% Code Generation (并行开始)
    R --> CG1[TASK-2.3.1 Code Generator Core]
    R --> CG2[TASK-2.3.2 Code Template Engine]
    CG1 --> CG3[TASK-2.3.3 Code Change Tracker]
    CG2 --> CG3
    CG3 --> CG4[TASK-2.3.4 Code Review UI]

    %% Local Dev Environment (并行)
    CG3 --> DE1[TASK-2.3.5 Dev Environment Manager]
    CG3 --> DE2[TASK-2.3.6 Hot Reload Support]
    CG3 --> DE3[TASK-2.3.7 Log Viewer]

    %% Testing Tools (并行)
    DE1 --> TT1[TASK-2.3.8 Test Case Manager]
    DE1 --> TT2[TASK-2.3.9 Manual Test UI]

    %% Debug Support (并行)
    DE1 --> DB1[TASK-2.3.10 Debug Integration]
    DE1 --> DB2[TASK-2.3.11 Error Tracker]

    %% Integration & Testing
    TT1 --> IT1[TASK-2.3.12 Code Generation API]
    TT2 --> IT1
    DB1 --> IT1
    DB2 --> IT1
    IT1 --> IT2[TASK-2.3.13 Dev Environment API]
    IT2 --> IT3[TASK-2.3.14 Unit Tests]
    IT3 --> IT4[TASK-2.3.15 Integration Tests]

    %% LLM Integration
    V --> LLM1[TASK-2.4.2 LLM Integration]
    LLM1 --> LLM2[TASK-2.4.3 Prompt Templates]
    LLM2 --> LLM3[TASK-2.4.4 Real Agent Implementation]

    %% 关键路径标注
    style A fill:#ff6b6b
    style F fill:#ff6b6b
    style L fill:#ff6b6b
    style R fill:#ff6b6b
    style U fill:#ff6b6b
    style CG1 fill:#ff6b6b
    style IT4 fill:#ff6b6b

    %% 并行任务组标注
    style H fill:#90EE90
    style I fill:#90EE90
    style J fill:#90EE90

    style N fill:#87CEEB
    style O fill:#87CEEB
    style P fill:#87CEEB

    style T1 fill:#FFD700
    style T2 fill:#FFD700
    style T3 fill:#FFD700
    style T4 fill:#FFD700

    style CG1 fill:#FFA500
    style CG2 fill:#FFA500

    style DE1 fill:#DDA0DD
    style DE2 fill:#DDA0DD
    style DE3 fill:#DDA0DD

    style TT1 fill:#F0E68C
    style TT2 fill:#F0E68C

    style DB1 fill:#98FB98
    style DB2 fill:#98FB98
```

**并行任务组**:
- ✅ **组 A** (可并行): TASK-2.2.6, 2.2.7, 2.2.8 (Keyword/Tag/Fuzzy Matcher)
- ✅ **组 B** (可并行): TASK-2.2.12, 2.2.13, 2.2.14 (Token/Truncator/Sorter)
- ✅ **组 C** (可并行): TASK-2.2.18, 2.2.19, 2.2.20, 2.2.21 (Skills Templates)
- ✅ **组 D** (可并行): TASK-2.3.1, 2.3.2 (Code Generator + Template Engine)
- ✅ **组 E** (可并行): TASK-2.3.5, 2.3.6, 2.3.7 (Dev Environment + Hot Reload + Log Viewer)
- ✅ **组 F** (可并行): TASK-2.3.8, 2.3.9 (Test Case Manager + Manual Test UI)
- ✅ **组 G** (可并行): TASK-2.3.10, 2.3.11 (Debug Integration + Error Tracker)

**关键路径** (Critical Path):
```
A → B → C → D → E → F → L → R → U → CG1 → CG3 → DE1 → IT1 → IT2 → IT3 → IT4
总工期: 约 26 天（考虑并行开发）
```

**工期优化建议**:
- 并行开发组 C (Skills Templates): 节省 3 天
- 并行开发组 D (Code Generation): 节省 1 天
- 并行开发组 E (Dev Environment): 节省 2 天
- 并行开发组 F-G (Testing & Debug): 节省 2 天
- **总节省**: 约 8 天

#### 2.5 Editor Integration (编辑器集成)
- [x] **[TASK-2.5.1] VS Code IPC**: VS Code IPC 基础 (`backend/app/editor_ipc.py`)
  - `EditorIPC` 类
  - `open_file()` 方法
  - `apply_file_edits()` 方法
  - **验收标准**: 可打开 VS Code 文件，可应用编辑

- [ ] **[TASK-2.5.2] File Watcher**: 文件监听器 (`backend/app/editor/file_watcher.py`)
  - 监听项目文件变更
  - 触发增量索引
  - 通知前端更新
  - **验收标准**: 文件变更延迟 < 1s，准确率 100%

- [ ] **[TASK-2.5.3] Code Analysis**: 代码分析器 (`backend/app/editor/code_analyzer.py`)
  - AST 解析（Python, TypeScript）
  - 提取函数、类、接口定义
  - 依赖关系分析
  - **验收标准**: 准确提取代码结构，支持主流语言

- [ ] **[TASK-2.5.4] Diff Generator**: 差异生成器 (`backend/app/editor/diff_generator.py`)
  - 生成 unified diff 格式
  - 支持多文件差异
  - 差异预览
  - **验收标准**: 生成的差异可直接应用，格式正确

### Phase 3: Enterprise Integration (企业集成) 🔥 P0
**目标**: 深度集成 TFS/Azure DevOps 和企业工作流
**周期**: Week 5 (5 工作日)
**状态**: ⚠️ 基础完成，需增强

#### 3.1 TFS MCP Server (TFS MCP 服务器)
- [x] **[TASK-3.1.1] TFS Client**: TFS 客户端 (`backend/app/tfs_mcp.py`)
  - `TfsClient` 类（Mock 实现）
  - `list_work_items()` 方法
  - `get_work_item()` 方法
  - `create_work_item()` 方法
  - `trigger_build()` 方法
  - **验收标准**: API 可调用（Mock 数据）

- [ ] **[TASK-3.1.2] Real TFS Integration**: 真实 TFS 集成 (`backend/app/tfs_mcp.py` 增强)
  - 使用 `azure-devops` Python SDK
  - 实现真实的 REST API 调用
  - 错误处理和重试机制
  - **验收标准**: 可连接真实 TFS 实例，API 调用成功率 > 99%

- [ ] **[TASK-3.1.3] Requirement Query by ID**: 需求ID查询 (`backend/app/tfs/requirement_query.py`) 🆕
  - 输入需求ID，查询TFS需求详情
  - 解析需求内容、描述、附件、关联任务
  - 提取验收标准和优先级
  - 缓存查询结果
  - **工作量**: 1天
  - **验收标准**: 可通过需求ID获取完整需求信息，延迟 < 500ms

- [ ] **[TASK-3.1.4] Work Item Sync**: Work Item 同步 (`backend/app/tfs/work_item_sync.py`)
  - 双向同步 OpenSpec 和 Work Item
  - 冲突检测和解决
  - 同步历史记录
  - **验收标准**: 同步准确，冲突可手动解决

- [ ] **[TASK-3.1.5] Code Commit to TFS**: 代码提交到TFS (`backend/app/tfs/code_commit.py`) 🆕
  - 开发完成后，自动创建 Git 分支
  - 提交代码到 TFS Git 仓库
  - 关联需求ID到提交记录（commit message）
  - 支持批量提交多个文件
  - **工作量**: 1天
  - **验收标准**: 代码可提交到TFS，关联需求ID，成功率 > 99%

- [ ] **[TASK-3.1.6] Pull Request Automation**: Pull Request 自动化 (`backend/app/tfs/pull_request.py`) 🆕
  - 自动创建 Pull Request
  - 关联需求ID和工作项
  - 设置审查者（基于团队配置）
  - 触发代码审查流程
  - **工作量**: 1天
  - **验收标准**: PR 自动创建，审查流程启动，成功率 > 95%

- [ ] **[TASK-3.1.7] Build Integration**: 构建集成 (`backend/app/tfs/build_integration.py`)
  - 触发 TFS 构建流水线
  - 监听构建状态
  - 构建失败通知
  - **验收标准**: 构建触发成功率 > 99%，状态实时更新

#### 3.1.8 TFS API Endpoints (TFS API 端点) 🆕

**需求查询 API**:
```
GET  /tfs/requirements/{id}              - 查询需求详情
GET  /tfs/requirements/{id}/attachments  - 查询需求附件
GET  /tfs/requirements/{id}/tasks        - 查询关联任务
GET  /tfs/requirements/search            - 搜索需求
```

**代码提交 API**:
```
POST /tfs/commit                         - 提交代码到 TFS
POST /tfs/pull-request                   - 创建 Pull Request
GET  /tfs/pull-request/{id}              - 查询 PR 状态
PUT  /tfs/pull-request/{id}              - 更新 PR
GET  /tfs/pull-request/{id}/comments     - 获取 PR 评论
```

**构建监控 API**:
```
POST /tfs/build/trigger                  - 触发构建
GET  /tfs/build/{id}/status              - 查询构建状态
GET  /tfs/build/{id}/logs                - 获取构建日志（SSE）
GET  /tfs/build/history                  - 获取构建历史
```

**Work Item API**:
```
GET  /tfs/work-items                     - 列出 Work Items
GET  /tfs/work-items/{id}                - 获取 Work Item 详情
POST /tfs/work-items/{id}/sync           - 同步 Work Item
PUT  /tfs/work-items/{id}                - 更新 Work Item
```

**Session 管理 API**:
```
POST /sessions/{session_id}/bind-requirement  - 绑定需求ID
GET  /sessions/by-requirement/{requirement_id} - 查询需求的所有Session
POST /sessions/{session_id}/replay            - 重放历史Session
GET  /sessions/{session_id}/context           - 获取Session上下文
```

#### 3.2 Authentication (认证系统)
- [x] **[TASK-3.2.1] TFS Auth Client**: TFS 认证客户端 (`backend/app/tfs_auth.py`)
  - `TfsAuthClient` 类
  - PAT 认证实现
  - OAuth 2.0 认证实现
  - Token 存储和管理
  - **验收标准**: 支持 PAT 和 OAuth，Token 安全存储

- [ ] **[TASK-3.2.2] Token Refresh**: Token 自动刷新 (`backend/app/tfs_auth.py` 增强)
  - 检测 Token 过期
  - 自动刷新 OAuth Token
  - 刷新失败重新登录
  - **验收标准**: Token 过期前自动刷新，用户无感知

- [ ] **[TASK-3.2.3] Multi-Org Support**: 多组织支持 (`backend/app/tfs/org_manager.py`)
  - 支持多个 TFS 组织
  - 组织切换
  - 组织级别配置
  - **验收标准**: 可管理多个组织，切换流畅

- [ ] **[TASK-3.2.4] SSO Integration**: SSO 集成 (`backend/app/auth/sso.py`)
  - Azure AD 集成
  - SAML 2.0 支持（可选）
  - 单点登录流程
  - **验收标准**: 支持企业 SSO，登录流程顺畅

#### 3.3 Check-in Guard (提交守卫)
- [x] **[TASK-3.3.1] Basic Check-in Guard**: 基础提交守卫 (`backend/app/checkin_guard.py`)
  - `CheckinGuard` 类
  - Lint 检查（Mock）
  - Type 检查（Mock）
  - Unit Test 检查（Mock）
  - **验收标准**: 检查流程可执行（Mock 实现）

- [ ] **[TASK-3.3.2] Real Linter Integration**: 真实 Linter 集成 (`backend/app/checkin/linter.py`)
  - ESLint 集成（JavaScript/TypeScript）
  - Pylint 集成（Python）
  - 自定义规则配置
  - **验收标准**: 可执行真实 Linter，准确报告错误

- [ ] **[TASK-3.3.3] Real Test Runner**: 真实测试执行器 (`backend/app/checkin/test_runner.py`)
  - pytest 集成（Python）
  - jest/vitest 集成（JavaScript/TypeScript）
  - 测试覆盖率统计
  - **验收标准**: 可执行真实测试，报告清晰

- [ ] **[TASK-3.3.4] Pre-commit Hooks**: Pre-commit Hooks 集成 (`backend/app/checkin/hooks.py`)
  - Git pre-commit hook 安装
  - Hook 配置管理
  - Hook 执行日志
  - **验收标准**: Hook 自动执行，阻止不合规提交

#### 3.4 Session Sync (会话同步)
- [x] **[TASK-3.4.1] Basic Session Sync**: 基础会话同步 (`backend/app/session_sync.py`)
  - `SessionSyncService` 类
  - 内存存储实现
  - `save_session()` 方法
  - `load_session()` 方法
  - `create_share_link()` 方法
  - **验收标准**: 会话可保存和加载（内存实现）

- [ ] **[TASK-3.4.2] Redis Storage**: Redis 存储 (`backend/app/session/redis_storage.py`)
  - 连接到 Redis 实例
  - 会话数据序列化
  - TTL 管理
  - **验收标准**: 会话可持久化到 Redis，支持过期

- [ ] **[TASK-3.4.3] Session History**: 会话历史 (`backend/app/session/history.py`)
  - 记录会话变更历史
  - 支持回滚到历史版本
  - 历史查询和过滤
  - **验收标准**: 历史记录完整，可回滚

- [ ] **[TASK-3.4.4] Session Sharing**: 会话分享增强 (`backend/app/session/sharing.py`)
  - 分享链接权限控制
  - 分享链接过期时间
  - 分享统计和追踪
  - **验收标准**: 分享链接安全，权限可控

- [ ] **[TASK-3.4.5] Session-Requirement Binding**: Session与需求ID绑定 (`backend/app/session/requirement_binding.py`) 🆕
  - Session 创建时绑定 TFS 需求ID
  - 存储 Session 与需求ID的映射关系（Redis）
  - 支持一个需求关联多个 Session（迭代开发）
  - 元数据：需求ID、Session ID、开发者、创建时间、状态
  - **工作量**: 1天
  - **验收标准**: Session 与需求ID强绑定，映射关系持久化

- [ ] **[TASK-3.4.6] Session History Query**: Session 历史查询 (`backend/app/session/history_query.py`) 🆕
  - 提供 API: `GET /sessions/by-requirement/{requirement_id}`
  - 返回该需求的所有开发 Session
  - 包含 Session 详情、开发者、时间、状态、OpenSpec
  - 支持分页和过滤（按时间、开发者、状态）
  - **工作量**: 1天
  - **验收标准**: 可查询需求的完整开发历史，响应时间 < 200ms

- [ ] **[TASK-3.4.7] Session Replay for Bug Fix**: Session 重放用于Bug修复 (`backend/app/session/replay.py`) 🆕
  - 其他开发者可以加载历史 Session
  - 查看原始需求、设计决策、代码变更
  - 恢复 Session 上下文（OpenSpec、Skills、代码状态）
  - 用于 Bug 修复或功能迭代
  - **工作量**: 1.5天
  - **验收标准**: 可重现历史开发过程，上下文加载准确率 > 95%

- [ ] **[TASK-3.4.8] Session Binding API**: Session 绑定 API (`backend/main.py`) 🆕
  - `POST /sessions/{session_id}/bind-requirement` - 绑定需求ID
  - `GET /sessions/by-requirement/{requirement_id}` - 查询需求的所有Session
  - `POST /sessions/{session_id}/replay` - 重放历史Session
  - **工作量**: 0.5天
  - **验收标准**: API 响应时间 < 100ms

#### 3.5 TFS & Session Frontend UI (TFS 与 Session 前端 UI) 🆕 ⚠️ **缺失**

##### 3.5.1 TFS Integration UI (TFS 集成 UI)

- [ ] **[TASK-3.5.1] Requirement Query UI**: 需求ID查询界面 (`packages/app/src/app/pages/requirement-query.tsx`)
  - 需求ID输入框（输入 TFS 需求ID）
  - 查询按钮（触发查询）
  - 需求详情卡片（显示需求标题、描述、状态、优先级）
  - 验收标准展示（显示验收标准列表）
  - 附件列表（显示需求附件）
  - 关联任务（显示关联的子任务）
  - 创建 OpenSpec 按钮（基于需求创建 OpenSpec）
  - **工作量**: 1.5天
  - **验收标准**: 查询快速（< 500ms），详情完整

- [ ] **[TASK-3.5.2] Work Item Sync Status**: Work Item 同步状态组件 (`packages/app/src/app/components/work-item-sync-status.tsx`)
  - 同步进度条（显示同步进度）
  - 同步状态指示器（同步中/成功/失败）
  - 冲突提示（显示同步冲突）
  - 手动解决按钮（手动解决冲突）
  - 同步历史（显示同步历史记录）
  - **工作量**: 1天
  - **验收标准**: 状态实时，冲突提示清晰

- [ ] **[TASK-3.5.3] Code Commit Modal**: 代码提交确认对话框 (`packages/app/src/app/components/code-commit-modal.tsx`)
  - 提交预览（显示将要提交的文件列表）
  - 需求ID关联（输入或选择需求ID）
  - 提交消息编辑（编辑 commit message）
  - 分支选择（选择目标分支）
  - 确认提交按钮（确认提交到 TFS）
  - **工作量**: 1天
  - **验收标准**: 预览清晰，提交安全

- [ ] **[TASK-3.5.4] Pull Request Modal**: Pull Request 创建对话框 (`packages/app/src/app/components/pull-request-modal.tsx`)
  - PR 标题和描述（编辑 PR 标题和描述）
  - 审查者选择（选择代码审查者）
  - 源分支和目标分支（显示和选择分支）
  - 变更预览（显示 PR 包含的变更）
  - 创建 PR 按钮（创建 Pull Request）
  - **工作量**: 1.5天
  - **验收标准**: PR 创建成功，信息完整

- [ ] **[TASK-3.5.5] Build Status Monitor**: 构建状态监控组件 (`packages/app/src/app/components/build-status-monitor.tsx`)
  - 构建进度条（显示构建进度）
  - 构建状态（显示构建状态：排队/运行中/成功/失败）
  - 构建日志（显示构建日志，实时更新）
  - 失败通知（构建失败时弹出通知）
  - 重新构建按钮（触发重新构建）
  - **工作量**: 1天
  - **验收标准**: 状态实时，日志清晰

- [ ] **[TASK-3.5.6] TFS Auth UI**: TFS 认证界面 (`packages/app/src/app/pages/tfs-auth.tsx`)
  - PAT 输入（输入 Personal Access Token）
  - OAuth 登录按钮（触发 OAuth 流程）
  - 登录状态显示（显示当前登录状态）
  - 登出按钮（登出当前账号）
  - 组织选择（选择 TFS 组织）
  - **工作量**: 1天
  - **验收标准**: 登录流程顺畅，状态准确

- [ ] **[TASK-3.5.7] Org Switcher**: 组织切换器 (`packages/app/src/app/components/org-switcher.tsx`)
  - 组织列表（下拉列表显示所有组织）
  - 当前组织显示（显示当前选中的组织）
  - 切换按钮（切换到其他组织）
  - 组织配置（查看和编辑组织配置）
  - **工作量**: 0.5天
  - **验收标准**: 切换流畅，配置完整

- [ ] **[TASK-3.5.8] Checkin Guard Results**: 提交守卫检查结果 (`packages/app/src/app/components/checkin-guard-results.tsx`)
  - Lint 错误列表（显示 Lint 检查错误）
  - 测试失败列表（显示测试失败用例）
  - 修复建议（显示 AI 生成的修复建议）
  - 忽略按钮（忽略特定错误）
  - 修复按钮（一键修复错误）
  - **工作量**: 1天
  - **验收标准**: 错误展示清晰，修复方便

##### 3.5.2 Session Management UI (Session 管理 UI)

- [ ] **[TASK-3.5.9] Session Requirement Binding**: Session 与需求绑定组件 (`packages/app/src/app/components/session-requirement-binding.tsx`)
  - 需求ID输入框（输入需求ID）
  - 绑定确认按钮（确认绑定）
  - 当前绑定显示（显示当前绑定的需求ID）
  - 解绑按钮（解除绑定）
  - 绑定历史（显示绑定历史记录）
  - **工作量**: 0.5天
  - **验收标准**: 绑定操作简单，历史完整

- [ ] **[TASK-3.5.10] Session History UI**: Session 历史查询界面 (`packages/app/src/app/pages/session-history.tsx`)
  - 需求ID查询（输入需求ID查询相关 Session）
  - Session 列表（表格形式，显示 Session ID、开发者、时间、状态）
  - Session 时间线（时间线形式展示 Session 历史）
  - Session 详情（点击查看 Session 详情）
  - 过滤和排序（按时间、开发者、状态过滤）
  - **工作量**: 1.5天
  - **验收标准**: 查询快速（< 200ms），展示清晰

- [ ] **[TASK-3.5.11] Session Replay UI**: Session 重放界面 (`packages/app/src/app/pages/session-replay.tsx`)
  - 历史 Session 选择（选择要重放的 Session）
  - 上下文加载（加载 Session 的完整上下文）
  - OpenSpec 展示（显示历史 OpenSpec）
  - 代码变更展示（显示历史代码变更）
  - 对比功能（对比历史和当前状态）
  - 恢复按钮（恢复到历史状态）
  - **工作量**: 2.5天 🆕 **调整** (原 2天)
  - **验收标准**: 重放准确，上下文完整

- [ ] **[TASK-3.5.12] Session Sharing Modal**: Session 分享管理对话框 (`packages/app/src/app/components/session-sharing-modal.tsx`)
  - 分享链接生成（生成分享链接）
  - 权限控制（设置查看/编辑权限）
  - 过期时间设置（设置链接过期时间）
  - 分享统计（显示分享链接的访问统计）
  - 撤销分享按钮（撤销分享链接）
  - **工作量**: 1天
  - **验收标准**: 分享安全，权限可控

#### 3.6 Phase 3 Testing (Phase 3 测试) 🧪 🆕

- [ ] **[TASK-3.6.1] TFS Integration Unit Tests** (`backend/tests/test_tfs_*.py`)
  - TFS Client 单元测试
  - Work Item Sync 单元测试
  - Session Binding 单元测试
  - Requirement Query 单元测试
  - Code Commit 单元测试
  - **工作量**: 1天
  - **验收标准**: 覆盖率 > 80%，所有测试通过

- [ ] **[TASK-3.6.2] TFS Integration Tests** (`backend/tests/integration/test_tfs.py`)
  - 需求查询集成测试
  - 代码提交集成测试
  - PR 创建集成测试
  - 构建触发集成测试
  - Session-Requirement 绑定集成测试
  - **工作量**: 1天
  - **验收标准**: 主要流程测试通过，集成无误

- [ ] **[TASK-3.6.3] Session Management Tests** (`backend/tests/test_session_*.py`)
  - Session-Requirement 绑定测试
  - Session 历史查询测试
  - Session 重放测试
  - Session 分享测试
  - **工作量**: 0.5天
  - **验收标准**: 覆盖率 > 80%，所有测试通过

- [ ] **[TASK-3.6.4] Frontend TFS UI Tests** (`packages/app/src/app/__tests__/tfs.test.tsx`)
  - Requirement Query UI 测试
  - Code Commit Modal 测试
  - Pull Request Modal 测试
  - Build Status Monitor 测试
  - Session History UI 测试
  - **工作量**: 0.5天
  - **验收标准**: 组件测试通过，UI 交互正确

#### 3.7 Phase 3 Task Dependencies (任务依赖关系) 📊 🆕

```mermaid
graph TD
    %% TFS MCP Server
    A[TASK-3.1.1 TFS Client] --> B[TASK-3.1.2 Real TFS Integration]
    B --> C[TASK-3.1.3 Requirement Query by ID]
    B --> D[TASK-3.1.4 Work Item Sync]
    B --> E[TASK-3.1.5 Code Commit to TFS]
    E --> F[TASK-3.1.6 Pull Request Automation]
    F --> G[TASK-3.1.7 Build Integration]

    %% Authentication
    B --> H[TASK-3.2.1 TFS Auth Client]
    H --> I[TASK-3.2.2 Token Refresh]
    I --> J[TASK-3.2.3 Multi-Org Support]
    J --> K[TASK-3.2.4 SSO Integration]

    %% Check-in Guard
    B --> L[TASK-3.3.1 Basic Check-in Guard]
    L --> M[TASK-3.3.2 Real Linter Integration]
    L --> N[TASK-3.3.3 Real Test Runner]
    M --> O[TASK-3.3.4 Pre-commit Hooks]
    N --> O

    %% Session Sync
    P[TASK-3.4.1 Basic Session Sync] --> Q[TASK-3.4.2 Redis Storage]
    Q --> R[TASK-3.4.3 Session History]
    R --> S[TASK-3.4.4 Session Sharing]
    S --> T[TASK-3.4.5 Session-Requirement Binding]
    T --> U[TASK-3.4.6 Session History Query]
    U --> V[TASK-3.4.7 Session Replay for Bug Fix]
    V --> W[TASK-3.4.8 Session Binding API]

    %% TFS Frontend UI (并行)
    C --> UI1[TASK-3.5.1 Requirement Query UI]
    D --> UI2[TASK-3.5.2 Work Item Sync Status]
    E --> UI3[TASK-3.5.3 Code Commit Modal]
    F --> UI4[TASK-3.5.4 Pull Request Modal]
    G --> UI5[TASK-3.5.5 Build Status Monitor]
    H --> UI6[TASK-3.5.6 TFS Auth UI]
    J --> UI7[TASK-3.5.7 Org Switcher]
    O --> UI8[TASK-3.5.8 Checkin Guard Results]

    %% Session Frontend UI (并行)
    T --> UI9[TASK-3.5.9 Session Requirement Binding]
    U --> UI10[TASK-3.5.10 Session History UI]
    V --> UI11[TASK-3.5.11 Session Replay UI]
    S --> UI12[TASK-3.5.12 Session Sharing Modal]

    %% Testing
    UI1 --> TEST1[TASK-3.6.1 TFS Integration Unit Tests]
    UI2 --> TEST1
    UI3 --> TEST1
    UI4 --> TEST1
    UI5 --> TEST1
    UI6 --> TEST1
    UI7 --> TEST1
    UI8 --> TEST1
    UI9 --> TEST1
    UI10 --> TEST1
    UI11 --> TEST1
    UI12 --> TEST1
    TEST1 --> TEST2[TASK-3.6.2 TFS Integration Tests]
    TEST2 --> TEST3[TASK-3.6.3 Session Management Tests]
    TEST3 --> TEST4[TASK-3.6.4 Frontend TFS UI Tests]

    %% 关键路径标注
    style A fill:#ff6b6b
    style B fill:#ff6b6b
    style C fill:#ff6b6b
    style E fill:#ff6b6b
    style F fill:#ff6b6b
    style UI3 fill:#ff6b6b
    style UI4 fill:#ff6b6b
    style TEST1 fill:#ff6b6b
    style TEST4 fill:#ff6b6b

    %% 并行任务组标注
    style C fill:#90EE90
    style D fill:#90EE90
    style E fill:#90EE90

    style M fill:#87CEEB
    style N fill:#87CEEB

    style UI1 fill:#FFD700
    style UI2 fill:#FFD700
    style UI3 fill:#FFD700
    style UI4 fill:#FFD700
    style UI5 fill:#FFD700
    style UI6 fill:#FFD700
    style UI7 fill:#FFD700
    style UI8 fill:#FFD700

    style UI9 fill:#FFA500
    style UI10 fill:#FFA500
    style UI11 fill:#FFA500
    style UI12 fill:#FFA500
```

**并行任务组**:
- ✅ **组 A** (可并行): TASK-3.1.3, 3.1.4, 3.1.5 (Requirement Query + Work Item Sync + Code Commit)
- ✅ **组 B** (可并行): TASK-3.3.2, 3.3.3 (Linter + Test Runner)
- ✅ **组 C** (可并行): TASK-3.5.1~8 (TFS Frontend UI，8个任务)
- ✅ **组 D** (可并行): TASK-3.5.9~12 (Session Frontend UI，4个任务)

**关键路径** (Critical Path):
```
A → B → C → E → F → UI3 → UI4 → TEST1 → TEST2 → TEST3 → TEST4
总工期: 约 8 天（考虑并行开发）
```

**工期优化建议**:
- 并行开发组 A (TFS 功能): 节省 2 天
- 并行开发组 C (TFS UI): 节省 6 天
- 并行开发组 D (Session UI): 节省 3 天
- **总节省**: 约 11 天

### Phase 4: Stability & Resilience (稳定性与韧性) 🔥 P0 - 新增
**目标**: 确保系统稳定性、可恢复性和生产就绪
**周期**: Week 6 (5 工作日)
**优先级**: 🔥 P0 - MVP 必须

#### 4.1 Feature Flags System (功能开关系统)

- [ ] **[TASK-4.1.1] Feature Flag Infrastructure** (`backend/app/feature_flags/manager.py`)
  - 实现 Feature Flag 管理器
  - 支持环境变量和配置文件
  - 支持动态开关（无需重启）
  - 内存缓存 + Redis 持久化
  - **工作量**: 1天
  - **验收标准**: 可动态开关功能，延迟 < 10ms

- [ ] **[TASK-4.1.2] Feature Flag Integration** (`backend/app/feature_flags/flags.py`)
  - Skills RAG Feature Flag (`ENABLE_SKILLS_RAG`)
  - TFS Integration Feature Flag (`ENABLE_TFS_INTEGRATION`)
  - Multi-Agent Feature Flag (`ENABLE_MULTI_AGENT`)
  - Vector Search Feature Flag (`ENABLE_VECTOR_SEARCH`)
  - **工作量**: 0.5天
  - **验收标准**: 关键功能可开关，不影响其他功能

- [ ] **[TASK-4.1.3] Feature Flag UI** (`packages/app/src/app/pages/feature-flags.tsx`)
  - 前端 Feature Flag 控制面板
  - 实时状态显示
  - 权限控制（仅管理员可修改）
  - **工作量**: 1天
  - **验收标准**: 可通过 UI 控制功能开关

#### 4.2 Degradation Strategy (降级策略)

- [ ] **[TASK-4.2.1] LLM Fallback** (`backend/app/resilience/llm_fallback.py`)
  - 主模型不可用 → 备用模型
  - 所有模型不可用 → 缓存响应
  - 缓存未命中 → 友好错误提示
  - 降级状态监控和告警
  - **工作量**: 1天
  - **验收标准**: LLM 不可用时系统仍可用，用户体验降级但不中断

- [ ] **[TASK-4.2.2] Skills RAG Fallback** (`backend/app/resilience/rag_fallback.py`)
  - 向量搜索失败 → 关键词搜索
  - 关键词搜索失败 → 使用默认 Skills
  - 默认 Skills 列表配置
  - **工作量**: 0.5天
  - **验收标准**: 检索失败时有降级方案，准确率 > 60%

- [ ] **[TASK-4.2.3] TFS Integration Fallback** (`backend/app/resilience/tfs_fallback.py`)
  - TFS 连接失败 → 本地模式
  - 本地模式下功能限制提示
  - 连接恢复后自动同步
  - 离线队列管理
  - **工作量**: 1天
  - **验收标准**: TFS 不可用时可本地工作，恢复后自动同步

#### 4.3 Rollback & Recovery (回滚与恢复)

- [ ] **[TASK-4.3.1] Data Migration Scripts** (`backend/scripts/migrations/`)
  - OpenSpec v0.1 → v0.2 迁移脚本
  - 回滚脚本 (v0.2 → v0.1)
  - 迁移测试用例
  - 迁移日志和验证
  - **工作量**: 1天
  - **验收标准**: 可安全迁移和回滚，数据完整性 100%

- [ ] **[TASK-4.3.2] Database Backup & Restore** (`backend/app/backup/manager.py`)
  - 自动备份策略（每日/每周）
  - 一键恢复功能
  - 备份验证和完整性检查
  - 备份存储管理（本地 + 云端）
  - **工作量**: 0.5天
  - **验收标准**: 可快速恢复数据，RTO < 5分钟

- [ ] **[TASK-4.3.3] Health Check & Monitoring** (`backend/app/monitoring/health.py`)
  - 健康检查端点增强 (`/health/detailed`)
  - 关键指标监控 (延迟、错误率、资源使用)
  - 告警机制（邮件/Slack/钉钉）
  - 监控仪表板
  - **工作量**: 1天
  - **验收标准**: 可实时监控系统健康状态，告警及时

- [ ] **[TASK-4.3.4] Circuit Breaker** (`backend/app/resilience/circuit_breaker.py`)
  - 实现断路器模式
  - 外部服务调用保护 (LLM, TFS, Redis)
  - 自动恢复机制（半开状态）
  - 断路器状态监控
  - **工作量**: 1天
  - **验收标准**: 外部服务故障时系统不崩溃，自动恢复

#### 4.4 Phase 4 Testing (Phase 4 测试) 🧪

- [ ] **[TASK-4.4.1] Resilience Tests** (`backend/tests/test_resilience_*.py`)
  - Feature Flags 测试
  - 降级策略测试
  - 断路器测试
  - **工作量**: 1天
  - **验收标准**: 覆盖率 > 80%，所有测试通过

- [ ] **[TASK-4.4.2] E2E Tests** (`backend/tests/e2e/test_mvp.py`)
  - 用户输入需求 → 生成 OpenSpec → 生成代码
  - TFS 集成流程测试
  - 错误恢复测试
  - **工作量**: 1天
  - **验收标准**: 主要用户流程测试通过

- [ ] **[TASK-4.4.3] Stress Tests** (`backend/tests/stress/test_load.py`)
  - 100 并发用户测试
  - 长时间运行测试 (4小时)
  - 内存泄漏测试
  - **工作量**: 0.5天
  - **验收标准**: 系统稳定，无内存泄漏，P95 延��� < 2s

- [ ] **[TASK-4.4.4] Post-Development Test Workflow**: 开发后测试工作流 (`backend/app/workflow/test_workflow.py`) 🆕
  - 所有开发任务完成后，自动触发 E2E 测试
  - 测试失败时，生成问题报告并分配给相关 Agent
  - 测试通过后，标记 OpenSpec 为 "ready for deployment"
  - 集成到 OpenSpec 任务状态机
  - **工作量**: 1天
  - **验收标准**: 测试流程自动化，失败有明确反馈，成功率 > 90%

- [ ] **[TASK-4.4.5] Test Report Generator**: 测试报告生成器 (`backend/app/testing/report_generator.py`) 🆕
  - 生成详细的测试报告（HTML/PDF）
  - 包含测试覆盖率、失败用例、性能指标
  - 关联需求ID和 Session ID
  - 发送报告给相关人员（邮件/钉钉）
  - **工作量**: 0.5天
  - **验收标准**: 报告格式清晰，信息完整

#### 4.5 Stability Frontend UI (稳定性前端 UI) 🆕 ⚠️ **缺失**

- [ ] **[TASK-4.5.1] Feature Flags Control Panel**: Feature Flags 控制面板 (`packages/app/src/app/pages/feature-flags.tsx`)
  - 功能开关列表（表格形式，显示功能名称、状态、描述）
  - 实时切换（开关按钮，实时生效）
  - 权限控制（仅管理员可修改）
  - 开关历史（显示开关变更历史）
  - 批量操作（批量启用/禁用功能）
  - **工作量**: 1.5天
  - **验收标准**: 切换实时生效，权限控制严格

- [ ] **[TASK-4.5.2] Feature Flag Indicator**: Feature Flag 状态指示器 (`packages/app/src/app/components/feature-flag-indicator.tsx`)
  - 功能可用性指示（显示功能是否可用）
  - 降级提示（功能降级时显示提示）
  - 状态徽章（显示功能状态徽章）
  - **工作量**: 0.5天
  - **验收标准**: 指示准确，提示及时

- [ ] **[TASK-4.5.3] Health Monitor Dashboard**: 系统健康检查面板 (`packages/app/src/app/pages/health-monitor.tsx`)
  - 服务状态卡片（显示各服务状态：正常/异常/降级）
  - 延迟监控（显示 API 响应延迟）
  - 错误率监控（显示错误率趋势）
  - 资源使用（显示 CPU、内存、磁盘使用）
  - 健康评分（综合健康评分）
  - **工作量**: 2.5天 🆕 **调整** (原 2天)
  - **验收标准**: 监控实时，数据准确

- [ ] **[TASK-4.5.4] Alert Notifications**: 告警和通知组件 (`packages/app/src/app/components/alert-notifications.tsx`)
  - 告警列表（显示所有告警）
  - 严重级别（Critical/High/Medium/Low）
  - 告警详情（点击查看详情）
  - 历史记录（查看历史告警）
  - 确认/忽略按钮（确认或忽略告警）
  - **工作量**: 1天
  - **验收标准**: 告警及时，分级清晰

- [ ] **[TASK-4.5.5] Backup & Restore UI**: 数据备份和恢复界面 (`packages/app/src/app/pages/backup-restore.tsx`)
  - 备份列表（显示所有备份，包含时间、大小、状态）
  - 创建备份按钮（手动创建备份）
  - 恢复按钮（选择备份进行恢复）
  - 进度显示（显示备份/恢复进度）
  - 备份验证（验证备份完整性）
  - **工作量**: 1.5天
  - **验收标准**: 备份可靠，恢复安全

- [ ] **[TASK-4.5.6] Monitoring Dashboard**: 系统监控仪表板 (`packages/app/src/app/pages/monitoring-dashboard.tsx`)
  - 性能图表（CPU、内存、网络、磁盘使用趋势）
  - 实时指标（显示实时性能指标）
  - 历史趋势（显示历史性能趋势）
  - 告警集成（显示相关告警）
  - 导出报告（导出监控报告）
  - **工作量**: 2天
  - **验收标准**: 图表清晰，数据实时

- [ ] **[TASK-4.5.7] Test Report Generator UI**: 测试报告生成器界面 (`packages/app/src/app/pages/test-report-generator.tsx`)
  - 报告配置（选择报告类型、格式、包含内容）
  - 报告预览（预览生成的报告）
  - 导出按钮（导出为 HTML/PDF）
  - 发送按钮（发送报告给相关人员）
  - 报告历史（查看历史报告）
  - **工作量**: 1天
  - **验收标准**: 报告完整，导出成功

- [ ] **[TASK-4.5.8] E2E Test Runner UI**: E2E 测试执行界面 (`packages/app/src/app/pages/e2e-test-runner.tsx`)
  - 测试选择（选择要执行的 E2E 测试）
  - 执行进度（显示测试执行进度）
  - 结果展示（显示测试结果，通过/失败）
  - 失败详情（查看失败测试的详情）
  - 重新执行（重新执行失败的测试）
  - **工作量**: 1.5天
  - **验收标准**: 执行可靠，结果清晰

- [ ] **[TASK-4.5.9] Stress Test Config UI**: 压力测试配置界面 (`packages/app/src/app/pages/stress-test-config.tsx`)
  - 并发数设置（设置并发用户数）
  - 持续时间设置（设置测试持续时间）
  - 测试场景选择（选择测试场景）
  - 执行按钮（启动压力测试）
  - 结果分析（显示压力测试结果和分析）
  - **工作量**: 1天
  - **验收标准**: 配置灵活，结果详细

- [ ] **[TASK-4.5.10] Test Automation Workflow UI**: 测试自动化工作流界面 (`packages/app/src/app/pages/test-automation-workflow.tsx`)
  - 工作流配置（配置测试自动化工作流）
  - 执行状态（显示工作流执行状态）
  - 失败处理（显示失败处理策略）
  - 通知配置（配置测试结果通知）
  - 工作流历史（查看工作流执行历史）
  - **工作量**: 1.5天
  - **验收标准**: 工作流可靠，通知及时

#### 4.6 Phase 4 API Endpoints (Phase 4 API 端点) 🆕

**Feature Flags API**:
```
GET  /feature-flags                      - 列出所有 Feature Flags
GET  /feature-flags/{name}               - 获取特定 Feature Flag
PUT  /feature-flags/{name}               - 更新 Feature Flag
GET  /feature-flags/history              - 获取变更历史
POST /feature-flags/batch                - 批量更新 Feature Flags
```

**健康检查 API**:
```
GET  /health                             - 基础健康检查
GET  /health/detailed                    - 详细健康检查
GET  /health/services                    - 服务状态
GET  /health/metrics                     - 性能指标
GET  /health/dependencies                - 依赖服务状态
```

**备份恢复 API**:
```
POST /backup/create                      - 创建备份
GET  /backup/list                        - 列出所有备份
POST /backup/restore                     - 恢复备份
POST /backup/verify                      - 验证备份完整性
DELETE /backup/{id}                      - 删除备份
GET  /backup/{id}/status                 - 查询备份状态
```

**监控告警 API**:
```
GET  /monitoring/metrics                 - 获取监控指标
GET  /monitoring/alerts                  - 获取告警列表
POST /monitoring/alerts/{id}/acknowledge - 确认告警
POST /monitoring/alerts/{id}/resolve     - 解决告警
GET  /monitoring/alerts/history          - 获取告警历史
```

**测试 API**:
```
POST /test/e2e/run                       - 运行 E2E 测试
GET  /test/e2e/status                    - 查询测试状态
GET  /test/e2e/report                    - 获取测试报告
POST /test/stress/run                    - 运行压力测试
GET  /test/stress/results                - 获取压力测试结果
```

#### 4.7 Phase 4 Task Dependencies (任务依赖关系) 📊 🆕

```mermaid
graph TD
    %% Feature Flags
    A[TASK-4.1.1 Feature Flag Infrastructure] --> B[TASK-4.1.2 Feature Flag Integration]
    B --> C[TASK-4.1.3 Feature Flag UI]

    %% Degradation Strategy
    D[TASK-4.2.1 LLM Fallback] --> E[TASK-4.2.2 Skills RAG Fallback]
    E --> F[TASK-4.2.3 TFS Integration Fallback]

    %% Rollback & Recovery
    G[TASK-4.3.1 Data Migration Scripts] --> H[TASK-4.3.2 Database Backup & Restore]
    H --> I[TASK-4.3.3 Health Check & Monitoring]
    I --> J[TASK-4.3.4 Circuit Breaker]

    %% Testing
    C --> K[TASK-4.4.1 Resilience Tests]
    F --> K
    J --> K
    K --> L[TASK-4.4.2 E2E Tests]
    L --> M[TASK-4.4.3 Stress Tests]
    M --> N[TASK-4.4.4 Post-Development Test Workflow]
    N --> O[TASK-4.4.5 Test Report Generator]

    %% Frontend UI (并行)
    B --> UI1[TASK-4.5.1 Feature Flags Control Panel]
    B --> UI2[TASK-4.5.2 Feature Flag Indicator]
    I --> UI3[TASK-4.5.3 Health Monitor Dashboard]
    I --> UI4[TASK-4.5.4 Alert Notifications]
    H --> UI5[TASK-4.5.5 Backup & Restore UI]
    I --> UI6[TASK-4.5.6 Monitoring Dashboard]
    O --> UI7[TASK-4.5.7 Test Report Generator UI]
    L --> UI8[TASK-4.5.8 E2E Test Runner UI]
    M --> UI9[TASK-4.5.9 Stress Test Config UI]
    N --> UI10[TASK-4.5.10 Test Automation Workflow UI]

    %% 关键路径标注
    style A fill:#ff6b6b
    style B fill:#ff6b6b
    style K fill:#ff6b6b
    style L fill:#ff6b6b
    style M fill:#ff6b6b
    style O fill:#ff6b6b

    %% 并行任务组标注
    style D fill:#90EE90
    style E fill:#90EE90
    style F fill:#90EE90

    style G fill:#87CEEB
    style H fill:#87CEEB
    style I fill:#87CEEB
    style J fill:#87CEEB

    style UI1 fill:#FFD700
    style UI2 fill:#FFD700
    style UI3 fill:#FFD700
    style UI4 fill:#FFD700
    style UI5 fill:#FFD700
    style UI6 fill:#FFD700
    style UI7 fill:#FFD700
    style UI8 fill:#FFD700
    style UI9 fill:#FFD700
    style UI10 fill:#FFD700
```

**并行任务组**:
- ✅ **组 A** (可并行): TASK-4.2.1, 4.2.2, 4.2.3 (LLM/RAG/TFS Fallback)
- ✅ **组 B** (可并行): TASK-4.3.1, 4.3.2, 4.3.3, 4.3.4 (Migration/Backup/Health/Circuit)
- ✅ **组 C** (可并行): TASK-4.5.1~10 (Stability Frontend UI，10个任务)

**关键路径** (Critical Path):
```
A → B → K → L → M → N → O
总工期: 约 6 天（考虑并行开发）
```

**工期优化建议**:
- 并行开发组 A (Degradation): 节省 2 天
- 并行开发组 B (Rollback & Recovery): 节省 3 天
- 并行开发组 C (Frontend UI): 节省 8 天
- **总节省**: 约 13 天

### Phase 5: Multi-Agent Enhancement (多智能体增强) 📋 P1
**目标**: 引入 Eigent AI 多智能体编排理念，实现专业化智能体协作
**周期**: MVP 后 4-8周
**优先级**: 📋 P1 - 增强功能

#### 4.1 Agent Framework (智能体框架)
- [ ] **[TASK-4.1.1] Agent Base Class**: 实现智能体基类 (`backend/app/agents/base_agent.py`)
  - 定义 Agent 接口：`execute()`, `plan()`, `validate()`
  - 实现消息通信协议：`send_message()`, `receive_message()`
  - 添加状态管理：`get_state()`, `set_state()`
  - **验收标准**: 单元测试覆盖率 > 80%，可实例化并执行简单任务

- [ ] **[TASK-4.1.2] Agent Registry**: 实现智能体注册中心 (`backend/app/agents/registry.py`)
  - 智能体注册和发现机制
  - 能力标签和匹配算法
  - 智能体生命周期管理（启动、停止、重启）
  - **验收标准**: 支持动态注册/注销，能根据能力标签查找智能体

- [ ] **[TASK-4.1.3] Message Bus**: 实现消息总线 (`backend/app/agents/message_bus.py`)
  - 发布/订阅模式实现
  - 消息队列和优先级管理
  - 消息持久化（Redis）
  - **验收标准**: 支持 1000+ 消息/秒吞吐量，消息不丢失

#### 4.2 Specialized Agents (专业化智能体)
- [ ] **[TASK-4.2.1] PM Agent**: 产品经理智能体 (`backend/app/agents/pm_agent.py`)
  - 需求分析和用户故事生成
  - 验收标准定义
  - 优先级评估
  - **验收标准**: 能从自然语言生成结构化需求，包含至少 3 条验收标准

- [ ] **[TASK-4.2.2] Architect Agent**: 架构师智能体 (`backend/app/agents/architect_agent.py`)
  - 系统架构设计
  - 技术选型建议
  - API 设计和数据模型设计
  - **验收标准**: 能生成完整的架构设计文档，包含 API 端点和数据模型

- [ ] **[TASK-4.2.3] Developer Agent**: 开发智能体 (`backend/app/agents/developer_agent.py`)
  - 代码生成（基于模板和 RAG）
  - Bug 修复
  - 代码重构
  - **验收标准**: 生成的代码符合公司规范，通过 Linter 检查

- [ ] **[TASK-4.2.4] Tester Agent**: 测试智能体 (`backend/app/agents/tester_agent.py`)
  - 单元测试生成
  - 集成测试生成
  - 测试执行和报告
  - **验收标准**: 生成的测试覆盖率 > 70%，测试可执行

- [ ] **[TASK-4.2.5] Reviewer Agent**: 代码审查智能体 (`backend/app/agents/reviewer_agent.py`)
  - 代码规范检查
  - 安全漏洞扫描
  - 性能分析
  - **验收标准**: 能识别常见代码问题（OWASP Top 10），生成审查报告

- [ ] **[TASK-4.2.6] DevOps Agent**: 运维智能体 (`backend/app/agents/devops_agent.py`)
  - CI/CD 配置生成
  - Docker/K8s 配置生成
  - 部署脚本生成
  - **验收标准**: 生成的配置文件可直接使用，通过验证

#### 4.3 Workflow Engine (工作流引擎)
- [ ] **[TASK-4.3.1] DAG Engine**: 实现 DAG 工作流引擎 (`backend/app/workflow/dag_engine.py`)
  - 工作流图解析（节点、边、条件）
  - 拓扑排序和执行计划生成
  - 并行执行调度
  - **验收标准**: 支持复杂工作流（10+ 节点），正确处理依赖关系

- [ ] **[TASK-4.3.2] Task Allocator**: 实现任务分配器 (`backend/app/workflow/task_allocator.py`)
  - 基于能力的任务匹配
  - 负载均衡算法
  - 优先级调度
  - **验收标准**: 任务分配延迟 < 100ms，负载均衡误差 < 10%

- [ ] **[TASK-4.3.3] Execution Context**: 实现执行上下文管理 (`backend/app/workflow/context.py`)
  - 共享状态管理
  - 上下文传递和隔离
  - 历史记录追踪
  - **验收标准**: 支持跨智能体上下文共享，状态一致性保证

- [ ] **[TASK-4.3.4] Workflow Templates**: 预定义工作流模板 (`backend/app/workflow/templates/`)
  - 全流程开发模板（需求 -> 设计 -> 开发 -> 测试 -> 审查 -> 部署）
  - Bug 修复模板
  - 代码重构模板
  - **验收标准**: 至少 3 个可用模板，可通过 UI 选择和自定义

### Phase 5: Enhanced Collaboration (增强协作) 🔮 P2
**目标**: 实现多人实时协作和会话共享
**周期**: 根据 MVP 反馈决定
**优先级**: 🔮 P2 - 未来迭代

#### 5.1 Real-time Collaboration (实时协作)
- [ ] **[TASK-5.1.1] WebSocket Server**: 实现 WebSocket 服务器 (`backend/app/collaboration/websocket.py`)
  - 连接管理和心跳检测
  - 房间（Room）概念和管理
  - 消息广播和单播
  - **验收标准**: 支持 100+ 并发连接，消息延迟 < 50ms

- [ ] **[TASK-5.1.2] Presence System**: 实现在线状态系统 (`backend/app/collaboration/presence.py`)
  - 用户在线/离线状态
  - 当前活动会话追踪
  - 光标位置同步（可选）
  - **验收标准**: 状态更新实时同步，准确率 > 99%

- [ ] **[TASK-5.1.3] Operational Transform**: 实现操作转换 (`backend/app/collaboration/ot.py`)
  - 文本编辑冲突解决
  - 操作序列化和反序列化
  - 历史回放支持
  - **验收标准**: 多人同时编辑无冲突，最终一致性保证

- [ ] **[TASK-5.1.4] Collaboration UI**: 前端协作界面 (`packages/app/src/app/pages/collaboration.tsx`)
  - 在线用户列表
  - 实时活动流
  - 会话共享和邀请
  - **验收标准**: UI 响应流畅，状态更新实时显示

#### 5.2 Permission & RBAC (权限管理)
- [ ] **[TASK-5.2.1] User Management**: 实现用户管理 (`backend/app/auth/user.py`)
  - 用户注册和登录
  - 用户信息管理
  - 密码加密和验证
  - **验收标准**: 支持基本的用户 CRUD 操作，密码安全存储

- [ ] **[TASK-5.2.2] Role System**: 实现角色系统 (`backend/app/auth/role.py`)
  - 角色定义（Admin, Developer, Viewer）
  - 角色权限配置
  - 角色分配和撤销
  - **验收标准**: 支持至少 3 种角色，权限可配置

- [ ] **[TASK-5.2.3] Permission Checker**: 实现权限检查器 (`backend/app/auth/permission.py`)
  - 资源级别权限控制
  - 操作级别权限控制
  - 权限缓存优化
  - **验收标准**: 权限检查延迟 < 10ms，准确率 100%

- [ ] **[TASK-5.2.4] Audit Logger**: 实现审计日志 (`backend/app/auth/audit.py`)
  - 操作日志记录
  - 日志查询和过滤
  - 日志导出（CSV/JSON）
  - **验收标准**: 所有敏感操作被记录，日志可追溯

### Phase 6: Enhanced Superpower (增强资产层) 🔮 P2
**目标**: 优化 RAG 性能和准确性，支持更多资产类型
**周期**: 根据 MVP 反馈决定
**优先级**: 🔮 P2 - 未来迭代

#### 6.1 Vector Store Enhancement (向量存储增强)
- [ ] **[TASK-6.1.1] Qdrant Integration**: 集成 Qdrant 向量数据库 (`backend/app/superpower/qdrant_store.py`)
  - 替换 ChromaDB 为 Qdrant（性能更好）
  - 集合（Collection）管理
  - 向量索引和搜索
  - **验收标准**: 搜索延迟 < 100ms，召回率 > 90%

- [ ] **[TASK-6.1.2] Hybrid Search**: 实现混合搜索 (`backend/app/superpower/hybrid_search.py`)
  - 向量搜索 + 关键词搜索
  - 结果融合和重排序
  - 相关性评分优化
  - **验收标准**: 搜索准确率提升 > 20%

- [ ] **[TASK-6.1.3] Incremental Indexing**: 实现增量索引 (`backend/app/superpower/indexer.py`)
  - 文件变更监听
  - 增量更新向量
  - 索引版本管理
  - **验收标准**: 索引更新延迟 < 5s，不影响查询性能

#### 6.2 Asset Management (资产管理)
- [ ] **[TASK-6.2.1] Code Snippet Library**: 代码片段库 (`backend/app/superpower/snippets.py`)
  - 代码片段存储和分类
  - 标签和元数据管理
  - 使用频率统计
  - **验收标准**: 支持 1000+ 代码片段，检索准确

- [ ] **[TASK-6.2.2] Document Indexer**: 文档索引器 (`backend/app/superpower/doc_indexer.py`)
  - Markdown/PDF/Word 文档解析
  - 章节和段落分割
  - 图表提取（可选）
  - **验收标准**: 支持多种文档格式，解析准确率 > 95%

- [ ] **[TASK-6.2.3] Best Practice Recommender**: 最佳实践推荐 (`backend/app/superpower/recommender.py`)
  - 基于上下文的推荐算法
  - 历史使用数据分析
  - 推荐结果排序
  - **验收标准**: 推荐准确率 > 70%，用户满意度 > 80%

### Phase 7: Full-Cycle Automation (全流程自动化) 📋 P1
**目标**: 实现从需求到发布的全流程自动化
**周期**: MVP 后根据需求
**优先级**: 📋 P1 - 增强功能 (部分功能)

#### 7.1 Testing Automation (测试自动化)
- [ ] **[TASK-7.1.1] Test Generator**: 测试生成器 (`backend/app/testing/generator.py`)
  - 基于代码生成单元测试
  - 基于 API 定义生成集成测试
  - 测试数据生成
  - **验收标准**: 生成的测试可执行，覆盖率 > 70%

- [ ] **[TASK-7.1.2] Test Runner**: 测试执行器 (`backend/app/testing/runner.py`)
  - 支持 pytest/jest/mocha 等测试框架
  - 并行测试执行
  - 测试报告生成
  - **验收标准**: 测试执行时间优化 > 30%，报告清晰

- [ ] **[TASK-7.1.3] Coverage Analyzer**: 覆盖率分析器 (`backend/app/testing/coverage.py`)
  - 代码覆盖率统计
  - 未覆盖代码高亮
  - 覆盖率趋势分析
  - **验收标准**: 准确统计覆盖率，可视化展示

#### 7.2 CI/CD Integration (CI/CD 集成)
- [ ] **[TASK-7.2.1] Pipeline Generator**: 流水线生成器 (`backend/app/cicd/pipeline_generator.py`)
  - 生成 GitHub Actions/GitLab CI/Jenkins 配置
  - 多阶段流水线配置
  - 环境变量和密钥管理
  - **验收标准**: 生成的配置可直接使用，通过验证

- [ ] **[TASK-7.2.2] Build Trigger**: 构建触发器 (`backend/app/cicd/build_trigger.py`)
  - 自动触发 TFS/Azure DevOps 构建
  - 构建状态监控
  - 构建失败通知
  - **验收标准**: 触发成功率 > 99%，状态实时更新

- [ ] **[TASK-7.2.3] Deployment Manager**: 部署管理器 (`backend/app/cicd/deployment.py`)
  - 多环境部署配置（Dev/Test/Prod）
  - 回滚机制
  - 部署审批流程
  - **验收标准**: 支持一键部署，回滚时间 < 5min

### Phase 8: Model & Performance (模型与性能) 🔮 P2
**目标**: 支持多模型配置和性能优化
**周期**: 根据 MVP 反馈决定
**优先级**: 🔮 P2 - 未来迭代

#### 8.1 Multi-Model Support (多模型支持)
- [ ] **[TASK-8.1.1] Model Router**: 模型路由器 (`backend/app/models/router.py`)
  - 多模型配置管理
  - 基于任务类型的模型选择
  - 模型负载均衡
  - **验收标准**: 支持 5+ 模型提供商，路由延迟 < 50ms

- [ ] **[TASK-8.1.2] Model Adapter**: 模型适配器 (`backend/app/models/adapters/`)
  - OpenAI 适配器
  - Anthropic 适配器
  - Azure OpenAI 适配器
  - 私有模型适配器
  - **验收标准**: 统一接口，支持流式和非流式调用

- [ ] **[TASK-8.1.3] Cost Tracker**: 成本追踪器 (`backend/app/models/cost_tracker.py`)
  - Token 使用统计
  - 成本计算和预警
  - 使用报告生成
  - **验收标准**: 准确统计成本，支持预算控制

#### 8.2 Performance Optimization (性能优化)
- [ ] **[TASK-8.2.1] Response Cache**: 响应缓存 (`backend/app/cache/response_cache.py`)
  - LLM 响应缓存（Redis）
  - 缓存键生成策略
  - 缓存失效策略
  - **验收标准**: 缓存命中率 > 30%，响应时间减少 > 50%

- [ ] **[TASK-8.2.2] Request Batching**: 请求批处理 (`backend/app/optimization/batching.py`)
  - 多个请求合并为批次
  - 批次大小动态调整
  - 批次结果分发
  - **验收标准**: 吞吐量提升 > 40%

- [ ] **[TASK-8.2.3] Async Processing**: 异步处理优化 (`backend/app/optimization/async_processing.py`)
  - 长时间任务异步化
  - 任务队列管理（Celery/RQ）
  - 进度追踪和通知
  - **验收标准**: 用户体验流畅，无阻塞

### Phase 9: UI/UX Enhancement (界面增强) 🔮 P2
**目标**: 优化用户界面和交互体验
**周期**: 根据 MVP 反馈决定
**优先级**: 🔮 P2 - 未来迭代

#### 9.1 Agent Monitor (智能体监控)
- [ ] **[TASK-9.1.1] Agent Dashboard**: 智能体仪表板 (`packages/app/src/app/pages/agent-monitor.tsx`)
  - 智能体状态实时显示
  - 任务执行进度可视化
  - 性能指标图表
  - **验收标准**: 实时更新，响应流畅

- [ ] **[TASK-9.1.2] Task Flow Visualization**: 任务流可视化 (`packages/app/src/app/components/task-flow.tsx`)
  - DAG 图可视化
  - 节点状态动画
  - 交互式节点详情
  - **验收标准**: 支持 20+ 节点，交互流畅

#### 9.2 Workflow Designer (工作流设计器)
- [ ] **[TASK-9.2.1] Visual Editor**: 可视化编辑器 (`packages/app/src/app/pages/workflow-designer.tsx`)
  - 拖拽式节点编辑
  - 连线和条件配置
  - 模板保存和加载
  - **验收标准**: 支持复杂工作流编辑，操作直观

- [ ] **[TASK-9.2.2] Workflow Validator**: 工作流验证器 (`packages/app/src/app/lib/workflow-validator.ts`)
  - 循环依赖检测
  - 节点配置验证
  - 错误提示和修复建议
  - **验收标准**: 准确检测错误，提示清晰

### Phase 10: Enterprise Features (企业特性) 🔮 P2
**目标**: 完善企业级功能
**周期**: 根据 MVP 反馈决定
**优先级**: 🔮 P2 - 未来迭代

#### 10.1 Company Framework Integration (公司框架集成)
- [ ] **[TASK-10.1.1] Framework Templates**: 框架模板库 (`backend/app/enterprise/frameworks/`)
  - 前端框架模板（Vue3/React）
  - 后端框架模板（FastAPI/Spring Boot）
  - 数据库模板（MySQL/PostgreSQL）
  - **验收标准**: 至少 5 个框架模板，可直接使用

- [ ] **[TASK-10.1.2] Code Standards**: 代码规范配置 (`backend/app/enterprise/standards/`)
  - ESLint/Pylint 规则配置
  - Prettier/Black 格式化配置
  - Git Hooks 配置
  - **验收标准**: 规范配置完整，自动检查生效

- [ ] **[TASK-10.1.3] Skills Library**: 技能库管理 (`backend/app/enterprise/skills/`)
  - 公司内部 Skills 管理
  - Skills 版本控制
  - Skills 使用统计
  - **验收标准**: 支持 20+ Skills，可动态加载

#### 10.2 Security & Compliance (安全与合规)
- [ ] **[TASK-10.2.1] Security Scanner**: 安全扫描器 (`backend/app/security/scanner.py`)
  - 依赖漏洞扫描
  - 敏感信息检测
  - OWASP Top 10 检查
  - **验收标准**: 准确检测常见漏洞，误报率 < 5%

- [ ] **[TASK-10.2.2] Compliance Checker**: 合规检查器 (`backend/app/security/compliance.py`)
  - 许可证合规检查
  - 代码版权检查
  - 合规报告生成
  - **验收标准**: 准确识别许可证冲突

- [ ] **[TASK-10.2.3] Data Encryption**: 数据加密 (`backend/app/security/encryption.py`)
  - 敏感数据加密存储
  - 传输加密（TLS）
  - 密钥管理
  - **验收标准**: 符合安全标准，性能影响 < 10%

## 6. Technology Stack / 技术栈详解

### 6.1 Frontend (前端)
```
Tauri v2.x              # 跨平台桌面应用框架
├── SolidJS             # 响应式 UI 框架
├── TailwindCSS v4      # 原子化 CSS
├── Lucide Icons        # 图标库
├── @tanstack/solid-query  # 数据获取和缓存
└── solid-router        # 路由管理
```

### 6.2 Backend (后端)
```
Python 3.10+            # 编程语言
├── FastAPI             # Web 框架
├── Uvicorn             # ASGI 服务器
├── Pydantic            # 数据验证
├── SQLAlchemy          # ORM (可选)
└── UV                  # 包管理器
```

### 6.3 AI & ML (AI 和机器学习)
```
LangChain               # LLM 应用框架
├── OpenAI SDK          # OpenAI API 客户端
├── Anthropic SDK       # Claude API 客户端
├── Azure OpenAI SDK    # Azure OpenAI 客户端
└── Ollama              # 本地模型运行时 (可选)
```

### 6.4 Vector Store & RAG (向量存储和 RAG)
```
Qdrant                  # 向量数据库
├── ChromaDB            # 备选向量数据库
├── OpenAI Embeddings   # 文本嵌入
└── Sentence Transformers  # 本地嵌入模型 (可选)
```

### 6.5 Message Queue & Cache (消息队列和缓存)
```
Redis                   # 缓存和消息队列
├── Celery / RQ         # 任务队列 (可选)
└── PostgreSQL          # 关系数据库 (可选)
```

### 6.6 DevOps & Monitoring (运维和监控)
```
Docker                  # 容器化
├── Docker Compose      # 本地开发环境
├── Prometheus          # 监控指标
├── Grafana             # 可视化仪表板
└── Sentry              # 错误追踪 (可选)
```

## 7. Development Roadmap / 开发路线图 (v0.3.0 Optimized)

### 7.0 MVP Overview / MVP 概览

**目标**: 6 周交付可用的 MVP，验证核心价值

**包含 Phase**:
- 🔥 **Phase 1**: Foundation & Contract (Week 1)
- 🔥 **Phase 2**: Skills-based RAG (Week 2-4)
- 🔥 **Phase 3**: TFS Integration (Week 5)
- 🔥 **Phase 4**: Stability & Testing (Week 6) - 新增

**关键指标**:
- ✅ 任务原子化：0.5-2天/任务
- ✅ 依赖关系明确：Mermaid 图 + 并行任务标注
- ✅ 测试覆盖：5层测试金字塔
- ✅ 稳定性保障：Feature Flags + 降级 + 回滚

### 7.1 Phase Completion Status (Phase 完成状态)

#### 🔥 Phase 1: Foundation & Contract (骨架与契约) - P0
- **完成度**: 100% (28/28 任务) ✅ **已完成**
- **状态**: ✅ 所有核心功能和前端 UI 已完成
- **周期**: Week 1 (5 工作日)
- **已完成**: 基础架构 + OpenSpec 契约层 + 版本管理 + 生命周期管理 + 前端 UI ✅
- **剩余**: TASK-1.4.7 Spec Archive to TFS（P1 可选，MVP 后实现）

#### 🔥 Phase 2: Assets & Coding (资产与编码) - P0
- **完成度**: 2% (1/63 任务，扩展后) 🆕
- **状态**: ⚠️ 基础完成，需大幅增强
- **周期**: Week 2-5 (20 工作日) 🆕 扩展
- **核心**: Skills-based RAG (28个任务) + Superpower 归档 (4个任务) + **代码生成与本地开发 (15个新增任务)** 🆕

#### 🔥 Phase 3: Enterprise Integration (企业集成) - P0
- **完成度**: 20% (4/24 任务) 🆕
- **状态**: ⚠️ 基础完成，需增强
- **周期**: Week 5 (5 工作日)
- **重点**: TFS 真实集成 + Work Item 同步 + Session-Requirement 绑定 (新增7个任务)

#### 🔥 Phase 4: Stability & Resilience (稳定性与韧性) - P0 - 新增
- **完成度**: 0% (0/15 任务) 🆕
- **状态**: 🆕 新增 Phase
- **周期**: Week 6 (5 工作日)
- **包含**: Feature Flags + 降级策略 + 回滚计划 + E2E 测试 (新增2个测试任务)

### 7.2 MVP Development Sequence (MVP 开发顺序)

#### Week 1: Phase 1 - Foundation
**目标**: 建立坚实的基础架构

**关键任务**:
1. Backend Infrastructure (2天)
   - Project Structure + FastAPI Server
   - Config (细化为 5 个子任务)
   - Logging + Error Handling

2. OpenSpec Schema (2天)
   - Enhanced Schema v0.2
   - Schema Validation + Migration

3. Frontend Integration (1天)
   - Spec Editor + Visualizer

4. Testing (1天)
   - Unit Tests + Integration Tests

**并行任务组**:
- 组 A: Config 子任务 (3个可并行)
- 组 B: Logging + Error Handling (2个可并行)

#### Week 2-5: Phase 2 - Skills RAG + Code Generation 🆕 扩展
**目标**: 实现基于公司规范的代码生成和本地开发环境

**Week 2: Skills Loader + Code Generation**
1. Skills Loader (3天)
   - Skill Model + Markdown Parser
   - Skills Scanner + Loader Core
   - Skills Loader API

2. Code Generation Core (2天) 🆕
   - Code Generator Core
   - Code Template Engine

**Week 3: Skills Retriever + Code Change Management**
3. Skills Retriever (3天)
   - Keyword Matcher + Tag Filter
   - Skills Retriever Core

4. Code Change Management (2天) 🆕
   - Code Change Tracker
   - Code Review UI

**Week 4: Context Builder + Local Dev Environment**
5. Context Builder (2天)
   - Token Counter + Content Truncator
   - Context Composer + Builder Core

6. Local Development Environment (3天) 🆕
   - Dev Environment Manager
   - Hot Reload Support
   - Log Viewer

**Week 5: LLM Integration + Testing Tools + Debug**
7. LLM Integration (3天)
   - LLM Client
   - Agent Integration + Context Injection

8. Manual Testing & Debug (2天) 🆕
   - Test Case Manager + Manual Test UI
   - Debug Integration + Error Tracker

9. Integration & Testing (2天)
   - Skills Cache + Tests
   - Code Generation API + Dev Environment API
   - Frontend Integration + Documentation

**新增任务**:
- TASK-2.3.1~15: 代码生成与本地开发（15个任务）

**并行任务组**:
- 组 A: Skills Templates (4个可并行)
- 组 B: Keyword/Tag/Fuzzy Matcher (3个可并行)
- 组 C: Token/Truncator/Sorter (3个可并行)
- 组 D: Code Generator + Template Engine (2个可并行) 🆕
- 组 E: Dev Environment + Hot Reload + Log Viewer (3个可并行) 🆕

#### Week 6: Phase 3 - TFS Integration
**目标**: 与企业工作流集成

**关键任务**:
1. Real TFS Integration (2天)
   - azure-devops SDK
   - REST API 调用
   - 需求ID查询功能 🆕

2. Work Item Sync + Code Commit (2天)
   - 双向同步
   - 冲突解决
   - 代码提交到TFS 🆕
   - Pull Request 自动化 🆕

3. Session-Requirement Binding (2天) 🆕
   - Session 与需求ID绑定
   - 历史查询功能
   - Session 重放功能

4. Build Integration + Testing (1天)
   - 触发构建
   - 状态监控
   - 集成测试

**新增任务**:
- TASK-3.1.3: Requirement Query by ID
- TASK-3.1.5: Code Commit to TFS
- TASK-3.1.6: Pull Request Automation
- TASK-3.4.5: Session-Requirement Binding
- TASK-3.4.6: Session History Query
- TASK-3.4.7: Session Replay for Bug Fix
- TASK-3.4.8: Session Binding API

#### Week 7: Phase 4 - Stability & Testing
**目标**: 确保生产就绪

**关键任务**:
1. Feature Flags (2天)
   - Infrastructure + Integration + UI

2. Degradation Strategy (2天)
   - LLM Fallback
   - RAG Fallback
   - TFS Fallback

3. Rollback & Recovery (2天)
   - Data Migration
   - Backup & Restore
   - Health Check
   - Circuit Breaker

4. Testing (2.5天) 🆕
   - Resilience Tests
   - E2E Tests
   - Stress Tests
   - Post-Development Test Workflow 🆕
   - Test Report Generator 🆕

**新增任务**:
- TASK-4.4.4: Post-Development Test Workflow
- TASK-4.4.5: Test Report Generator

**并行任务组**:
- 组 A: LLM/RAG/TFS Fallback (3个可并行)
- 组 B: Migration/Backup/Health/Circuit (4个可并行)

### 7.3 Timeline (时间线) - Optimized v0.6.0 🆕 **已更新**

```
🔥 MVP (9 Weeks) - P0 Priority 🆕 **调整后** (+2周)
├── Week 1: Phase 1 - Foundation & Contract
│   ├── Backend Infrastructure (2天)
│   ├── OpenSpec Schema v0.2 (2天)
│   ├── Frontend Integration (1天)
│   └── Testing (1天)
│
├── Week 2-6: Phase 2 - Skills RAG + Code Generation 🆕 **扩展** (+1周)
│   ├── Week 2: Skills Loader + Code Generation Core (5天)
│   ├── Week 3: Retriever + Code Change Management (5天)
│   ├── Week 4: Context Builder + Local Dev Environment (5天)
│   ├── Week 5: LLM Integration + Testing Tools + Debug (5天)
│   └── Week 6: Frontend UI Implementation (5天) 🆕 **新增**
│
├── Week 7-8: Phase 3 - TFS Integration 🆕 **扩展** (+1周)
│   ├── Week 7: TFS Integration + Testing (5天)
│   │   ├── Real TFS Integration (2天)
│   │   ├── Work Item Sync + Code Commit (2天)
│   │   └── TFS Integration Tests (1天) 🆕
│   └── Week 8: Session Management + Frontend UI (5天)
│       ├── Session-Requirement Binding (2天)
│       ├── Build Integration (1天)
│       └── Frontend UI + Tests (2天) 🆕
│
└── Week 9: Phase 4 - Stability & Testing
    ├── Feature Flags (2天)
    ├── Degradation Strategy (2天)
    ├── Rollback & Recovery (2天)
    └── E2E + Stress Testing (2天)

📋 Post-MVP (4-8 Weeks) - P1 Priority
├── Phase 5: Multi-Agent (简化版)
│   ├── PM Agent
│   ├── Architect Agent
│   └── Developer Agent
│
└── Phase 7: Testing Automation (部分)
    ├── Test Generator
    └── Test Runner

🔮 Future Iterations - P2 Priority
├── Phase 5: Enhanced Collaboration
├── Phase 6: Enhanced Superpower (Vector RAG)
├── Phase 8: Model & Performance
├── Phase 9: UI/UX Enhancement
└── Phase 10: Enterprise Features
```

### 7.4 Resource Requirements (资源需求) - Optimized v0.6.0 🆕 **已更新**

**团队配置** (MVP - 9周) 🆕 **调整后**:
- **后端开发**: 2 人（Python, FastAPI, LLM 集成，代码生成）
- **前端开发**: 2.5 人（SolidJS, Tauri, 代码审查UI, 日志查看器）🆕 **增加 1 人**
- **AI 工程师**: 1 人（Prompt 工程，RAG 优化）
- **测试工程师**: 1 人（测试和质量保证）🆕 **增加 0.5 人**
- **总计**: 6.5 人（原 5 人，增加 1.5 人）🆕

**技术栈**:
- Python 3.10+, FastAPI, Pydantic
- `python-frontmatter` - YAML frontmatter 解析
- `tiktoken` - Token 计数
- `jieba` - 中文分词
- `rapidfuzz` - 模糊匹配
- `watchdog` - 文件监听
- OpenAI/Anthropic SDK - LLM 集成

**基础设施**:
- 开发环境：本地 + Docker
- CI/CD：GitHub Actions
- 测试：pytest, coverage
- 文档：MkDocs 或 Docusaurus

### 7.5 Success Metrics (成功指标) - Optimized

**Week 1 (Phase 1) 成功指标**:
- ✅ Backend 服务可启动，健康检查通过
- ✅ OpenSpec v0.2 Schema 定义完整
- ✅ Forge UI 可生成和展示 OpenSpec
- ✅ 单元测试覆盖率 > 80%

**Week 2-6 (Phase 2) 成功指标** 🆕 **已更新**:
- ✅ 可加载 100+ Skills < 1s
- ✅ 检索延迟 < 50ms，准确率 > 75%
- ✅ 上下文构建延迟 < 100ms
- ✅ Agent 生成代码符合规范率 > 80%
- ✅ LLM 响应质量提升 > 30%
- ✅ 代码生成功能可用，准确率 > 80% 🆕
- ✅ 本地开发环境可启动/停止，成功率 > 95% 🆕
- ✅ 热重载延迟 < 2s 🆕
- ✅ 日志查看器实时显示，延迟 < 100ms 🆕
- ✅ 测试覆盖率 > 80%
- ✅ 归档功能正常，成功率 > 95%

**Week 7-8 (Phase 3) 成功指标** 🆕 **已更新**:
- ✅ TFS 连接成功率 > 99%
- ✅ 需求ID查询延迟 < 500ms
- ✅ Work Item 同步准确率 100%
- ✅ 代码提交成功率 > 99%
- ✅ PR 自动创建成功率 > 95%
- ✅ Session-需求ID绑定成功率 100%
- ✅ Session 历史查询响应时间 < 200ms
- ✅ 构建触发成功率 > 99%
- ✅ TFS 集成测试覆盖率 > 80% 🆕
- ✅ Session 管理测试覆盖率 > 80% 🆕

**Week 9 (Phase 4) 成功指标** 🆕 **已更新**:
- ✅ Feature Flags 可动态开关
- ✅ LLM/RAG/TFS 故障时系统仍可用
- ✅ 数据可安全迁移和回滚
- ✅ E2E 测试通过率 100%
- ✅ 测试自动化流程成功率 > 90% 🆕
- ✅ 100 并发用户，P95 延迟 < 2s
- ✅ 无内存泄漏

**MVP 整体成功指标**:
- ✅ 用户可输入需求，生成符合公司规范的 OpenSpec
- ✅ 基于 Skills 的代码生成准确率 > 80%
- ✅ TFS Work Items 可双向同步
- ✅ 可通过需求ID查询完整需求信息 🆕
- ✅ 代码可自动提交到TFS并创建PR 🆕
- ✅ Session 与需求ID强绑定，可查询历史 🆕
- ✅ 开发完成后自动归档到 Superpower 🆕
- ✅ 开发完成后自动触发测试 🆕
- ✅ 系统稳定，有降级策略和回滚能力
- ✅ 测试覆盖率 > 80%
- ✅ 用户满意度 > 4.0/5.0
- ✅ 文档完整度 > 90%

### 7.6 Milestones (里程碑) - Optimized v0.6.0 🆕 **已更新**

- **M0 (Week 9)**: MVP 交付 🔥 🆕 **调整** (原 Week 6)
  - 完成 Phase 1-4
  - 验收标准：用户可完成需求 → OpenSpec → 代码生成 → 本地开发 → TFS 提交的完整流程
  - 系统稳定，有降级和回滚能力
  - 50+ UI 组件全部实现 🆕
  - 测试覆盖率 > 80%

- **M1 (Week 13)**: 增强功能 📋 🆕 **调整** (原 Week 10)
  - 完成 Multi-Agent 简化版 (3个核心 Agent)
  - 完成 Testing Automation 基础功能
  - 验收标准：多智能体协作流畅，自动化测试可用

- **M2 (根据反馈)**: 协作与性能 🔮
  - 实时协作和会话共享
  - 性能优化和多模型支持
  - 验收标准：支持 5 人团队协作，性能提升 > 50%

- **M3 (根据反馈)**: 企业级完善 🔮
  - 完成所有企业特性
  - 性能优化和安全加固
  - 验收标准：通过企业级安全审计，支持 50+ 用户

## 8. Risk Assessment / 风险评估

### 8.1 Technical Risks (技术风险)

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| **多智能体协调复杂度** | 高 | 中 | 采用成熟的消息总线，充分测试 |
| **LLM 响应不稳定** | 中 | 高 | 实现重试机制、降级策略、缓存 |
| **向量搜索性能** | 中 | 中 | 使用 Qdrant，优化索引策略 |
| **实时协作冲突** | 中 | 中 | 实现 OT 算法，充分测试边界情况 |
| **TFS API 变更** | 低 | 低 | 抽象 TFS 接口，易于适配 |

### 8.2 Business Risks (业务风险)

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| **用户接受度** | 高 | 中 | 充分的用户培训和文档 |
| **AI 成本过高** | 中 | 中 | 实现成本追踪和预算控制 |
| **数据安全合规** | 高 | 低 | 严格的权限控制和审计日志 |
| **团队技能差距** | 中 | 中 | 技术培训和知识分享 |

## 9. Success Metrics / 成功指标

### 9.1 Technical Metrics (技术指标)

- **性能指标**:
  - API 响应时间 < 200ms (P95)
  - 向量搜索延迟 < 100ms
  - WebSocket 消息延迟 < 50ms
  - 系统可用性 > 99.5%

- **质量指标**:
  - 代码覆盖率 > 80%
  - 生成代码通过 Linter 率 > 95%
  - 安全漏洞检测准确率 > 90%
  - 用户报告 Bug 数 < 5/月

### 9.2 Business Metrics (业务指标)

- **效率提升**:
  - 需求到代码时间减少 > 50%
  - 代码审查时间减少 > 40%
  - Bug 修复时间减少 > 30%
  - 部署频率提升 > 100%

- **用户满意度**:
  - 用户满意度评分 > 4.0/5.0
  - 日活跃用户 > 80%
  - 功能使用率 > 60%
  - 用户留存率 > 90%

- **成本效益**:
  - AI 成本 < $500/用户/月
  - ROI > 200% (第一年)
  - 开发效率提升 > 2x

## 10. Conclusion / 总结

### 10.1 Core Advantages (核心优势)

1. **Forge 核心界面**: 已实现完整的需求输入和 OpenSpec 生成界面，用户体验流畅
2. **基于成熟基础**: OpenWork 已有完整的桌面应用、TFS 集成、OpenSpec 契约层、Superpower 资产层
3. **多智能体协作**: 引入 Eigent AI 理念，实现专业化智能体协同工作
4. **全流程自动化**: 从需求分析到代码发布的完整自动化流程
5. **企业级特性**: 权限管理、审计日志、安全扫描、合规检查
6. **团队协作**: 实时协作、会话共享、多人开发支持
7. **可扩展性**: MCP、Skills、Plugins 扩展机制，易于定制

### 10.2 Differentiation (差异化)

与市面上其他 AI 编程工具相比，Enterprise Forge 的差异化优势：

- **Forge 核心入口**: 简洁直观的需求输入界面，自动生成结构化 OpenSpec 契约
- **契约驱动**: OpenSpec 作为需求、设计、代码的一致性契约
- **资产中心化**: Superpower Layer 提供公司内部代码和文档的智能检索
- **企业集成**: 深度集成 TFS/Azure DevOps，符合企业开发流程
- **多智能体**: 专业化智能体协作，而非单一 AI 助手
- **全流程**: 覆盖需求、设计、开发、测试、审查、构建、发布全流程

### 10.3 Next Steps (下一步)

1. **立即开始**: Phase 4 多智能体增强开发
2. **组建团队**: 2-3 名后端开发 + 1 名前端开发 + 1 名 AI 工程师
3. **设置环境**: 搭建开发环境、CI/CD 流水线、监控系统
4. **迭代开发**: 按照 Phase 4-10 的计划逐步实现
5. **用户反馈**: 每个 Phase 完成后收集用户反馈，快速迭代

---

**Document Version**: 0.5.0 (Optimized with Code Generation & Local Development) 🆕
**Last Updated**: 2026-01-30
**Author**: AI Development Team
**Status**: Optimized & Ready for MVP Implementation 🚀

**v0.5.0 Major Optimization** (基于 v0.4.1):
- ✅ **补充代码生成与本地开发模块** (Phase 2 新增 15 个核心任务) 🔥
  - 代码生成器（基于 OpenSpec + Skills）
  - 代码变更追踪和可视化
  - 本地开发环境管理
  - 热重载支持
  - 日志查看器
  - 手动测试工具
  - 调试支持
  - 错误追踪器
- ✅ **调整 MVP 时间线**: 6周 → 7周（+1周用于核心开发功能）
- ✅ **更新任务统计**: Phase 2 从 48 个任务扩展到 63 个任务
- ✅ **优化开发流程**: 更符合实际研发习惯，补充人工介入点

**关键改进**:
1. ✅ 补充了"代码生成"环节（TASK-2.3.1~2）
2. ✅ 补充了"代码变更管理"环节（TASK-2.3.3~4）
3. ✅ 补充了"本地开发环境"环节（TASK-2.3.5~7）
4. ✅ 补充了"手动测试工具"环节（TASK-2.3.8~9）
5. ✅ 补充了"调试支持"环节（TASK-2.3.10~11）
6. ✅ 增加了"人工介入点"（代码审查、自测确认、提交确认）
7. ✅ 流程更符合实际研发习惯

**v0.4.1 Enhancement Summary** (基于 v0.4.0):
- ✅ 补充 OpenSpec 版本管理功能 (Phase 1 新增 1 个任务)
  - 审批前只保存草稿（draft.json），不创建版本号
  - 审批通过后自动生成版本号（v1, v2...）
- ✅ 补充 OpenSpec 归档到 TFS 功能 (Phase 1 新增 1 个任务，P1 可选)
  - 主要存储在项目本地，TFS 归档为可选功能
- ✅ 补充 OpenSpec 生命周期管理 (Phase 1 新增 1 个任务)
  - 状态流转：draft → review → approved（触发版本生成）→ archived
- ✅ 更新任务统计

**v0.4.0 Enhancement Summary** (基于 v0.3.0):
- ✅ 补充 Superpower 归档系统 (Phase 2 新增 4 个任务)
- ✅ 补充需求ID查询功能 (Phase 3 新增 1 个任务)
- ✅ 补充代码提交和PR自动化 (Phase 3 新增 2 个任务)
- ✅ 补充 Session-需求ID绑定 (Phase 3 新增 4 个任务)
- ✅ 补充测试自动化工作流 (Phase 4 新增 2 个任务)
- ✅ 更新任务统计和时间线
- ✅ 更新成功指标

**新增任务总计**: 31 个
- Phase 1: +3 任务 (25 → 28，含版本管理、TFS归档、生命周期管理)
- Phase 2: +19 任务 (44 → 63，含 Skills RAG + 代码生成与本地开发) 🔥
- Phase 3: +7 任务 (16 → 24，含需求查询、代码提交、Session绑定)
- Phase 4: +2 任务 (13 → 15)

**MVP 周期**: 6周 → **7周** (+1周)

**覆盖完整功能流程**:
1. ✅ 研发通过需求ID查询TFS需求详情
2. ✅ AI分析生成符合OpenSpec的开发计划（draft 状态）
3. ✅ OpenSpec 保存到项目本地，与需求ID关联 🆕
4. ✅ 研发编辑完善开发计划（draft.json，覆盖式保存）
5. ✅ 研发提交审批（review 状态）
6. ✅ 审批通过后自动生成版本号（v1, approved 状态）🆕
7. ✅ 多智能体协作开发
8. ✅ 每阶段完成后归档到Superpower
9. ✅ 开发完成后自动触发测试
10. ✅ 代码自动���交到TFS并创建PR
11. ✅ Session与需求ID绑定，可查询历史用于Bug修复
12. ✅ 开发完成后 OpenSpec 状态变为 archived

**Optimization Summary** (v0.3.0):
- ✅ 聚焦 6 周 MVP (Phase 1-4)
- ✅ 任务原子化 (0.5-2天/任务)
- ✅ 明确依赖关系 (Mermaid 图)
- ✅ 完善测试策略 (5层测试金字塔)
- ✅ 添加稳定性保障 (Feature Flags + 降级 + 回滚)
