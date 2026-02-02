"""
OpenSpec 生命周期管理模块

状态流转：
- draft（草稿）：AI 生成后的初始状态，可随意修改
- review（审批中）：研发提交审批，等待审批人确认
- approved（已审批）：审批通过，自动生成版本号
- archived（已归档）：开发完成后归档
"""

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from pydantic import BaseModel

from .spec_versioning import SpecVersion


class SpecStatus(str, Enum):
    """OpenSpec 状态枚举"""
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    ARCHIVED = "archived"


class StatusTransition(BaseModel):
    """状态转换记录"""
    from_status: str
    to_status: str
    operator: str
    timestamp: str
    reason: str = ""


class SpecLifecycle:
    """OpenSpec 生命周期管理器"""

    def __init__(self, base_path: str = ".openwork/specs"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.version_manager = SpecVersion(base_path)

        # 定义状态转换规则
        self.transition_rules = {
            SpecStatus.DRAFT: [SpecStatus.REVIEW],
            SpecStatus.REVIEW: [SpecStatus.APPROVED, SpecStatus.DRAFT],
            SpecStatus.APPROVED: [SpecStatus.ARCHIVED, SpecStatus.DRAFT],
            SpecStatus.ARCHIVED: []
        }

        # 状态变更通知回调
        self.notification_callbacks: List[Callable] = []

    def _get_spec_dir(self, requirement_id: str) -> Path:
        """获取 OpenSpec 存储目录"""
        spec_dir = self.base_path / requirement_id
        spec_dir.mkdir(parents=True, exist_ok=True)
        return spec_dir

    def _get_lifecycle_file(self, requirement_id: str) -> Path:
        """获取生命周期文件路径"""
        return self._get_spec_dir(requirement_id) / "lifecycle.json"

    def _load_lifecycle(self, requirement_id: str) -> Dict[str, Any]:
        """加载生命周期数据"""
        lifecycle_file = self._get_lifecycle_file(requirement_id)
        if lifecycle_file.exists():
            with open(lifecycle_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        # 默认生命周期数据
        return {
            "requirement_id": requirement_id,
            "current_status": SpecStatus.DRAFT.value,
            "history": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

    def _save_lifecycle(self, requirement_id: str, lifecycle: Dict[str, Any]):
        """保存生命周期数据"""
        lifecycle["updated_at"] = datetime.now().isoformat()
        lifecycle_file = self._get_lifecycle_file(requirement_id)
        with open(lifecycle_file, 'w', encoding='utf-8') as f:
            json.dump(lifecycle, f, indent=2, ensure_ascii=False)

    def get_status(self, requirement_id: str) -> SpecStatus:
        """
        获取当前状态

        Args:
            requirement_id: 需求ID

        Returns:
            当前状态
        """
        lifecycle = self._load_lifecycle(requirement_id)
        return SpecStatus(lifecycle["current_status"])

    def can_transition(self, requirement_id: str, to_status: SpecStatus) -> bool:
        """
        检查是否可以转换到目标状态

        Args:
            requirement_id: 需求ID
            to_status: 目标状态

        Returns:
            是否可以转换
        """
        current_status = self.get_status(requirement_id)
        allowed_statuses = self.transition_rules.get(current_status, [])
        return to_status in allowed_statuses

    def transition_to(
        self,
        requirement_id: str,
        to_status: SpecStatus,
        operator: str,
        reason: str = "",
        spec_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        转换到目标状态

        Args:
            requirement_id: 需求ID
            to_status: 目标状态
            operator: 操作人
            reason: 转换原因
            spec_data: OpenSpec 数据（审批通过时需要）

        Returns:
            是否成功
        """
        current_status = self.get_status(requirement_id)

        # 检查是否可以转换
        if not self.can_transition(requirement_id, to_status):
            return False

        # 记录状态转换
        lifecycle = self._load_lifecycle(requirement_id)
        transition = StatusTransition(
            from_status=current_status.value,
            to_status=to_status.value,
            operator=operator,
            timestamp=datetime.now().isoformat(),
            reason=reason
        )
        lifecycle["history"].append(transition.dict())
        lifecycle["current_status"] = to_status.value

        # 如果转换到 approved 状态，生成版本
        if to_status == SpecStatus.APPROVED and spec_data:
            version = self.version_manager.create_version(
                requirement_id=requirement_id,
                spec_data=spec_data,
                approver=operator,
                change_summary=reason or "Approved"
            )
            lifecycle["current_version"] = version

        self._save_lifecycle(requirement_id, lifecycle)

        # 发送通知
        self._notify_status_change(requirement_id, current_status, to_status, operator)

        return True

    def submit_for_review(
        self,
        requirement_id: str,
        submitter: str,
        reason: str = ""
    ) -> bool:
        """
        提交审批

        Args:
            requirement_id: 需求ID
            submitter: 提交人
            reason: 提交原因

        Returns:
            是否成功
        """
        return self.transition_to(
            requirement_id=requirement_id,
            to_status=SpecStatus.REVIEW,
            operator=submitter,
            reason=reason or "Submit for review"
        )

    def approve(
        self,
        requirement_id: str,
        approver: str,
        spec_data: Dict[str, Any],
        reason: str = ""
    ) -> bool:
        """
        审批通过

        Args:
            requirement_id: 需求ID
            approver: 审批人
            spec_data: OpenSpec 数据
            reason: 审批意见

        Returns:
            是否成功
        """
        return self.transition_to(
            requirement_id=requirement_id,
            to_status=SpecStatus.APPROVED,
            operator=approver,
            reason=reason or "Approved",
            spec_data=spec_data
        )

    def reject(
        self,
        requirement_id: str,
        approver: str,
        reason: str
    ) -> bool:
        """
        审批退回

        Args:
            requirement_id: 需求ID
            approver: 审批人
            reason: 退回原因

        Returns:
            是否成功
        """
        return self.transition_to(
            requirement_id=requirement_id,
            to_status=SpecStatus.DRAFT,
            operator=approver,
            reason=reason
        )

    def archive(
        self,
        requirement_id: str,
        operator: str,
        reason: str = ""
    ) -> bool:
        """
        归档

        Args:
            requirement_id: 需求ID
            operator: 操作人
            reason: 归档原因

        Returns:
            是否成功
        """
        success = self.transition_to(
            requirement_id=requirement_id,
            to_status=SpecStatus.ARCHIVED,
            operator=operator,
            reason=reason or "Development completed"
        )

        if success:
            # 归档当前版本
            lifecycle = self._load_lifecycle(requirement_id)
            current_version = lifecycle.get("current_version")
            if current_version:
                self.version_manager.archive_version(requirement_id, current_version)

        return success

    def get_history(self, requirement_id: str) -> List[StatusTransition]:
        """
        获取状态变更历史

        Args:
            requirement_id: 需求ID

        Returns:
            状态变更历史列表
        """
        lifecycle = self._load_lifecycle(requirement_id)
        return [StatusTransition(**h) for h in lifecycle.get("history", [])]

    def register_notification_callback(self, callback: Callable):
        """
        注册状态变更通知回调

        Args:
            callback: 回调函数，签名为 (requirement_id, from_status, to_status, operator)
        """
        self.notification_callbacks.append(callback)

    def _notify_status_change(
        self,
        requirement_id: str,
        from_status: SpecStatus,
        to_status: SpecStatus,
        operator: str
    ):
        """
        发送状态变更通知

        Args:
            requirement_id: 需求ID
            from_status: 原状态
            to_status: 新状态
            operator: 操作人
        """
        for callback in self.notification_callbacks:
            try:
                callback(requirement_id, from_status, to_status, operator)
            except Exception as e:
                print(f"Notification callback error: {e}")

    def get_lifecycle_info(self, requirement_id: str) -> Dict[str, Any]:
        """
        获取完整的生命周期信息

        Args:
            requirement_id: 需求ID

        Returns:
            生命周期信息
        """
        lifecycle = self._load_lifecycle(requirement_id)
        versions = self.version_manager.list_versions(requirement_id)

        return {
            "requirement_id": requirement_id,
            "current_status": lifecycle["current_status"],
            "current_version": lifecycle.get("current_version"),
            "created_at": lifecycle["created_at"],
            "updated_at": lifecycle["updated_at"],
            "history": lifecycle["history"],
            "versions": [v.dict() for v in versions]
        }
