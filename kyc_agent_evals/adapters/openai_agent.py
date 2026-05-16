from __future__ import annotations

import os
from typing import Any

from kyc_agent_evals.agent_interface import KycAgent
from kyc_agent_evals.models import AgentResponse, Scenario

from .prompt_builder import build_system_prompt, build_user_prompt, parse_agent_response_json


class OpenAIAgent(KycAgent):
    """OpenAI adapter.

    Requires the optional `openai` package and an `OPENAI_API_KEY` environment variable.
    The dependency is imported lazily so normal CI and baseline runs do not require paid API SDKs.
    """

    def __init__(
        self,
        model: str = "gpt-4.1-mini",
        temperature: float = 0.0,
        client: Any | None = None,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.client = client or self._build_client()

    @staticmethod
    def _build_client() -> Any:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ImportError(
                "OpenAIAgent requires the optional dependency `openai`. "
                "Install it with: pip install openai"
            ) from exc

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

        return OpenAI(api_key=api_key)

    def review(self, scenario: Scenario) -> AgentResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": build_system_prompt()},
                {"role": "user", "content": build_user_prompt(scenario)},
            ],
        )

        raw_text = response.choices[0].message.content or ""
        return parse_agent_response_json(raw_text, scenario_id=scenario.id)
