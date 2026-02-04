"""
工作区分析器 - 分析目标工作区的技术栈、项目规范和开发指南
"""
import json
import os
import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class RequirementType(Enum):
    """需求类型枚举"""
    FRONTEND_COMPONENT = "frontend_component"
    BACKEND_API = "backend_api"
    ARCHITECTURE_DESIGN = "architecture_design"
    CONFIGURATION_SETUP = "configuration_setup"
    TESTING_IMPLEMENTATION = "testing_implementation"
    UNKNOWN = "unknown"


@dataclass
class ContentSection:
    """文档内容段落"""
    title: str
    content: str
    level: int  # 标题级别 (1=##, 2=###, 3=####)
    section_type: str  # 段落类型
    relevance_score: float = 0.0


@dataclass
class TechStackInfo:
    """技术栈信息"""
    framework: str
    version: str
    ui_library: Optional[str] = None
    build_tools: List[str] = None
    dependencies: List[str] = None


@dataclass
class Guideline:
    """开发指南"""
    category: str
    title: str
    content: str
    code_examples: List[str] = None
    priority: str = "medium"  # high, medium, low


class WorkspaceAnalyzer:
    """工作区分析器"""

    def __init__(self):
        # 预定义的段落模式，支持中英文和同义词
        self.section_patterns = {
            "tech_stack": [
                r"(?i)##?\s*(?:技术栈|technology\s+stack|tech\s+stack|key\s+technologies)",
                r"(?i)##?\s*(?:技术选型|technology\s+selection|tech\s+choices)",
                r"(?i)##?\s*(?:核心技术|core\s+technologies)"
            ],
            "development_guidelines": [
                r"(?i)##?\s*(?:开发指南|development\s+guidelines?|coding\s+guidelines?)",
                r"(?i)##?\s*(?:代码规范|code\s+style|coding\s+standards?)",
                r"(?i)##?\s*(?:最佳实践|best\s+practices?)",
                r"(?i)##?\s*(?:开发规范|development\s+standards?)"
            ],
            "architecture": [
                r"(?i)##?\s*(?:架构|architecture)",
                r"(?i)##?\s*(?:系统架构|system\s+architecture)",
                r"(?i)##?\s*(?:项目架构|project\s+architecture)",
                r"(?i)##?\s*(?:核心架构|core\s+architecture)"
            ],
            "project_overview": [
                r"(?i)##?\s*(?:项目概述|project\s+overview)",
                r"(?i)##?\s*(?:项目介绍|project\s+introduction)",
                r"(?i)##?\s*(?:概述|overview)"
            ],
            "configuration": [
                r"(?i)##?\s*(?:配置|configuration|config)",
                r"(?i)##?\s*(?:环境配置|environment\s+setup)",
                r"(?i)##?\s*(?:开发环境|development\s+environment)",
                r"(?i)##?\s*(?:构建配置|build\s+configuration)"
            ],
            "commands": [
                r"(?i)##?\s*(?:命令|commands?)",
                r"(?i)##?\s*(?:构建命令|build\s+commands?)",
                r"(?i)##?\s*(?:开发命令|development\s+commands?)",
                r"(?i)##?\s*(?:脚本|scripts?)"
            ]
        }

    def analyze_workspace(self, workspace_path: str) -> Dict[str, Any]:
        """全面分析目标工作区的技术栈、项目规范和开发指南"""
        if not workspace_path or not os.path.exists(workspace_path):
            logger.warning(f"Workspace path does not exist: {workspace_path}")
            return self._get_default_workspace_info()

        workspace_info = {
            "tech_stack": "unknown",
            "framework": "unknown",
            "project_name": "unknown",
            "version": "1.0.0",
            "dependencies": {},
            "project_context": "",
            "development_guidelines": "",
            "architecture_info": "",
            "project_structure": {}
        }

        try:
            # 1. 分析 package.json - 技术栈识别
            package_json_path = os.path.join(workspace_path, "package.json")
            if os.path.exists(package_json_path):
                package_info = self._analyze_package_json(package_json_path)
                workspace_info.update(package_info)

            # 2. 分析 AGENTS.md - 开发指南和产品目标
            agents_md_path = os.path.join(workspace_path, "AGENTS.md")
            if os.path.exists(agents_md_path):
                workspace_info["development_guidelines"] = self._extract_agents_info(agents_md_path)

            # 3. 分析 CLAUDE.md - 项目架构和开发规范
            claude_md_path = os.path.join(workspace_path, "CLAUDE.md")
            if os.path.exists(claude_md_path):
                workspace_info["architecture_info"] = self._extract_claude_info(claude_md_path)

            # 4. 分析项目结构
            workspace_info["project_structure"] = self._analyze_project_structure(workspace_path)

            # 5. 构建项目上下文摘要
            workspace_info["project_context"] = self._build_project_context(workspace_info)

            logger.info(f"Workspace analyzed successfully: {workspace_info['project_name']} ({workspace_info['tech_stack']})")
            return workspace_info

        except Exception as e:
            logger.error(f"Failed to analyze workspace {workspace_path}: {e}")
            return self._get_default_workspace_info()

    def _analyze_package_json(self, package_json_path: str) -> Dict[str, Any]:
        """分析 package.json 获取技术栈信息"""
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)

            dependencies = {
                **package_data.get("dependencies", {}),
                **package_data.get("devDependencies", {})
            }

            # 技术栈识别
            tech_info = {
                "project_name": package_data.get("name", "unknown"),
                "version": package_data.get("version", "1.0.0"),
                "dependencies": dependencies,
                "project_type": "unknown"  # 新增项目类型识别
            }

            # Vue.js 项目识别
            if any(dep in dependencies for dep in ["vue", "vue-echarts", "@vue/cli"]):
                tech_info.update({
                    "tech_stack": "vue3",
                    "framework": "spark" if "spark" in dependencies else "vue",
                    "project_type": "frontend"  # 明确标识为前端项目
                })

                # 检查是否使用 WinDesign UI 组件库
                if any("winex" in dep or "winning" in dep for dep in dependencies):
                    tech_info["ui_library"] = "windesign"

            # React 项目识别
            elif "react" in dependencies:
                tech_info.update({
                    "tech_stack": "react",
                    "framework": "next" if "next" in dependencies else "react",
                    "project_type": "frontend"
                })
            # SolidJS 项目识别
            elif "solid-js" in dependencies:
                tech_info.update({
                    "tech_stack": "solidjs",
                    "framework": "solidjs",
                    "project_type": "frontend"
                })
            # Angular 项目识别
            elif "@angular/core" in dependencies:
                tech_info.update({
                    "tech_stack": "angular",
                    "framework": "angular",
                    "project_type": "frontend"
                })
            # Node.js 后端项目识别
            elif any(dep in dependencies for dep in ["express", "fastapi", "koa", "nest"]):
                tech_info.update({
                    "tech_stack": "nodejs",
                    "framework": "express" if "express" in dependencies else "unknown",
                    "project_type": "backend"
                })
            else:
                tech_info.update({
                    "tech_stack": "unknown",
                    "framework": "unknown",
                    "project_type": "unknown"
                })

            return tech_info

        except Exception as e:
            logger.warning(f"Failed to analyze package.json: {e}")
            return {"tech_stack": "unknown", "framework": "unknown", "project_type": "unknown"}

    def _extract_agents_info(self, agents_md_path: str) -> str:
        """提取 AGENTS.md 中的开发指南和产品目标"""
        try:
            with open(agents_md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 使用增强的段落提取
            all_sections = []

            # 提取开发指南相关段落
            dev_sections = self._extract_section_enhanced(content, self.section_patterns["development_guidelines"])
            all_sections.extend(dev_sections)

            # 提取配置和命令相关段落
            config_sections = self._extract_section_enhanced(content, self.section_patterns["configuration"])
            all_sections.extend(config_sections)

            command_sections = self._extract_section_enhanced(content, self.section_patterns["commands"])
            all_sections.extend(command_sections)

            # 如果没有找到特定段落，提取项目概述
            if not all_sections:
                overview_sections = self._extract_section_enhanced(content, self.section_patterns["project_overview"])
                all_sections.extend(overview_sections)

            # 如果仍然没有内容，返回前600字符作为概要
            if not all_sections:
                return content[:600] + "..." if len(content) > 600 else content

            # 按重要性排序并组合
            return self._combine_sections(all_sections, max_length=1000)

        except Exception as e:
            logger.warning(f"Failed to extract AGENTS.md info: {e}")
            return ""

    def _extract_claude_info(self, claude_md_path: str) -> str:
        """提取 CLAUDE.md 中的项目架构和开发规范"""
        try:
            with open(claude_md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 使用增强的段落提取
            all_sections = []

            # 提取项目概述
            overview_sections = self._extract_section_enhanced(content, self.section_patterns["project_overview"])
            all_sections.extend(overview_sections)

            # 提取技术栈信息
            tech_sections = self._extract_section_enhanced(content, self.section_patterns["tech_stack"])
            all_sections.extend(tech_sections)

            # 提取架构信息
            arch_sections = self._extract_section_enhanced(content, self.section_patterns["architecture"])
            all_sections.extend(arch_sections)

            # 提取开发规范
            dev_sections = self._extract_section_enhanced(content, self.section_patterns["development_guidelines"])
            all_sections.extend(dev_sections)

            # 如果没有找到特定段落，返回前600字符作为概要
            if not all_sections:
                return content[:600] + "..." if len(content) > 600 else content

            # 按重要性排序并组合
            return self._combine_sections(all_sections, max_length=1200)

        except Exception as e:
            logger.warning(f"Failed to extract CLAUDE.md info: {e}")
            return ""

    def _combine_sections(self, sections: List[ContentSection], max_length: int = 1000) -> str:
        """组合段落，按重要性排序"""
        if not sections:
            return ""

        # 按段落类型和级别排序（重要性优先）
        section_priority = {
            "tech_stack": 1,
            "project_overview": 2,
            "architecture": 3,
            "development_guidelines": 4,
            "configuration": 5,
            "commands": 6,
            "general": 7
        }

        sections.sort(key=lambda s: (section_priority.get(s.section_type, 10), s.level))

        # 组合内容
        combined_parts = []
        current_length = 0

        for section in sections:
            section_text = f"## {section.title}\n{section.content}"

            if current_length + len(section_text) <= max_length:
                combined_parts.append(section_text)
                current_length += len(section_text)
            else:
                # 尝试截断当前段落以适应长度限制
                remaining_length = max_length - current_length
                if remaining_length > 100:  # 至少保留100字符
                    truncated_content = section.content[:remaining_length-50] + "..."
                    combined_parts.append(f"## {section.title}\n{truncated_content}")
                break

        return "\n\n".join(combined_parts)

    def _extract_section_enhanced(self, content: str, section_patterns: List[str]) -> List[ContentSection]:
        """增强的段落提取，支持多种匹配模式和内容清理"""
        sections = []

        for pattern in section_patterns:
            try:
                # 查找所有匹配的标题
                matches = list(re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE))

                for match in matches:
                    # 提取标题
                    title_start = match.start()
                    title_end = content.find('\n', title_start)
                    if title_end == -1:
                        title_end = len(content)

                    title = content[title_start:title_end].strip()

                    # 确定标题级别
                    level = len(re.match(r'^#+', title.lstrip()).group()) if re.match(r'^#+', title.lstrip()) else 2

                    # 提取内容
                    content_start = title_end + 1
                    section_content = self._extract_section_content(content, content_start, level)

                    if section_content.strip():
                        # 清理和验证内容
                        cleaned_content = self._clean_content(section_content)

                        # 确定段落类型
                        section_type = self._determine_section_type(title, cleaned_content)

                        sections.append(ContentSection(
                            title=title.strip('#').strip(),
                            content=cleaned_content,
                            level=level,
                            section_type=section_type
                        ))

            except Exception as e:
                logger.warning(f"Failed to extract section with pattern {pattern}: {e}")
                continue

        return sections

    def _extract_section_content(self, content: str, start_pos: int, current_level: int) -> str:
        """提取段落内容，准确识别段落边界"""
        if start_pos >= len(content):
            return ""

        # 查找下一个同级或更高级标题
        remaining_content = content[start_pos:]

        # 构建结束模式：同级或更高级标题
        end_patterns = []
        for i in range(1, current_level + 1):
            end_patterns.append(f"^{'#' * i}\\s+")

        end_pattern = '|'.join(end_patterns)

        # 查找段落结束位置
        end_match = re.search(end_pattern, remaining_content, re.MULTILINE)

        if end_match:
            section_content = remaining_content[:end_match.start()]
        else:
            section_content = remaining_content

        return section_content.strip()

    def _clean_content(self, content: str) -> str:
        """清理和验证内容"""
        if not content:
            return ""

        # 移除多余的空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

        # 保护代码块
        code_blocks = []
        def preserve_code_block(match):
            code_blocks.append(match.group(0))
            return f"__CODE_BLOCK_{len(code_blocks) - 1}__"

        # 提取并保护代码块
        content = re.sub(r'```[\s\S]*?```', preserve_code_block, content)
        content = re.sub(r'`[^`\n]+`', preserve_code_block, content)

        # 清理格式符号（但保护代码块）
        content = re.sub(r'^\s*[-*+]\s*', '• ', content, flags=re.MULTILINE)  # 统一列表符号
        content = re.sub(r'^\s*\d+\.\s*', lambda m: f"{m.group().strip()} ", content, flags=re.MULTILINE)  # 保持编号列表

        # 恢复代码块
        for i, code_block in enumerate(code_blocks):
            content = content.replace(f"__CODE_BLOCK_{i}__", code_block)

        # 限制长度但保护重要内容
        if len(content) > 1200:  # 增加长度限制
            # 尝试在句号或段落边界截断
            truncate_pos = content.rfind('.', 0, 1200)
            if truncate_pos == -1:
                truncate_pos = content.rfind('\n', 0, 1200)
            if truncate_pos == -1:
                truncate_pos = 1200

            content = content[:truncate_pos] + "..."

        return content.strip()

    def _determine_section_type(self, title: str, content: str) -> str:
        """确定段落类型"""
        title_lower = title.lower()
        content_lower = content.lower()

        # 技术栈相关
        if any(keyword in title_lower for keyword in ['技术栈', 'technology', 'tech', 'stack']):
            return "tech_stack"

        # 开发指南相关
        if any(keyword in title_lower for keyword in ['指南', 'guidelines', '规范', 'standards', '最佳实践', 'best practices']):
            return "development_guidelines"

        # 架构相关
        if any(keyword in title_lower for keyword in ['架构', 'architecture']):
            return "architecture"

        # 配置相关
        if any(keyword in title_lower for keyword in ['配置', 'configuration', 'config', '环境', 'environment']):
            return "configuration"

        # 命令相关
        if any(keyword in title_lower for keyword in ['命令', 'commands', '脚本', 'scripts']):
            return "commands"

        # 根据内容判断
        if '```' in content or 'npm run' in content_lower or 'yarn' in content_lower:
            return "commands"

        if any(keyword in content_lower for keyword in ['component', '组件', 'props', 'state']):
            return "development_guidelines"

        return "general"

    def _analyze_project_structure(self, workspace_path: str) -> Dict[str, Any]:
        """分析项目结构"""
        try:
            structure = {
                "has_src": os.path.exists(os.path.join(workspace_path, "src")),
                "has_components": False,
                "has_pages": False,
                "has_api": False,
                "has_tests": False,
                "config_files": []
            }

            # 检查常见目录
            src_path = os.path.join(workspace_path, "src")
            if structure["has_src"]:
                structure["has_components"] = os.path.exists(os.path.join(src_path, "components"))
                structure["has_pages"] = os.path.exists(os.path.join(src_path, "pages"))
                structure["has_api"] = os.path.exists(os.path.join(src_path, "api"))

            # 检查测试目录
            structure["has_tests"] = any(os.path.exists(os.path.join(workspace_path, test_dir))
                                       for test_dir in ["test", "tests", "__tests__", "spec"])

            # 检查配置文件
            config_files = [
                "vite.config.js", "vite.config.ts",
                "webpack.config.js", "vue.config.js",
                "tailwind.config.js", "tailwind.config.ts",
                "tsconfig.json", "jsconfig.json"
            ]

            for config_file in config_files:
                if os.path.exists(os.path.join(workspace_path, config_file)):
                    structure["config_files"].append(config_file)

            return structure

        except Exception as e:
            logger.warning(f"Failed to analyze project structure: {e}")
            return {}

    def _build_project_context(self, workspace_info: Dict[str, Any]) -> str:
        """构建项目上下文摘要"""
        context_parts = []

        # 基本信息
        context_parts.append(f"项目: {workspace_info['project_name']}")
        context_parts.append(f"技术栈: {workspace_info['tech_stack']} + {workspace_info['framework']}")

        # 开发指南摘要
        if workspace_info.get("development_guidelines"):
            guidelines_summary = workspace_info["development_guidelines"][:200] + "..." if len(workspace_info["development_guidelines"]) > 200 else workspace_info["development_guidelines"]
            context_parts.append(f"开发指南: {guidelines_summary}")

        # 架构信息摘要
        if workspace_info.get("architecture_info"):
            arch_summary = workspace_info["architecture_info"][:200] + "..." if len(workspace_info["architecture_info"]) > 200 else workspace_info["architecture_info"]
            context_parts.append(f"架构信息: {arch_summary}")

        return "\n".join(context_parts)

    def classify_requirement_type(self, requirement) -> RequirementType:
        """
        分析需求内容，分类为不同的需求类型

        Args:
            requirement: Requirement 对象，包含 summary 和 description

        Returns:
            RequirementType: 需求类型枚举
        """
        try:
            # 合并需求描述进行分析
            content = f"{requirement.summary} {requirement.description}".lower()

            # 前端组件开发关键词
            frontend_keywords = [
                '前端', 'frontend', 'ui', '界面', '组件', 'component',
                '页面', 'page', '视图', 'view', '表单', 'form',
                '按钮', 'button', '输入框', 'input', '下拉框', 'select',
                '计算器', 'calculator', '图表', 'chart', '弹窗', 'modal',
                'vue', 'react', 'angular', 'solidjs'
            ]

            # 后端API开发关键词
            backend_keywords = [
                '后端', 'backend', 'api', '接口', 'endpoint',
                '服务', 'service', '数据库', 'database', 'sql',
                '认证', 'auth', '登录', 'login', '权限', 'permission',
                'express', 'fastapi', 'spring', 'django'
            ]

            # 架构设计关键词
            architecture_keywords = [
                '架构', 'architecture', '设计', 'design', '系统',
                '微服务', 'microservice', '模块', 'module', '框架', 'framework',
                '重构', 'refactor', '优化', 'optimize', '性能', 'performance'
            ]

            # 配置设置关键词
            configuration_keywords = [
                '配置', 'config', '环境', 'environment', '部署', 'deploy',
                '构建', 'build', '打包', 'bundle', '安装', 'install',
                'docker', 'nginx', 'webpack', 'vite'
            ]

            # 测试实现关键词
            testing_keywords = [
                '测试', 'test', '单元测试', 'unit test', '集成测试', 'integration',
                '自动化', 'automation', '覆盖率', 'coverage', 'jest', 'vitest'
            ]

            # 计算各类型的匹配分数
            scores = {
                RequirementType.FRONTEND_COMPONENT: self._calculate_keyword_score(content, frontend_keywords),
                RequirementType.BACKEND_API: self._calculate_keyword_score(content, backend_keywords),
                RequirementType.ARCHITECTURE_DESIGN: self._calculate_keyword_score(content, architecture_keywords),
                RequirementType.CONFIGURATION_SETUP: self._calculate_keyword_score(content, configuration_keywords),
                RequirementType.TESTING_IMPLEMENTATION: self._calculate_keyword_score(content, testing_keywords)
            }

            # 找到最高分的类型
            max_score = max(scores.values())
            if max_score > 0:
                for req_type, score in scores.items():
                    if score == max_score:
                        logger.info(f"Classified requirement as {req_type.value} with score {score}")
                        return req_type

            # 如果没有明确匹配，返回未知类型
            logger.info("Could not classify requirement type, returning UNKNOWN")
            return RequirementType.UNKNOWN

        except Exception as e:
            logger.error(f"Failed to classify requirement type: {e}")
            return RequirementType.UNKNOWN

    def _calculate_keyword_score(self, content: str, keywords: List[str]) -> float:
        """计算关键词匹配分数"""
        score = 0.0
        content_words = content.split()

        for keyword in keywords:
            if keyword in content:
                # 完整匹配得更高分
                if keyword in content_words:
                    score += 2.0
                else:
                    score += 1.0

        # 归一化分数
        return score / len(keywords) if keywords else 0.0

    def score_content_relevance(self, content_section: str, requirement, workspace_info: Dict[str, Any] = None) -> float:
        """
        基于多个因素评分内容相关性

        Args:
            content_section: 文档段落内容
            requirement: 需求对象
            workspace_info: 工作区信息

        Returns:
            float: 相关性分数 (0.0 - 1.0)
        """
        try:
            if not content_section or not requirement:
                return 0.0

            # 合并需求内容
            req_content = f"{requirement.summary} {requirement.description}".lower()
            section_content = content_section.lower()

            # 1. 关键词匹配度 (40%)
            keyword_score = self._calculate_keyword_relevance(req_content, section_content)

            # 2. 技术栈相关性 (30%)
            tech_score = self._calculate_tech_relevance(req_content, section_content, workspace_info)

            # 3. 内容类型匹配 (20%)
            type_score = self._calculate_type_relevance(requirement, section_content)

            # 4. 内容新鲜度 (10%) - 基于内容长度和结构化程度
            freshness_score = self._calculate_freshness_score(section_content)

            # 加权计算总分
            total_score = (
                keyword_score * 0.4 +
                tech_score * 0.3 +
                type_score * 0.2 +
                freshness_score * 0.1
            )

            return min(1.0, max(0.0, total_score))

        except Exception as e:
            logger.error(f"Failed to score content relevance: {e}")
            return 0.0

    def _calculate_keyword_relevance(self, req_content: str, section_content: str) -> float:
        """计算关键词匹配相关性"""
        req_words = set(req_content.split())
        section_words = set(section_content.split())

        # 计算交集
        common_words = req_words.intersection(section_words)

        if not req_words:
            return 0.0

        # 基础匹配分数
        basic_score = len(common_words) / len(req_words)

        # 重要关键词加权
        important_keywords = [
            'vue', 'react', 'angular', 'solidjs', 'component', '组件',
            'api', 'backend', 'frontend', 'database', 'config', '配置'
        ]

        important_matches = sum(1 for word in common_words if word in important_keywords)
        importance_bonus = important_matches * 0.1

        return min(1.0, basic_score + importance_bonus)

    def _calculate_tech_relevance(self, req_content: str, section_content: str, workspace_info: Dict[str, Any] = None) -> float:
        """计算技术栈相关性"""
        if not workspace_info:
            return 0.0

        tech_stack = workspace_info.get('tech_stack', '').lower()
        framework = workspace_info.get('framework', '').lower()
        project_type = workspace_info.get('project_type', '').lower()

        score = 0.0

        # 技术栈匹配
        if tech_stack and tech_stack in section_content:
            score += 0.4

        # 框架匹配
        if framework and framework in section_content:
            score += 0.3

        # 项目类型匹配
        if project_type and project_type in section_content:
            score += 0.2

        # 需求中提到的技术栈
        if tech_stack and tech_stack in req_content:
            score += 0.1

        return min(1.0, score)

    def _calculate_type_relevance(self, requirement, section_content: str) -> float:
        """计算内容类型匹配度"""
        req_type = self.classify_requirement_type(requirement)

        type_indicators = {
            RequirementType.FRONTEND_COMPONENT: ['component', '组件', 'vue', 'react', 'ui', 'interface'],
            RequirementType.BACKEND_API: ['api', 'endpoint', 'service', 'database', 'server'],
            RequirementType.ARCHITECTURE_DESIGN: ['architecture', '架构', 'design', 'pattern', 'structure'],
            RequirementType.CONFIGURATION_SETUP: ['config', '配置', 'setup', 'environment', 'build'],
            RequirementType.TESTING_IMPLEMENTATION: ['test', '测试', 'spec', 'coverage', 'automation']
        }

        if req_type in type_indicators:
            indicators = type_indicators[req_type]
            matches = sum(1 for indicator in indicators if indicator in section_content)
            return matches / len(indicators) if indicators else 0.0

        return 0.0

    def _calculate_freshness_score(self, section_content: str) -> float:
        """计算内容新鲜度分数"""
        score = 0.0

        # 内容长度适中得分更高
        length = len(section_content)
        if 100 <= length <= 800:
            score += 0.4
        elif 50 <= length < 100 or 800 < length <= 1200:
            score += 0.2

        # 包含代码示例
        if '```' in section_content or '`' in section_content:
            score += 0.3

        # 结构化内容（列表、标题等）
        if any(marker in section_content for marker in ['•', '-', '*', '1.', '2.']):
            score += 0.2

        # 包含具体配置或命令
        if any(cmd in section_content for cmd in ['npm', 'yarn', 'pnpm', 'git', 'docker']):
            score += 0.1

        return min(1.0, score)

    def select_relevant_content(self, all_sections: List[ContentSection], requirement, workspace_info: Dict[str, Any] = None, max_sections: int = 5) -> List[ContentSection]:
        """
        根据需求选择最相关的内容段落

        Args:
            all_sections: 所有提取的段落
            requirement: 需求对象
            workspace_info: 工作区信息
            max_sections: 最大返回段落数

        Returns:
            List[ContentSection]: 按相关性排序的段落列表
        """
        try:
            # 为每个段落计算相关性分数
            for section in all_sections:
                section.relevance_score = self.score_content_relevance(
                    section.content, requirement, workspace_info
                )

            # 按相关性分数排序
            sorted_sections = sorted(all_sections, key=lambda s: s.relevance_score, reverse=True)

            # 返回前 max_sections 个最相关的段落
            relevant_sections = sorted_sections[:max_sections]

            logger.info(f"Selected {len(relevant_sections)} relevant sections from {len(all_sections)} total sections")
            for i, section in enumerate(relevant_sections):
                logger.debug(f"Section {i+1}: {section.title} (score: {section.relevance_score:.2f})")

            return relevant_sections

        except Exception as e:
            logger.error(f"Failed to select relevant content: {e}")
            return all_sections[:max_sections]  # 降级处理

    def _get_default_workspace_info(self) -> Dict[str, Any]:
        """获取默认的工作区信息"""
        return {
            "tech_stack": "unknown",
            "framework": "unknown",
            "project_name": "unknown",
            "version": "1.0.0",
            "dependencies": {},
            "project_context": "无法分析工作区信息",
            "development_guidelines": "",
            "architecture_info": "",
            "project_structure": {}
        }


# 全局实例
workspace_analyzer = WorkspaceAnalyzer()