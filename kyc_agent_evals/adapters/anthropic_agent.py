from __future__ import annotations

import os
from typing import Any

from kyc_agent_evals.agent_interface import KycAgent
from kyc_agent_evals.models import AgentResponse, Scenario

from .prompt_builder import build_system_prompt, build_user_prompt, parse_agent_response_json


class AnthropicAgent(KycAgent):
    """Anthropic Claude adapter.

    Requires the optional `anthropic` package and an `ANTHROPIC_API_KEY` environment variable.
    The dependency is imported lazily so normal CI and baseline runs do not require paid API SDKs.
    """

    def __init__(
        self,
        model: str = "claude-3-5-sonnet-latest",
        max_tokens: int = 1200,
        temperature: float = 0.0,
        client: Any | None = None,
    ) -> None:
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.client = client or self._build_client()

    @staticmethod
    def _build_client() -> Any:
        try:
            from anthropic import Anthropic
        except ImportError as exc:
            raise ImportError(
                "AnthropicAgent requires the optional dependency `anthropic`. "
                "Install it with: pip install anthropic"
            ) from exc

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set.")

        return Anthropic(api_key=api_key)

    def review(self, scenario: Scenario) -> AgentResponse:
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=build_system_prompt(),
            messages=[{"role": "user", "content": build_user_prompt(scenario)}],
        )

        raw_text = "".join(
            block.text for block in message.content if getattr(block, "type", None) == "text"
        )
        return parse_agent_response_json(raw_text, scenario_id=scenario.id)
