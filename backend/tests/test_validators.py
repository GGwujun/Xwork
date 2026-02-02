import unittest

from app.schemas import Collaboration, Metadata, OpenSpec, Requirement, Task, Workflow, WorkflowEdge, WorkflowNode
from app.validators import OpenSpecValidationError, validate_open_spec


class ValidatorTests(unittest.TestCase):
    def _base_spec(self) -> OpenSpec:
        return OpenSpec(
            project_name="Demo",
            requirement=Requirement(summary="Summary", description="Details"),
            tasks=[
                Task(id="task-1", title="First", description="One"),
                Task(id="task-2", title="Second", description="Two", dependencies=["task-1"]),
            ],
            workflow=Workflow(
                nodes=[
                    WorkflowNode(id="n1", type="task", label="Task 1"),
                    WorkflowNode(id="n2", type="task", label="Task 2"),
                ],
                edges=[WorkflowEdge(source="n1", target="n2")],
            ),
            collaboration=Collaboration(owner="user-1"),
            metadata=Metadata(created_at="2026-01-01T00:00:00Z", updated_at="2026-01-01T00:00:00Z"),
        )

    def test_valid_spec_passes(self) -> None:
        spec = self._base_spec()
        validate_open_spec(spec)

    def test_duplicate_task_ids_fail(self) -> None:
        spec = self._base_spec()
        spec.tasks.append(Task(id="task-1", title="Dup", description="Dup"))
        with self.assertRaises(OpenSpecValidationError):
            validate_open_spec(spec)

    def test_task_dependency_missing_fails(self) -> None:
        spec = self._base_spec()
        spec.tasks.append(Task(id="task-3", title="Third", description="Three", dependencies=["missing"]))
        with self.assertRaises(OpenSpecValidationError):
            validate_open_spec(spec)

    def test_workflow_cycle_fails(self) -> None:
        spec = self._base_spec()
        spec.workflow = Workflow(
            nodes=[
                WorkflowNode(id="a", type="task", label="A"),
                WorkflowNode(id="b", type="task", label="B"),
            ],
            edges=[WorkflowEdge(source="a", target="b"), WorkflowEdge(source="b", target="a")],
        )
        with self.assertRaises(OpenSpecValidationError):
            validate_open_spec(spec)


if __name__ == "__main__":
    unittest.main()
