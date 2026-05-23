from __future__ import annotations

from cli.help.registry import HelpRegistry, default_help_registry


def search_help(query: str, registry: HelpRegistry | None = None):
    return (registry or default_help_registry).search(query)

