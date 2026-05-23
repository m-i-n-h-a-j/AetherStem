from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cli.help.registry import CommandHelp, HelpRegistry


class HelpFormatter:
    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    def overview(self, registry: HelpRegistry) -> None:
        table = Table(title="AetherStem Help")
        table.add_column("Command", style="cyan")
        table.add_column("Category", style="magenta")
        table.add_column("Summary")
        for command in registry.all():
            table.add_row(command.name, command.category, command.summary)
        self.console.print(table)
        self.console.print("Use [cyan]aetherstem help COMMAND[/cyan] for contextual help.")

    def command(self, command: CommandHelp) -> None:
        self.console.print(Panel(command.description, title=f"{command.name}: {command.summary}", border_style="cyan"))
        table = Table(show_header=False)
        table.add_column("Field", style="magenta")
        table.add_column("Value")
        table.add_row("Usage", command.usage)
        if command.options:
            table.add_row("Options", "\n".join(command.options))
        if command.examples:
            table.add_row("Examples", "\n".join(command.examples))
        if command.related:
            table.add_row("Related", ", ".join(command.related))
        if command.troubleshooting:
            table.add_row("Troubleshooting", "\n".join(command.troubleshooting))
        self.console.print(table)

