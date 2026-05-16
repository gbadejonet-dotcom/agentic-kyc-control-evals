# Agentic KYC Control Evals

A lightweight evaluation harness for testing whether AI agents can perform high-risk KYC / AML file review tasks in a controlled, auditable way.

This project is designed as a research artefact for AI safety, AI security, compliance automation, and model evaluation work. It focuses on agent behaviour in regulated-finance scenarios where mistakes are not just bad answers — they can create legal, supervisory, and financial-crime risk.

## Research question

Can AI agents reliably identify, escalate, and evidence-control failures in high-risk customer due diligence files without hallucinating, over-escalating, or degrading the audit trail?

## Why this matters

Financial institutions are increasingly experimenting with AI agents for operational review, customer due diligence, adverse media analysis, sanctions triage, and remediation. The weak version of this trend is dangerous: models can produce confident but unauditable conclusions.

This repo tests agent outputs against structured compliance expectations:

- Did the agent identify the real control issue?
- Did it distinguish ownership, control, influence, and risk?
- Did it avoid accepting weak documentation at face value?
- Did it preserve an audit trail?
- Did it resist prompt-injection instructions inside customer documents?
- Did it recommend proportionate next steps?

## Current scope

The first version covers five scenario types:

1. Nominee shareholder confusion
2. Personal Asset Holding Vehicle classification
3. Sanctions false positive triage
4. Missing source of wealth evidence
5. Prompt injection inside customer-supplied documents

## Quick start

```bash
git clone https://github.com/gbadejonet-dotcom/agentic-kyc-control-evals.git
cd agentic-kyc-control-evals

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
python -m kyc_agent_evals.runner --scenarios data/scenarios.jsonl --output outputs/sample_run.json
```

## Evaluation dimensions

Each scenario is scored across:

- `issue_detection`
- `risk_reasoning`
- `evidence_quality`
- `auditability`
- `proportionality`
- `prompt_injection_resistance`

## Intended next milestones

- Add LLM adapters for Anthropic and OpenAI APIs
- Add richer scenario generation
- Add red-team prompt-injection cases
- Add model-comparison reports
- Add a short research paper based on initial findings

## Non-goals

This is not legal advice, regulatory advice, or a production KYC system. It is a research/evaluation harness for controlled testing.

## Licence

MIT.
