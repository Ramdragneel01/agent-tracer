
"""Terminal rendering utilities for agent trace timelines."""

from __future__ import annotations

from typing import Iterable, List, Union

from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from .tracer import TraceStep


class TraceRenderer:
    """Renders trace steps as a readable timeline tree in terminal output."""

    def render(self, steps: Iterable[Union[TraceStep, dict]], console: Console | None = None) -> None:
        """Prints a timeline tree and summary table for trace steps."""
        console = console or Console()
        normalized_steps = self._normalize_steps(steps)

        tree = Tree("Agent Trace Timeline")
        for step in normalized_steps:
            status_tag = "[green]success[/green]" if step.status == "success" else "[red]error[/red]"
            tree.add(
                f"{step.node_name} | {status_tag} | {step.latency_ms:.2f} ms | {step.token_usage} tokens"
            )

        summary = Table(title="Trace Summary")
        summary.add_column("Metric", style="cyan")
        summary.add_column("Value", justify="right", style="magenta")
        summary.add_row("Steps", str(len(normalized_steps)))
        summary.add_row(
            "Total latency (ms)",
            f"{sum(step.latency_ms for step in normalized_steps):.2f}",
        )
        summary.add_row(
            "Total tokens",
            str(sum(step.token_usage for step in normalized_steps)),
        )

        console.print(tree)
        console.print(summary)

    @staticmethod
    def _normalize_steps(steps: Iterable[Union[TraceStep, dict]]) -> List[TraceStep]:
        """Converts mixed dict/dataclass inputs into TraceStep dataclasses."""
        normalized: List[TraceStep] = []
        for step in steps:
            if isinstance(step, TraceStep):
                normalized.append(step)
                continue
            normalized.append(
                TraceStep(
                    node_name=str(step.get("node_name", "unknown")),
                    input_state=step.get("input_state"),
                    output_state=step.get("output_state"),
                    latency_ms=float(step.get("latency_ms", 0.0)),
                    token_usage=int(step.get("token_usage", 0)),
                    timestamp=str(step.get("timestamp", "")),
                    status=str(step.get("status", "unknown")),
                    error=step.get("error"),
                )
            )
        return normalized
