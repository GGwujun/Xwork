"""
OpenSpec 版本管理和生命周期管理的单元测试
"""

import pytest
import json
import shutil
from pathlib import Path
from app.spec_versioning import SpecVersion, VersionMetadata
from app.spec_lifecycle import SpecLifecycle, SpecStatus


@pytest.fixture
def test_base_path(tmp_path):
    """创建临时测试目录"""
    test_path = tmp_path / "test_specs"
    test_path.mkdir()
    yield str(test_path)
    # 清理
    if test_path.exists():
        shutil.rmtree(test_path)


@pytest.fixture
def spec_version(test_base_path):
    """创建 SpecVersion 实例"""
    return SpecVersion(base_path=test_base_path)


@pytest.fixture
def spec_lifecycle(test_base_path):
    """创建 SpecLifecycle 实例"""
    return SpecLifecycle(base_path=test_base_path)


@pytest.fixture
def sample_spec():
    """示例 OpenSpec 数据"""
    return {
        "spec_version": "0.2.0",
        "project_name": "Test Project",
        "requirement": {
            "summary": "Test requirement",
            "description": "Test description",
            "acceptance_criteria": ["Criterion 1", "Criterion 2"]
        },
        "tasks": [
            {
                "id": "task-1",
                "title": "Task 1",
                "description": "Description 1",
                "status": "pending"
            }
        ]
    }


class TestSpecVersioning:
    """测试 OpenSpec 版本管理"""

    def test_create_version(self, spec_version, sample_spec):
        """测试创建版本"""
        requirement_id = "REQ-001"
        version = spec_version.create_version(
            requirement_id=requirement_id,
            spec_data=sample_spec,
            approver="test_user",
            change_summary="Initial version"
        )

        assert version == 1

        # 验证版本文件存在
        version_file = Path(spec_version.base_path) / requirement_id / "v1.json"
        assert version_file.exists()

        # 验证版本内容
        loaded_spec = spec_version.get_version(requirement_id, 1)
        assert loaded_spec == sample_spec

    def test_create_multiple_versions(self, spec_version, sample_spec):
        """测试创建多个版本"""
        requirement_id = "REQ-002"

        # 创建第一个版本
        v1 = spec_version.create_version(
            requirement_id=requirement_id,
            spec_data=sample_spec,
            approver="user1",
            change_summary="Version 1"
        )
        assert v1 == 1

        # 修改 spec 并创建第二个版本
        modified_spec = sample_spec.copy()
        modified_spec["requirement"]["summary"] = "Modified requirement"

        v2 = spec_version.create_version(
            requirement_id=requirement_id,
            spec_data=modified_spec,
            approver="user2",
            change_summary="Version 2"
        )
        assert v2 == 2

        # 验证两个版本都存在
        spec_v1 = spec_version.get_version(requirement_id, 1)
        spec_v2 = spec_version.get_version(requirement_id, 2)

        assert spec_v1["requirement"]["summary"] == "Test requirement"
        assert spec_v2["requirement"]["summary"] == "Modified requirement"

    def test_get_latest_version(self, spec_version, sample_spec):
        """测试获取最新版本"""
        requirement_id = "REQ-003"

        # 没有版本时返回 None
        assert spec_version.get_latest_version(requirement_id) is None

        # 创建版本
        spec_version.create_version(
            requirement_id=requirement_id,
            spec_data=sample_spec,
            approver="user1"
        )

        # 获取最新版本
        latest = spec_version.get_latest_version(requirement_id)
        assert latest == sample_spec

    def test_list_versions(self, spec_version, sample_spec):
        """测试列出所有版本"""
        requirement_id = "REQ-004"

        # 创建多个版本
        for i in range(3):
            spec_version.create_version(
                requirement_id=requirement_id,
                spec_data=sample_spec,
                approver=f"user{i}",
                change_summary=f"Version {i+1}"
            )

        # 列出版本
        versions = spec_version.list_versions(requirement_id)
        assert len(versions) == 3
        assert all(isinstance(v, VersionMetadata) for v in versions)

    def test_rollback_to_version(self, spec_version, sample_spec):
        """测试回滚到指定版本"""
        requirement_id = "REQ-005"

        # 创建两个版本
        spec_version.create_version(
            requirement_id=requirement_id,
            spec_data=sample_spec,
            approver="user1"
        )

        modified_spec = sample_spec.copy()
        modified_spec["requirement"]["summary"] = "Modified"
        spec_version.create_version(
            requirement_id=requirement_id,
            spec_data=modified_spec,
            approver="user2"
        )

        # 回滚到版本 1
        success = spec_version.rollback_to_version(requirement_id, 1)
        assert success

        # 验证 draft.json 已更新
        spec_dir = Path(spec_version.base_path) / requirement_id
        draft_file = spec_dir / "draft.json"
        assert draft_file.exists()

        with open(draft_file, 'r', encoding='utf-8') as f:
            draft_spec = json.load(f)
        assert draft_spec["requirement"]["summary"] == "Test requirement"

    def test_compare_versions(self, spec_version, sample_spec):
        """测试版本比较"""
        requirement_id = "REQ-006"

        # 创建两个不同的版本
        spec_version.create_version(
            requirement_id=requirement_id,
            spec_data=sample_spec,
            approver="user1"
        )

        modified_spec = sample_spec.copy()
        modified_spec["requirement"]["summary"] = "Modified"
        spec_version.create_version(
            requirement_id=requirement_id,
            spec_data=modified_spec,
            approver="user2"
        )

        # 比较版本
        diff = spec_version.compare_versions(requirement_id, 1, 2)
        assert diff["version1"] == 1
        assert diff["version2"] == 2
        assert len(diff["changes"]) > 0


class TestSpecLifecycle:
    """测试 OpenSpec 生命周期管理"""

    def test_initial_status(self, spec_lifecycle):
        """测试初始状态"""
        requirement_id = "REQ-101"
        status = spec_lifecycle.get_status(requirement_id)
        assert status == SpecStatus.DRAFT

    def test_submit_for_review(self, spec_lifecycle):
        """测试提交审批"""
        requirement_id = "REQ-102"

        success = spec_lifecycle.submit_for_review(
            requirement_id=requirement_id,
            submitter="developer1",
            reason="Ready for review"
        )
        assert success

        status = spec_lifecycle.get_status(requirement_id)
        assert status == SpecStatus.REVIEW

    def test_approve(self, spec_lifecycle, sample_spec):
        """测试审批通过"""
        requirement_id = "REQ-103"

        # 先提交审批
        spec_lifecycle.submit_for_review(
            requirement_id=requirement_id,
            submitter="developer1"
        )

        # 审批通过
        success = spec_lifecycle.approve(
            requirement_id=requirement_id,
            approver="manager1",
            spec_data=sample_spec,
            reason="Approved"
        )
        assert success

        status = spec_lifecycle.get_status(requirement_id)
        assert status == SpecStatus.APPROVED

        # 验证版本已创建
        lifecycle_info = spec_lifecycle.get_lifecycle_info(requirement_id)
        assert lifecycle_info["current_version"] == 1

    def test_reject(self, spec_lifecycle):
        """测试审批退回"""
        requirement_id = "REQ-104"

        # 提交审批
        spec_lifecycle.submit_for_review(
            requirement_id=requirement_id,
            submitter="developer1"
        )

        # 退回
        success = spec_lifecycle.reject(
            requirement_id=requirement_id,
            approver="manager1",
            reason="Need more details"
        )
        assert success

        status = spec_lifecycle.get_status(requirement_id)
        assert status == SpecStatus.DRAFT

    def test_archive(self, spec_lifecycle, sample_spec):
        """测试归档"""
        requirement_id = "REQ-105"

        # 完整流程：draft -> review -> approved -> archived
        spec_lifecycle.submit_for_review(
            requirement_id=requirement_id,
            submitter="developer1"
        )

        spec_lifecycle.approve(
            requirement_id=requirement_id,
            approver="manager1",
            spec_data=sample_spec
        )

        success = spec_lifecycle.archive(
            requirement_id=requirement_id,
            operator="developer1",
            reason="Development completed"
        )
        assert success

        status = spec_lifecycle.get_status(requirement_id)
        assert status == SpecStatus.ARCHIVED

    def test_invalid_transition(self, spec_lifecycle):
        """测试无效的状态转换"""
        requirement_id = "REQ-106"

        # 尝试从 draft 直接到 archived（不允许）
        success = spec_lifecycle.transition_to(
            requirement_id=requirement_id,
            to_status=SpecStatus.ARCHIVED,
            operator="user1"
        )
        assert not success

    def test_get_history(self, spec_lifecycle, sample_spec):
        """测试获取状态变更历史"""
        requirement_id = "REQ-107"

        # 执行多次状态转换
        spec_lifecycle.submit_for_review(
            requirement_id=requirement_id,
            submitter="developer1"
        )

        spec_lifecycle.approve(
            requirement_id=requirement_id,
            approver="manager1",
            spec_data=sample_spec
        )

        # 获取历史
        history = spec_lifecycle.get_history(requirement_id)
        assert len(history) == 2
        assert history[0].from_status == SpecStatus.DRAFT.value
        assert history[0].to_status == SpecStatus.REVIEW.value
        assert history[1].from_status == SpecStatus.REVIEW.value
        assert history[1].to_status == SpecStatus.APPROVED.value

    def test_lifecycle_info(self, spec_lifecycle, sample_spec):
        """测试获取完整生命周期信息"""
        requirement_id = "REQ-108"

        # 执行完整流程
        spec_lifecycle.submit_for_review(
            requirement_id=requirement_id,
            submitter="developer1"
        )

        spec_lifecycle.approve(
            requirement_id=requirement_id,
            approver="manager1",
            spec_data=sample_spec
        )

        # 获取生命周期信息
        info = spec_lifecycle.get_lifecycle_info(requirement_id)
        assert info["requirement_id"] == requirement_id
        assert info["current_status"] == SpecStatus.APPROVED.value
        assert info["current_version"] == 1
        assert len(info["history"]) == 2
        assert len(info["versions"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
