
"""Demonstrates tracing on a simple three-node graph."""

from __future__ import annotations

from typing import Any, Dict

from src.renderer import TraceRenderer
from src.tracer import AgentTracer


class DemoGraph:
    """A tiny graph-like object exposing a mutable nodes mapping."""

    def __init__(self) -> None:
        """Initializes demo nodes in execution order."""
        self.nodes = {
            "retrieve": self.retrieve,
            "summarize": self.summarize,
            "answer": self.answer,
        }

    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Executes all demo nodes sequentially."""
        current = dict(state)
        for name in ("retrieve", "summarize", "answer"):
            current = self.nodes[name](current)
        return current

    @staticmethod
    def retrieve(state: Dict[str, Any]) -> Dict[str, Any]:
        """Adds mock retrieval artifacts to state."""
        next_state = dict(state)
        next_state["documents"] = [
            "Indexing can reduce timeout on large joins.",
            "Connection pooling lowers overhead for short-lived requests.",
        ]
        return next_state

    @staticmethod
    def summarize(state: Dict[str, Any]) -> Dict[str, Any]:
        """Builds a compact summary from retrieved documents."""
        next_state = dict(state)
        docs = next_state.get("documents", [])
        next_state["summary"] = " ".join(docs[:1])
        return next_state

    @staticmethod
    def answer(state: Dict[str, Any]) -> Dict[str, Any]:
        """Constructs the final answer payload from summary content."""
        next_state = dict(state)
        summary = next_state.get("summary", "")
        next_state["final_answer"] = f"Recommendation: {summary}"
        return next_state


def main() -> None:
    """Runs demo graph with tracer and renders a terminal timeline."""
    tracer = AgentTracer()
    graph = tracer.trace(DemoGraph())

    result = graph.invoke({"query": "How to reduce DB timeout?"})

    print("Final answer:")
    print(result.get("final_answer", "<missing>"))
    print()

    renderer = TraceRenderer()
    renderer.render(tracer.get_steps())

    print()
    print("JSON export:")
    print(tracer.export_json())


if __name__ == "__main__":
    main()
