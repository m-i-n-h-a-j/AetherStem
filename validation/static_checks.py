from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import yaml  # type: ignore[import-untyped]


PROJECT_PACKAGES = {"ai", "audio_io", "benchmarks", "cli", "dsp", "models", "pipeline", "utils", "validation"}


def validate_config_schema(path: Path) -> list[str]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for section in ("audio", "pipeline", "ai", "paths"):
        if section not in payload:
            errors.append(f"missing config section: {section}")
    audio = payload.get("audio", {})
    if int(audio.get("sample_rate", 0)) <= 0:
        errors.append("audio.sample_rate must be positive")
    if int(audio.get("bit_depth", 0)) <= 0:
        errors.append("audio.bit_depth must be positive")
    return errors


def validate_import_graph(paths: Iterable[Path]) -> list[str]:
    graph: dict[str, set[str]] = defaultdict(set)
    module_paths = [path for path in paths if path.suffix == ".py" and "__pycache__" not in path.parts]
    for path in module_paths:
        module = _module_name(path)
        for dependency in _imports(path):
            root = dependency.split(".", 1)[0]
            if root in PROJECT_PACKAGES and root != module.split(".", 1)[0]:
                graph[module].add(dependency)
    return _find_cycles(graph)


def _imports(path: Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return set()
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


def _module_name(path: Path) -> str:
    return ".".join(path.with_suffix("").parts)


def _find_cycles(graph: dict[str, set[str]]) -> list[str]:
    cycles: list[str] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, stack: list[str]) -> None:
        if node in visiting:
            start = stack.index(node) if node in stack else 0
            cycles.append(" -> ".join(stack[start:] + [node]))
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in graph.get(node, set()):
            visit(dependency, stack + [dependency])
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node, [node])
    return cycles
