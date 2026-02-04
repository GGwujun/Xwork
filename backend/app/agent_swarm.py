import json
import uuid
from typing import Any

from app.context_server import context_server
from app.llm.client import LlmClient
from app.prompts.templates import build_architect_prompt, build_developer_prompt, build_pm_prompt
from app.schemas import ApiEndpoint, DataModel, Design, OpenSpec, Requirement, Task
from app.workspace_analyzer import workspace_analyzer

class AgentSwarm:
    def __init__(self):
        pass

    async def generate_spec(self, requirements: Requirement, workspace_path: str = None) -> OpenSpec:
        """
        Orchestrate the PM and Architect agents to generate an OpenSpec.
        """
        # 分析目标工作区环境
        workspace_info = workspace_analyzer.analyze_workspace(workspace_path) if workspace_path else {}

        # 构建精准的查询，结合需求描述和概要
        query = f"{requirements.summary} {requirements.description}".strip()

        # 分类需求类型，用于智能内容选择
        req_type = workspace_analyzer.classify_requirement_type(requirements)

        # 动态分配 token 预算
        token_allocation = self._allocate_token_budget(requirements, workspace_info, req_type)

        # 根据需求内容和工作区信息智能选择相关的 skills
        context, _skills = context_server.build_skills_context(
            query=query,
            tags=self._extract_relevant_tags(requirements, workspace_info),
            top_k=token_allocation["skills_count"],
            max_tokens=token_allocation["skills_tokens"],
        )

        # 将工作区信息融入 context，使用智能内容选择
        enhanced_context = self._build_enhanced_context(context, workspace_info, requirements, token_allocation)

        client = LlmClient()

        pm_system, pm_user = build_pm_prompt(requirements, enhanced_context, workspace_info)
        pm_response = await client.generate(pm_system, pm_user)
        pm_json = _parse_json(pm_response)

        arch_system, arch_user = build_architect_prompt(requirements, enhanced_context, workspace_info)
        arch_response = await client.generate(arch_system, arch_user)
        arch_json = _parse_json(arch_response)

        dev_system, dev_user = build_developer_prompt(requirements, enhanced_context, workspace_info)
        dev_response = await client.generate(dev_system, dev_user)
        dev_json = _parse_json(dev_response)

        # 使用工作区项目名称，如果可用的话
        project_name = workspace_info.get("project_name", f"Project-{uuid.uuid4().hex[:8]}")
        if project_name == "unknown":
            project_name = f"Project-{uuid.uuid4().hex[:8]}"

        # 安全地创建 DataModel 实例
        data_models = []
        for item in arch_json.get("data_models", []):
            try:
                # 确保 fields 字段存在
                if "fields" not in item:
                    item["fields"] = []
                data_models.append(DataModel(**item))
            except Exception as e:
                print(f"Warning: Failed to create DataModel from {item}: {e}")
                # 创建一个默认的 DataModel
                data_models.append(DataModel(
                    name=item.get("name", "UnknownModel"),
                    fields=[]
                ))

        design = Design(
            architecture_overview=_normalize_architecture_overview(
                arch_json.get("architecture_overview", "")
            ),
            api_endpoints=[ApiEndpoint(**item) for item in arch_json.get("api_endpoints", [])],
            data_models=data_models,
        )

        tasks = [
            Task(
                id=str(uuid.uuid4()),
                title=task.get("title", "Untitled Task"),
                description=task.get("description", ""),
                status="pending",
            )
            for task in dev_json.get("tasks", [])
        ]

        requirements.summary = pm_json.get("summary", requirements.summary)
        requirements.description = pm_json.get("description", requirements.description)
        requirements.acceptance_criteria = pm_json.get("acceptance_criteria", requirements.acceptance_criteria)

        return OpenSpec(
            project_name=project_name,
            requirement=requirements,
            design=design,
            tasks=tasks,
        )

    def _extract_relevant_tags(self, requirements: Requirement, workspace_info: dict = None) -> list[str]:
        """
        根据需求内容和工作区信息提取相关标签，用于精准匹配 skills
        """
        tags = []
        content = f"{requirements.summary} {requirements.description}".lower()

        # 优先使用工作区技术栈信息
        if workspace_info:
            tech_stack = workspace_info.get("tech_stack", "").lower()
            framework = workspace_info.get("framework", "").lower()

            if tech_stack == "vue3" or "vue" in tech_stack:
                tags.append('vue')
                tags.append('frontend')
            elif tech_stack == "react":
                tags.append('react')
                tags.append('frontend')
            elif tech_stack == "solidjs":
                tags.append('solidjs')
                tags.append('frontend')
            elif tech_stack == "angular":
                tags.append('angular')
                tags.append('frontend')

            # 框架特定标签
            if framework == "spark":
                tags.append('spark')
            elif framework == "next":
                tags.append('nextjs')

        # 技术栈相关标签（基于需求内容）
        if any(keyword in content for keyword in ['前端', 'frontend', 'ui', 'react', 'vue', 'angular']):
            tags.append('frontend')
        if any(keyword in content for keyword in ['后端', 'backend', 'api', 'server', 'database']):
            tags.append('backend')
        if any(keyword in content for keyword in ['数据库', 'database', 'sql', 'mysql', 'postgresql']):
            tags.append('database')

        # 功能类型标签
        if any(keyword in content for keyword in ['用户', 'user', '登录', 'login', '认证', 'auth']):
            tags.append('user-management')
        if any(keyword in content for keyword in ['报告', 'report', '统计', 'analytics', '图表', 'chart']):
            tags.append('reporting')
        if any(keyword in content for keyword in ['支付', 'payment', '订单', 'order', '交易', 'transaction']):
            tags.append('payment')
        if any(keyword in content for keyword in ['计算器', 'calculator', '计算', 'calculate']):
            tags.append('calculator')

        # 如果没有匹配到特定标签，返回通用标签
        if not tags:
            tags.append('general')

        return tags

    def _allocate_token_budget(self, requirements: Requirement, workspace_info: dict, req_type) -> dict:
        """
        动态分配 token 预算

        Args:
            requirements: 需求对象
            workspace_info: 工作区信息
            req_type: 需求类型

        Returns:
            dict: token 分配策略
        """
        # 基础分配 (总预算 2000 tokens)
        base_allocation = {
            "workspace_tokens": 800,    # 工作区文档 40%
            "skills_tokens": 600,       # 相关 Skills 30%
            "code_examples_tokens": 400, # 代码示例 20%
            "buffer_tokens": 200,       # 缓冲区 10%
            "skills_count": 3,          # Skills 数量
            "max_sections": 5           # 最大段落数
        }

        # 根据需求类型动态调整
        from app.workspace_analyzer import RequirementType

        if req_type == RequirementType.FRONTEND_COMPONENT:
            # 前端需求 → 增加组件模式权重
            base_allocation.update({
                "workspace_tokens": 1000,   # 增加工作区文档权重
                "skills_tokens": 500,       # 减少 Skills 权重
                "code_examples_tokens": 300,
                "max_sections": 6           # 增加段落数
            })
        elif req_type == RequirementType.ARCHITECTURE_DESIGN:
            # 架构需求 → 增加设计原则权重
            base_allocation.update({
                "workspace_tokens": 900,
                "skills_tokens": 700,       # 增加 Skills 权重
                "code_examples_tokens": 200,
                "skills_count": 4           # 增加 Skills 数量
            })
        elif req_type == RequirementType.CONFIGURATION_SETUP:
            # 配置需求 → 增加环境设置权重
            base_allocation.update({
                "workspace_tokens": 600,
                "skills_tokens": 400,
                "code_examples_tokens": 600,  # 增加代码示例权重
                "max_sections": 4
            })

        # 根据工作区信息调整
        if workspace_info.get("project_type") == "frontend":
            base_allocation["workspace_tokens"] += 100
            base_allocation["skills_tokens"] -= 100

        return base_allocation

    def _build_enhanced_context(self, context: str, workspace_info: dict, requirements: Requirement, token_allocation: dict) -> str:
        """
        将工作区信息融入 context，构建增强的上下文，使用智能内容选择

        Args:
            context: Skills 上下文
            workspace_info: 工作区信息
            requirements: 需求对象
            token_allocation: token 分配策略

        Returns:
            str: 增强的上下文
        """
        if not workspace_info:
            return context

        enhanced_parts = []

        # 1. 项目基础信息 (优先级最高)
        if workspace_info.get("project_context"):
            project_info = f"## 当前工作区信息\n{workspace_info['project_context']}"
            enhanced_parts.append(("project_info", project_info, 1))

        # 2. 智能选择相关的开发指南
        if workspace_info.get("development_guidelines"):
            dev_sections = self._extract_and_score_sections(
                workspace_info["development_guidelines"],
                requirements,
                workspace_info,
                "development_guidelines"
            )
            if dev_sections:
                relevant_dev_content = self._intelligent_truncation(
                    dev_sections,
                    token_allocation["workspace_tokens"] // 3
                )
                if relevant_dev_content:
                    enhanced_parts.append(("dev_guidelines", f"## 开发指南\n{relevant_dev_content}", 2))

        # 3. 智能选择相关的架构信息
        if workspace_info.get("architecture_info"):
            arch_sections = self._extract_and_score_sections(
                workspace_info["architecture_info"],
                requirements,
                workspace_info,
                "architecture"
            )
            if arch_sections:
                relevant_arch_content = self._intelligent_truncation(
                    arch_sections,
                    token_allocation["workspace_tokens"] // 3
                )
                if relevant_arch_content:
                    enhanced_parts.append(("architecture", f"## 架构信息\n{relevant_arch_content}", 3))

        # 4. 相关 Skills 内容 (补充通用最佳实践)
        if context and context.strip():
            skills_content = self._truncate_skills_context(context, token_allocation["skills_tokens"])
            enhanced_parts.append(("skills", f"## 相关技术规范\n{skills_content}", 4))

        # 按优先级排序并组合
        enhanced_parts.sort(key=lambda x: x[2])

        # 去重和优化
        final_content = self._deduplicate_and_optimize([part[1] for part in enhanced_parts])

        return final_content

    def _extract_and_score_sections(self, content: str, requirements: Requirement, workspace_info: dict, section_type: str) -> list:
        """从文档内容中提取并评分段落"""
        try:
            # 使用 workspace_analyzer 的增强段落提取
            if section_type == "development_guidelines":
                patterns = workspace_analyzer.section_patterns["development_guidelines"]
            elif section_type == "architecture":
                patterns = workspace_analyzer.section_patterns["architecture"]
            else:
                patterns = workspace_analyzer.section_patterns.get(section_type, [])

            all_sections = []
            for pattern in patterns:
                sections = workspace_analyzer._extract_section_enhanced(content, [pattern])
                all_sections.extend(sections)

            # 使用智能内容选择
            if all_sections:
                relevant_sections = workspace_analyzer.select_relevant_content(
                    all_sections, requirements, workspace_info, max_sections=3
                )
                return relevant_sections

            return []

        except Exception as e:
            print(f"Warning: Failed to extract and score sections: {e}")
            return []

    def _intelligent_truncation(self, sections: list, max_tokens: int) -> str:
        """智能截断策略，保留最重要的信息"""
        if not sections:
            return ""

        # 估算 token 数量 (粗略估算: 1 token ≈ 4 字符)
        current_tokens = 0
        selected_content = []

        for section in sections:
            section_text = f"### {section.title}\n{section.content}"
            section_tokens = len(section_text) // 4

            if current_tokens + section_tokens <= max_tokens:
                selected_content.append(section_text)
                current_tokens += section_tokens
            else:
                # 尝试截断当前段落以适应 token 限制
                remaining_tokens = max_tokens - current_tokens
                if remaining_tokens > 50:  # 至少保留50个token
                    remaining_chars = remaining_tokens * 4
                    truncated_content = section.content[:remaining_chars-50] + "..."
                    selected_content.append(f"### {section.title}\n{truncated_content}")
                break

        return "\n\n".join(selected_content)

    def _truncate_skills_context(self, context: str, max_tokens: int) -> str:
        """截断 Skills 上下文"""
        max_chars = max_tokens * 4  # 粗略估算
        if len(context) <= max_chars:
            return context

        # 尝试在段落边界截断
        truncate_pos = context.rfind('\n\n', 0, max_chars)
        if truncate_pos == -1:
            truncate_pos = context.rfind('\n', 0, max_chars)
        if truncate_pos == -1:
            truncate_pos = max_chars

        return context[:truncate_pos] + "\n\n[内容已截断...]"

    def _deduplicate_and_optimize(self, content_parts: list) -> str:
        """去重和优化内容"""
        if not content_parts:
            return ""

        # 简单的去重：移除重复的段落
        seen_titles = set()
        unique_parts = []

        for part in content_parts:
            # 提取标题进行去重检查
            lines = part.split('\n')
            title_line = lines[0] if lines else ""

            if title_line not in seen_titles:
                seen_titles.add(title_line)
                unique_parts.append(part)

        # 确保上下文连贯性
        final_content = "\n\n".join(unique_parts)

        # 添加必要的连接词
        if len(unique_parts) > 1:
            final_content = "基于以下工作区信息和技术规范：\n\n" + final_content

        return final_content


def _parse_json(text: str) -> dict[str, Any]:
    start = text.find("{")
    if start == -1:
        raise ValueError("LLM response did not contain JSON")
    payload = text[start:]
    decoder = json.JSONDecoder()
    data, _ = decoder.raw_decode(payload)
    if not isinstance(data, dict):
        raise ValueError("LLM response JSON was not an object")
    return data


def _normalize_architecture_overview(value: Any) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    try:
        return json.dumps(value, ensure_ascii=False)
    except TypeError:
        return str(value)

agent_swarm = AgentSwarm()
