from __future__ import annotations

from abc import ABC, abstractmethod

from .models import AgentResponse, Scenario


class KycAgent(ABC):
    """Abstract interface for any agent being evaluated."""

    @abstractmethod
    def review(self, scenario: Scenario) -> AgentResponse:
        """Review a KYC/AML scenario and return a structured response."""
        raise NotImplementedError
