from __future__ import annotations

from app.schemas import Requirement


def build_pm_prompt(requirement: Requirement, context: str, workspace_info: dict = None) -> tuple[str, str]:
    system = "You are a product manager. Produce concise user stories and acceptance criteria in JSON. Please respond in Simplified Chinese."

    # 只在有相关context时才包含，避免无关信息干扰
    context_section = ""
    if context and context.strip():
        context_section = f"参考以下相关规范和最佳实践：\n{context}\n\n"

    # 添加工作区特定信息，增强项目感知
    workspace_section = ""
    if workspace_info and workspace_info.get("project_context"):
        project_name = workspace_info.get('project_name', 'unknown')
        tech_stack = workspace_info.get('tech_stack', 'unknown')
        framework = workspace_info.get('framework', 'unknown')
        project_type = workspace_info.get('project_type', 'unknown')

        workspace_section = f"当前工作区: {project_name} ({tech_stack} + {framework})\n"
        if project_type != "unknown":
            workspace_section += f"项目类型: {project_type}\n"

    # 根据项目类型调整需求分析要求
    project_type = workspace_info.get("project_type", "unknown") if workspace_info else "unknown"

    if project_type == "frontend":
        requirements_guidance = (
            f"**项目背景**: 这是一个 {workspace_info.get('tech_stack', 'Vue3')} + {workspace_info.get('framework', 'Spark')} 前端项目。\n"
            "请基于前端开发的特点，生成精准的产品需求文档。\n\n"
            "返回JSON格式，包含以下字段：\n"
            "- summary: 需求概要（简洁明了，突出前端功能特性）\n"
            "- description: 详细描述（针对具体的前端交互需求）\n"
            "- acceptance_criteria: 验收标准列表（具体可测试的前端功能条件）\n\n"
            "**需求分析要点**:\n"
            "- 重点关注用户界面和交互体验\n"
            "- 考虑组件的可复用性和可维护性\n"
            "- 明确前端数据流和状态管理需求\n"
            "- 避免涉及后端API的具体实现细节\n"
            "- 验收标准应该是前端可验证的功能点\n"
        )
    else:
        requirements_guidance = (
            "基于用户需求，生成精准的产品需求文档。\n"
            "返回JSON格式，包含以下字段：\n"
            "- summary: 需求概要（简洁明了）\n"
            "- description: 详细描述（针对具体需求）\n"
            "- acceptance_criteria: 验收标准列表（具体可测试的条件）\n\n"
        )

    user = (
        f"{workspace_section}"
        f"{context_section}"
        f"{requirements_guidance}"
        "请确保内容与用户需求高度相关，避免添加无关功能。\n"
        "特别注意：需求分析应该符合当前项目的技术特点和开发模式。\n\n"
        f"用户需求概要：{requirement.summary}\n"
        f"用户需求描述：{requirement.description}\n"
    )
    return system, user


def build_architect_prompt(requirement: Requirement, context: str, workspace_info: dict = None) -> tuple[str, str]:
    system = "You are a software architect. Produce architecture and API design in JSON. Please respond in Simplified Chinese."

    # 只在有相关context时才包含，避免无关信息干扰
    context_section = ""
    if context and context.strip():
        context_section = f"参考以下技术规范和架构模式：\n{context}\n\n"

    # 添加工作区技术栈信息和专门化指导
    tech_stack_section = ""
    project_type = workspace_info.get("project_type", "unknown") if workspace_info else "unknown"

    if workspace_info:
        tech_stack = workspace_info.get("tech_stack", "unknown")
        framework = workspace_info.get("framework", "unknown")
        ui_library = workspace_info.get("ui_library", "")

        if tech_stack != "unknown":
            tech_stack_section = f"目标技术栈: {tech_stack} + {framework}\n"
            tech_stack_section += f"项目: {workspace_info.get('project_name', 'unknown')}\n"
            tech_stack_section += f"项目类型: {project_type}\n"

            if ui_library:
                tech_stack_section += f"UI组件库: {ui_library}\n"

    # 根据项目类型调整设计要求，增强工作区感知
    if project_type == "frontend":
        design_requirements = (
            f"基于用户需求和目标技术栈，设计前端组件架构。\n"
            f"**重要提醒**: 这是一个 {workspace_info.get('tech_stack', 'Vue3')} + {workspace_info.get('framework', 'Spark')} 前端项目，"
            f"请严格遵循该技术栈的架构模式和最佳实践。\n\n"
            "返回JSON格式，包含以下字段：\n"
            "- architecture_overview: 前端架构概述（组件结构、状态管理、路由设计）\n"
            "  * 必须基于当前项目的技术栈和框架\n"
            "  * 遵循工作区文档中的架构模式\n"
            "  * 引用具体的代码规范和组件结构\n"
            "- api_endpoints: 前端需要调用的API接口列表（如果需要），每个包含 method, path, description\n"
            "- data_models: 前端数据模型列表（组件props、state、store等），每个包含：\n"
            "  - name: 模型名称（如 CalculatorState, ButtonProps等）\n"
            "  - fields: 字段列表，每个字段包含 name, type, required 属性\n\n"
            "**架构设计原则**:\n"
            "- 重点关注前端组件设计，不要设计后端API实现\n"
            "- data_models应该是Vue组件相关的数据结构\n"
            "- 如果是纯前端功能（如计算器），api_endpoints可以为空\n"
            "- 严格遵循工作区的开发规范和代码风格\n"
            "- 避免生成与当前技术栈不符的内容\n"
        )
    else:
        design_requirements = (
            "基于用户需求和目标技术栈，设计简洁实用的技术架构。\n"
            "返回JSON格式，包含以下字段：\n"
            "- architecture_overview: 架构概述（针对具体需求的技术方案）\n"
            "- api_endpoints: API端点列表，每个包含 method, path, description\n"
            "- data_models: 数据模型列表，每个包含：\n"
            "  - name: 模型名称\n"
            "  - fields: 字段列表，每个字段包含 name, type, required 属性\n\n"
        )

    user = (
        f"{tech_stack_section}"
        f"{context_section}"
        f"{design_requirements}"
        "请确保架构设计与需求和技术栈匹配，避免过度设计。\n"
        "特别注意：必须完全符合工作区的技术规范和架构模式。\n\n"
        f"用户需求概要：{requirement.summary}\n"
        f"用户需求描述：{requirement.description}\n"
    )
    return system, user


def build_developer_prompt(requirement: Requirement, context: str, workspace_info: dict = None) -> tuple[str, str]:
    system = "You are a senior developer. Propose an implementation task list in JSON. Please respond in Simplified Chinese."

    # 只在有相关context时才包含，避免无关信息干扰
    context_section = ""
    if context and context.strip():
        context_section = f"参考以下开发规范和最佳实践：\n{context}\n\n"

    # 添加工作区开发环境信息，增强工作区感知
    dev_env_section = ""
    project_type = workspace_info.get("project_type", "unknown") if workspace_info else "unknown"

    if workspace_info:
        tech_stack = workspace_info.get("tech_stack", "unknown")
        framework = workspace_info.get("framework", "unknown")
        ui_library = workspace_info.get("ui_library", "")

        if tech_stack != "unknown":
            dev_env_section = f"开发环境: {tech_stack} + {framework}\n"
            dev_env_section += f"项目结构: {workspace_info.get('project_name', 'unknown')}\n"
            dev_env_section += f"项目类型: {project_type}\n"

            if ui_library:
                dev_env_section += f"UI组件库: {ui_library}\n"

    # 根据项目类型调整任务要求，基于工作区规范
    if project_type == "frontend":
        task_requirements = (
            f"基于用户需求和前端开发环境，制定具体的前端开发任务清单。\n"
            f"**重要提醒**: 这是一个 {workspace_info.get('tech_stack', 'Vue3')} + {workspace_info.get('framework', 'Spark')} 前端项目，"
            f"请严格遵循该项目的开发规范和构建流程。\n\n"
            "返回JSON格式，包含以下字段：\n"
            "- tasks: 任务列表，每个任务包含：\n"
            "  - title: 任务标题（简洁明确）\n"
            "  - description: 任务描述（具体的前端实现要求）\n\n"
            "**开发任务要求**:\n"
            "- 任务应该专注于前端组件开发、样式设计、交互逻辑\n"
            "- 使用Vue3 Composition API和TypeScript（如果项目支持）\n"
            "- 遵循项目的代码规范和组件结构\n"
            "- 引用工作区文档中的构建命令和开发流程\n"
            "- 如果需要状态管理，考虑使用Pinia或项目指定的状态管理方案\n"
            "- 包含项目特定的测试和验证要求\n"
            "- 考虑项目的部署和配置要求\n"
            "- 不要包含后端API开发任务\n"
            "- 严格按照工作区的开发指南执行\n"
        )
    else:
        task_requirements = (
            "基于用户需求和开发环境，制定具体的开发任务清单。\n"
            "返回JSON格式，包含以下字段：\n"
            "- tasks: 任务列表，每个任务包含：\n"
            "  - title: 任务标题（简洁明确）\n"
            "  - description: 任务描述（具体的实现要求）\n\n"
        )

    user = (
        f"{dev_env_section}"
        f"{context_section}"
        f"{task_requirements}"
        "请确保任务列表针对具体需求和技术栈，避免添加不必要的任务。\n"
        "任务应该按照开发顺序排列，每个任务应该是独立可完成的。\n"
        "特别注意：必须完全遵循工作区的开发规范、构建流程和代码风格。\n\n"
        f"用户需求概要：{requirement.summary}\n"
        f"用户需求描述：{requirement.description}\n"
    )
    return system, user


def build_opencode_spec_prompt(requirement: Requirement, context: str, workspace_info: dict = None) -> str:
    """
    构建OpenCode专用的spec生成prompt
    确保输出格式严格符合OpenSpec v0.2.0结构

    Args:
        requirement: 需求信息
        context: 上下文信息
        workspace_info: 工作区信息（可选）

    Returns:
        str: 完整的prompt文本
    """

    # 构建工作区信息部分
    workspace_section = ""
    if workspace_info:
        project_name = workspace_info.get('project_name', 'unknown')
        tech_stack = workspace_info.get('tech_stack', 'unknown')
        framework = workspace_info.get('framework', 'unknown')
        project_type = workspace_info.get('project_type', 'unknown')

        workspace_section = f"""
## 工作区信息
- 项目名称: {project_name}
- 技术栈: {tech_stack} + {framework}
- 项目类型: {project_type}
"""

    # 构建上下文部分
    context_section = ""
    if context and context.strip():
        context_section = f"""
## 项目上下文
{context}
"""

    # 构建主要prompt
    prompt = f"""你是一个专业的软件架构师和产品经理。请基于用户需求生成完整的OpenSpec开发规范。

{workspace_section}
{context_section}

## 用户需求
**概要**: {requirement.summary}
**详细描述**: {requirement.description}
**验收标准**: {', '.join(requirement.acceptance_criteria) if requirement.acceptance_criteria else '待定义'}

## 输出要求
请严格按照以下JSON格式输出，确保数据结构完全符合OpenSpec v0.2.0规范：

```json
{{
  "spec_version": "0.2.0",
  "project_name": "项目名称（基于需求生成合适的名称）",
  "requirement": {{
    "summary": "{requirement.summary}",
    "description": "{requirement.description}",
    "acceptance_criteria": {requirement.acceptance_criteria if requirement.acceptance_criteria else '["待完善验收标准"]'}
  }},
  "design": {{
    "architecture_overview": "# 技术架构概述\\n\\n## 系统架构\\n详细的Markdown格式架构说明，包括：\\n- 整体架构设计\\n- 技术选型说明\\n- 核心模块划分\\n- 数据流设计\\n- 安全考虑\\n\\n## 实现要点\\n- 关键技术实现方案\\n- 性能优化策略\\n- 可扩展性设计",
    "api_endpoints": [
      {{
        "method": "POST",
        "path": "/api/example",
        "description": "API描述",
        "request_model": {{"field": "type"}},
        "response_model": {{"result": "type"}}
      }}
    ],
    "data_models": [
      {{
        "name": "ModelName",
        "fields": [
          {{"name": "field1", "type": "string", "required": true}},
          {{"name": "field2", "type": "number", "required": false}}
        ]
      }}
    ],
    "tech_stack": {{
      "frontend": "技术栈",
      "backend": "技术栈",
      "database": "数据库",
      "deployment": "部署方案"
    }},
    "dependencies": ["依赖1", "依赖2"]
  }},
  "tasks": [
    {{
      "id": "task-1",
      "title": "任务标题",
      "description": "详细的任务描述，包括具体的实现要求和验收标准",
      "status": "pending",
      "file_changes": ["src/components/Example.vue", "src/api/example.ts"],
      "assigned_agent": null,
      "dependencies": []
    }}
  ]
}}
```

## 生成要求

### 1. 技术规范 (design.architecture_overview)
- 使用Markdown格式编写详细的技术架构文档
- 包含系统架构图的文字描述
- 详细说明技术选型和实现方案
- 考虑性能、安全、可扩展性等非功能性需求
- 内容应该丰富详实，至少包含500字的架构说明

### 2. API设计 (design.api_endpoints)
- 设计完整的API接口规范
- 包含请求和响应的数据模型
- 考虑RESTful设计原则
- 包含错误处理和状态码说明

### 3. 数据模型 (design.data_models)
- 设计完整的数据结构
- 包含字段类型和约束
- 考虑数据关系和完整性
- 符合业务逻辑需求

### 4. 实现计划 (tasks)
- 将需求分解为具体的开发任务
- 每个任务应该是独立可完成的
- 按照开发顺序排列
- 包含具体的文件变更列表
- 任务描述应该详细具体，便于开发人员执行

### 5. 技术栈选择
- 基于项目需求选择合适的技术栈
- 考虑团队技能和项目复杂度
- 包含主要依赖和工具链

## 注意事项
1. 输出必须是有效的JSON格式，不要包含任何其他内容
2. 所有字符串中的换行符使用\\n表示
3. 确保所有必需字段都有值，不能为null或空
4. 任务ID使用简单的字符串格式（如task-1, task-2）
5. 文件路径使用相对路径，符合项目结构
6. 架构概述要详细具体，不要使用占位符文本

请基于以上要求生成完整的OpenSpec规范。"""

    return prompt
