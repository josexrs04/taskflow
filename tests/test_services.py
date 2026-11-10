import pytest

from taskflow.services import TaskService
from taskflow.storage import JsonStorage


@pytest.fixture
def service(tmp_path):
    return TaskService(JsonStorage(tmp_path / "tasks.json"))


def test_add_task(service):
    task = service.add("Escribir informe", priority="high")
    assert task.id == 1
    assert task.priority == "high"


def test_add_invalid_priority(service):
    with pytest.raises(ValueError):
        service.add("X", priority="urgentísima")


def test_complete_task(service):
    task = service.add("Tarea")
    service.complete(task.id)
    assert service.list()[0].done is True


def test_list_pending_only(service):
    a = service.add("A")
    service.add("B")
    service.complete(a.id)
    assert [t.title for t in service.list(include_done=False)] == ["B"]


def test_delete_task(service):
    task = service.add("Borrame")
    service.delete(task.id)
    assert service.list() == []
