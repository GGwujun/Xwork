"""
OpenSpec 版本管理模块

版本策略：
- 审批前（draft/review 状态）：只保存 draft.json，不创建版本号
- 审批通过后（approved 状态）：生成 v1 版本，保存为 v1.json
- 后续修改：每次审批通过后创建新版本（v2, v3...）
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class VersionMetadata(BaseModel):
    """版本元数据"""
    version: int
    created_at: str
    approver: str
    approval_time: str
    change_summary: str
    status: str  # approved, archived


class SpecVersion:
    """OpenSpec 版本管理器"""

    def __init__(self, base_path: str = ".openwork/specs"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_spec_dir(self, requirement_id: str) -> Path:
        """获取 OpenSpec 存储目录"""
        spec_dir = self.base_path / requirement_id
        spec_dir.mkdir(parents=True, exist_ok=True)
        return spec_dir

    def _get_metadata_file(self, requirement_id: str) -> Path:
        """获取元数据文件路径"""
        return self._get_spec_dir(requirement_id) / "metadata.json"

    def _load_metadata(self, requirement_id: str) -> Dict[str, Any]:
        """加载元数据"""
        metadata_file = self._get_metadata_file(requirement_id)
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "requirement_id": requirement_id,
            "versions": [],
            "current_version": None,
            "latest_version": 0
        }

    def _save_metadata(self, requirement_id: str, metadata: Dict[str, Any]):
        """保存元数据"""
        metadata_file = self._get_metadata_file(requirement_id)
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    def create_version(
        self,
        requirement_id: str,
        spec_data: Dict[str, Any],
        approver: str,
        change_summary: str = ""
    ) -> int:
        """
        创建新版本（审批通过后调用）

        Args:
            requirement_id: 需求ID
            spec_data: OpenSpec 数据
            approver: 审批人
            change_summary: 变更摘要

        Returns:
            版本号
        """
        spec_dir = self._get_spec_dir(requirement_id)
        metadata = self._load_metadata(requirement_id)

        # 生成新版本号
        new_version = metadata["latest_version"] + 1

        # 保存版本文件
        version_file = spec_dir / f"v{new_version}.json"
        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump(spec_data, f, indent=2, ensure_ascii=False)

        # 更新元数据
        now = datetime.now().isoformat()
        version_meta = VersionMetadata(
            version=new_version,
            created_at=now,
            approver=approver,
            approval_time=now,
            change_summary=change_summary or f"Version {new_version} approved",
            status="approved"
        )

        metadata["versions"].append(version_meta.dict())
        metadata["latest_version"] = new_version
        metadata["current_version"] = new_version

        self._save_metadata(requirement_id, metadata)

        return new_version

    def get_version(self, requirement_id: str, version: int) -> Optional[Dict[str, Any]]:
        """
        获取指定版本的 OpenSpec

        Args:
            requirement_id: 需求ID
            version: 版本号

        Returns:
            OpenSpec 数据，如果版本不存在则返回 None
        """
        spec_dir = self._get_spec_dir(requirement_id)
        version_file = spec_dir / f"v{version}.json"

        if not version_file.exists():
            return None

        with open(version_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_latest_version(self, requirement_id: str) -> Optional[Dict[str, Any]]:
        """
        获取最新版本的 OpenSpec

        Args:
            requirement_id: 需求ID

        Returns:
            OpenSpec 数据，如果没有版本则返回 None
        """
        metadata = self._load_metadata(requirement_id)
        latest_version = metadata.get("latest_version", 0)

        if latest_version == 0:
            return None

        return self.get_version(requirement_id, latest_version)

    def list_versions(self, requirement_id: str) -> List[VersionMetadata]:
        """
        列出所有版本

        Args:
            requirement_id: 需求ID

        Returns:
            版本元数据列表
        """
        metadata = self._load_metadata(requirement_id)
        return [VersionMetadata(**v) for v in metadata.get("versions", [])]

    def rollback_to_version(self, requirement_id: str, version: int) -> bool:
        """
        回滚到指定版本

        Args:
            requirement_id: 需求ID
            version: 目标版本号

        Returns:
            是否成功
        """
        spec_data = self.get_version(requirement_id, version)
        if spec_data is None:
            return False

        # 将指定版本复制为 draft.json
        spec_dir = self._get_spec_dir(requirement_id)
        draft_file = spec_dir / "draft.json"

        with open(draft_file, 'w', encoding='utf-8') as f:
            json.dump(spec_data, f, indent=2, ensure_ascii=False)

        # 更新元数据
        metadata = self._load_metadata(requirement_id)
        metadata["current_version"] = version
        self._save_metadata(requirement_id, metadata)

        return True

    def compare_versions(
        self,
        requirement_id: str,
        version1: int,
        version2: int
    ) -> Dict[str, Any]:
        """
        比较两个版本的差异

        Args:
            requirement_id: 需求ID
            version1: 版本1
            version2: 版本2

        Returns:
            差异信息
        """
        spec1 = self.get_version(requirement_id, version1)
        spec2 = self.get_version(requirement_id, version2)

        if spec1 is None or spec2 is None:
            return {"error": "Version not found"}

        # 简单的差异对比（可以使用更复杂的 diff 算法）
        diff = {
            "version1": version1,
            "version2": version2,
            "changes": []
        }

        # 对比主要字段
        for key in ["requirement", "design", "tasks"]:
            if spec1.get(key) != spec2.get(key):
                diff["changes"].append({
                    "field": key,
                    "changed": True
                })

        return diff

    def archive_version(self, requirement_id: str, version: int) -> bool:
        """
        归档指定版本

        Args:
            requirement_id: 需求ID
            version: 版本号

        Returns:
            是否成功
        """
        metadata = self._load_metadata(requirement_id)

        # 查找并更新版本状态
        for v in metadata["versions"]:
            if v["version"] == version:
                v["status"] = "archived"
                self._save_metadata(requirement_id, metadata)
                return True

        return False

    def get_version_history(self, requirement_id: str) -> List[Dict[str, Any]]:
        """
        获取版本历史

        Args:
            requirement_id: 需求ID

        Returns:
            版本历史列表
        """
        metadata = self._load_metadata(requirement_id)
        return metadata.get("versions", [])
