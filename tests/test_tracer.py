
"""Unit tests for tracer instrumentation behavior."""

from __future__ import annotations

import json

import pytest

from src.tracer import AgentTracer, TraceStep


class DummyGraph:
    """Simple graph-like object with mutable node mapping."""

    def __init__(self) -> None:
        """Initializes three successful nodes."""
        self.nodes = {
            "retrieve": self.retrieve,
            "plan": self.plan,
            "answer": self.answer,
        }

    def invoke(self, state: dict) -> dict:
        """Runs nodes sequentially over the evolving state."""
        current = dict(state)
        for name in ("retrieve", "plan", "answer"):
            current = self.nodes[name](current)
        return current

    @staticmethod
    def retrieve(state: dict) -> dict:
        """Adds retrieved context to state."""
        result = dict(state)
        result["docs"] = ["doc-1"]
        return result

    @staticmethod
    def plan(state: dict) -> dict:
        """Adds a plan derived from docs."""
        result = dict(state)
        result["plan"] = "use doc-1"
        return result

    @staticmethod
    def answer(state: dict) -> dict:
        """Adds a final answer to state."""
        result = dict(state)
        result["answer"] = "done"
        return result


class FailingGraph:
    """Simple graph-like object with a failing node for error tracing."""

    def __init__(self) -> None:
        """Initializes one passing and one failing node."""
        self.nodes = {
            "ok": self.ok,
            "boom": self.boom,
        }

    def invoke(self, state: dict) -> dict:
        """Runs nodes sequentially and propagates failures."""
        current = dict(state)
        for name in ("ok", "boom"):
            current = self.nodes[name](current)
        return current

    @staticmethod
    def ok(state: dict) -> dict:
        """Returns state unchanged to simulate successful work."""
        return dict(state)

    @staticmethod
    def boom(state: dict) -> dict:
        """Raises a runtime error to test failure tracing."""
        _ = state
        raise RuntimeError("node exploded")


def test_tracer_captures_per_node_steps() -> None:
    """Ensures each node execution is recorded in order."""
    tracer = AgentTracer()
    graph = tracer.trace(DummyGraph())

    result = graph.invoke({"query": "hello"})
    steps = tracer.get_steps()

    assert result["answer"] == "done"
    assert [step.node_name for step in steps] == ["retrieve", "plan", "answer"]
    assert all(step.status == "success" for step in steps)
    assert all(step.latency_ms >= 0.0 for step in steps)


def test_tracer_records_error_status() -> None:
    """Ensures failures are captured with error status and message."""
    tracer = AgentTracer()
    graph = tracer.trace(FailingGraph())

    with pytest.raises(RuntimeError):
        graph.invoke({"query": "hello"})

    steps = tracer.get_steps()
    assert [step.node_name for step in steps] == ["ok", "boom"]
    assert steps[-1].status == "error"
    assert "node exploded" in (steps[-1].error or "")


def test_export_json_returns_serialized_trace() -> None:
    """Ensures JSON export returns parseable trace payload."""
    tracer = AgentTracer()
    graph = tracer.trace(DummyGraph())
    graph.invoke({"query": "hello"})

    payload = tracer.export_json()
    parsed = json.loads(payload)

    assert isinstance(parsed, list)
    assert parsed
    assert parsed[0]["node_name"] == "retrieve"


def test_tracer_respects_max_steps_retention() -> None:
    """Ensures oldest trace steps are evicted when retention limit is reached."""

    tracer = AgentTracer(max_steps=2)
    tracer.add_step(
        TraceStep(
            node_name="first",
            input_state={},
            output_state={},
            latency_ms=1.0,
            token_usage=1,
            timestamp="2026-01-01T00:00:00+00:00",
            status="success",
            error=None,
        )
    )
    tracer.add_step(
        TraceStep(
            node_name="second",
            input_state={},
            output_state={},
            latency_ms=1.0,
            token_usage=1,
            timestamp="2026-01-01T00:00:01+00:00",
            status="success",
            error=None,
        )
    )
    tracer.add_step(
        TraceStep(
            node_name="third",
            input_state={},
            output_state={},
            latency_ms=1.0,
            token_usage=1,
            timestamp="2026-01-01T00:00:02+00:00",
            status="success",
            error=None,
        )
    )

    assert tracer.get_max_steps() == 2
    assert [step.node_name for step in tracer.get_steps()] == ["second", "third"]


def test_tracer_rejects_invalid_max_steps() -> None:
    """Ensures tracer rejects non-positive retention settings."""

    with pytest.raises(ValueError):
        AgentTracer(max_steps=0)
