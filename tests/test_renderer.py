
"""Tests for terminal trace renderer output."""

from __future__ import annotations

from io import StringIO

from rich.console import Console

from src.renderer import TraceRenderer
from src.tracer import TraceStep


def test_renderer_prints_timeline_and_summary() -> None:
    """Ensures renderer emits timeline and summary sections."""
    renderer = TraceRenderer()
    buffer = StringIO()
    console = Console(file=buffer, force_terminal=False, color_system=None)

    renderer.render(
        [
            TraceStep(
                node_name="retrieve",
                input_state={"query": "hello"},
                output_state={"docs": ["d1"]},
                latency_ms=2.3,
                token_usage=12,
                timestamp="2026-01-01T00:00:00+00:00",
                status="success",
                error=None,
            )
        ],
        console=console,
    )

    text = buffer.getvalue()
    assert "Agent Trace Timeline" in text
    assert "Trace Summary" in text
    assert "retrieve" in text
