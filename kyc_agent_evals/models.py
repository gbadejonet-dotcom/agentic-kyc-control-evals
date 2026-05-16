from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ScenarioType(str, Enum):
    NOMINEE = "nominee_shareholder"
    PAHV = "personal_asset_holding_vehicle"
    SANCTIONS = "sanctions_false_positive"
    SOURCE_OF_WEALTH = "missing_source_of_wealth"
    PROMPT_INJECTION = "prompt_injection"


class Scenario(BaseModel):
    id: str
    title: str
    scenario_type: ScenarioType
    customer_profile: str
    file_material: str
    task: str
    expected_issues: list[str] = Field(default_factory=list)
    red_flags: list[str] = Field(default_factory=list)
    gold_standard_next_steps: list[str] = Field(default_factory=list)


class AgentResponse(BaseModel):
    scenario_id: str
    conclusion: str
    issues_identified: list[str] = Field(default_factory=list)
    risk_rating: Literal["low", "medium", "high", "critical"]
    rationale: str
    evidence_cited: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)


class CriterionScore(BaseModel):
    name: str
    score: int = Field(ge=0, le=5)
    comment: str


class EvaluationResult(BaseModel):
    scenario_id: str
    total_score: int
    max_score: int
    criteria: list[CriterionScore]
    pass_threshold_met: bool
    summary: str
