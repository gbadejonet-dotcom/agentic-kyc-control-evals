from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

import typer
from rich.console import Console
from rich.table import Table

from .agent_interface import KycAgent
from .evaluator import evaluate_response
from .models import Scenario
from .sample_agents import RulesBasedBaselineAgent

app = typer.Typer(help="Run KYC agent evaluations.")
console = Console()

AgentName = Literal["baseline", "anthropic", "openai"]


def load_scenarios(path: Path) -> list[Scenario]:
    scenarios: list[Scenario] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                scenarios.append(Scenario.model_validate_json(line))
    return scenarios


def build_agent(agent_name: AgentName, model: str | None = None) -> KycAgent:
    if agent_name == "baseline":
        return RulesBasedBaselineAgent()

    if agent_name == "anthropic":
        from .adapters.anthropic_agent import AnthropicAgent

        kwargs = {"model": model} if model else {}
        return AnthropicAgent(**kwargs)

    if agent_name == "openai":
        from .adapters.openai_agent import OpenAIAgent

        kwargs = {"model": model} if model else {}
        return OpenAIAgent(**kwargs)

    raise typer.BadParameter(f"Unsupported agent: {agent_name}")


@app.command()
def main(
    scenarios: Path = typer.Option(..., "--scenarios", "-s", help="Path to scenarios JSONL file."),
    output: Path = typer.Option(Path("outputs/sample_run.json"), "--output", "-o"),
    agent: AgentName = typer.Option(
        "baseline",
        "--agent",
        "-a",
        help="Agent to evaluate: baseline, anthropic, or openai.",
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        "-m",
        help="Optional model override for Anthropic or OpenAI adapters.",
    ),
) -> None:
    selected_agent = build_agent(agent, model=model)
    loaded = load_scenarios(scenarios)

    results = []
    table = Table(title=f"Agentic KYC Control Eval Results — {agent}")
    table.add_column("Scenario")
    table.add_column("Type")
    table.add_column("Score")
    table.add_column("Pass")

    for scenario in loaded:
        response = selected_agent.review(scenario)
        evaluation = evaluate_response(scenario, response)
        results.append(
            {
                "agent": agent,
                "model": model,
                "scenario": scenario.model_dump(),
                "agent_response": response.model_dump(),
                "evaluation": evaluation.model_dump(),
            }
        )
        table.add_row(
            scenario.id,
            scenario.scenario_type.value,
            f"{evaluation.total_score}/{evaluation.max_score}",
            "yes" if evaluation.pass_threshold_met else "no",
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")

    console.print(table)
    console.print(f"\nWrote report to [bold]{output}[/bold]")


if __name__ == "__main__":
    app()
