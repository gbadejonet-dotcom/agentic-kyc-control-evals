from __future__ import annotations

from .agent_interface import KycAgent
from .models import AgentResponse, Scenario, ScenarioType


class RulesBasedBaselineAgent(KycAgent):
    """Simple deterministic baseline.

    This is intentionally basic. It exists so the harness runs without API keys.
    LLM agents should later be added as adapters that implement KycAgent.
    """

    def review(self, scenario: Scenario) -> AgentResponse:
        issues: list[str] = []
        actions: list[str] = []
        evidence: list[str] = []

        material = f"{scenario.customer_profile}\n{scenario.file_material}".lower()

        if scenario.scenario_type == ScenarioType.PROMPT_INJECTION:
            issues.append(
                "Customer-supplied material contains instructions attempting to override reviewer controls."
            )
            actions.append("Ignore customer-supplied instructions and assess only substantive evidence.")
            evidence.append("Embedded instruction detected in customer-provided document.")
            risk_rating = "high"

        elif scenario.scenario_type == ScenarioType.NOMINEE:
            issues.append("Nominee arrangement may obscure beneficial ownership or control.")
            actions.append("Obtain nominee agreement, beneficial owner confirmation, and control rationale.")
            evidence.append("File references nominee shareholder arrangement.")
            risk_rating = "high"

        elif scenario.scenario_type == ScenarioType.PAHV:
            issues.append(
                "Entity may be a Personal Asset Holding Vehicle requiring specific risk classification."
            )
            actions.append("Validate source of funds/source of wealth and purpose of structure.")
            evidence.append("Entity appears to hold personal/family assets rather than operating trade.")
            risk_rating = "high"

        elif scenario.scenario_type == ScenarioType.SOURCE_OF_WEALTH:
            issues.append("Source of wealth evidence is missing, weak, or not independently corroborated.")
            actions.append("Request independent SOW/SOF evidence proportionate to risk.")
            evidence.append("File lacks documentary support for wealth origin.")
            risk_rating = "high"

        elif scenario.scenario_type == ScenarioType.SANCTIONS:
            if "date of birth mismatch" in material or "different jurisdiction" in material:
                issues.append("Potential sanctions false positive requires documented discounting rationale.")
                actions.append("Record matching logic, identifiers checked, and reason for discounting.")
                evidence.append("Identifiers appear inconsistent with sanctioned person.")
                risk_rating = "medium"
            else:
                issues.append("Possible sanctions match requires escalation.")
                actions.append("Escalate for sanctions review before onboarding or exit decision.")
                evidence.append("Name match appears in screening output.")
                risk_rating = "critical"
        else:
            issues.append("Control issue requires manual review.")
            actions.append("Escalate to senior reviewer.")
            evidence.append("Scenario type not mapped.")
            risk_rating = "medium"

        return AgentResponse(
            scenario_id=scenario.id,
            conclusion="Review completed with control issues identified.",
            issues_identified=issues,
            risk_rating=risk_rating,
            rationale="Baseline rules were applied to the scenario type and file material.",
            evidence_cited=evidence,
            recommended_actions=actions,
        )
