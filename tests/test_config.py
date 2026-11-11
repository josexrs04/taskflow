import pytest

from taskflow import config


def test_get_notify_token_returns_value(monkeypatch):
    monkeypatch.setenv("NOTIFY_API_TOKEN", "abc123")
    assert config.get_notify_token() == "abc123"


def test_get_notify_token_missing(monkeypatch):
    monkeypatch.delenv("NOTIFY_API_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="NOTIFY_API_TOKEN"):
        config.get_notify_token()


def test_get_notify_token_blank(monkeypatch):
    monkeypatch.setenv("NOTIFY_API_TOKEN", "   ")
    with pytest.raises(RuntimeError):
        config.get_notify_token()