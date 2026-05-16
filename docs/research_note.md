# Research Note: Evaluating AI Agents in High-Risk KYC Decision Environments

## Abstract

AI agents are increasingly being positioned as tools for regulated-finance review, including customer due diligence, source-of-wealth assessment, sanctions triage, and remediation support. The risk is that institutions may mistake fluent outputs for defensible control execution.

This project proposes a lightweight evaluation harness to test whether AI agents can identify KYC / AML control failures, preserve an audit trail, resist prompt injection, and recommend proportionate next steps.

## Core hypothesis

AI agents can assist KYC review, but only where their outputs are constrained by scenario-specific evaluation, structured evidence requirements, and clear escalation logic.

Without evaluation, agents may:

- hallucinate missing evidence;
- over-accept weak customer narratives;
- under-escalate high-risk structures;
- confuse ownership with control;
- accept customer-supplied prompt-injection instructions;
- produce unauditable conclusions.

## Evaluation dimensions

The harness scores agent outputs against six dimensions:

1. Issue detection
2. Risk reasoning
3. Evidence quality
4. Auditability
5. Proportionality
6. Prompt-injection resistance

## Initial scenario classes

### Nominee shareholder confusion

Nominee arrangements are often misread as a reason to stop ownership analysis. A defensible review should ask: who is the nominee acting for, what rights are exercised, and who ultimately controls the asset or entity?

### Personal Asset Holding Vehicle risk

A private company holding family assets may not behave like a trading company. Its purpose, source of wealth, ownership/control logic, and structure rationale require a different risk lens.

### Sanctions false positive triage

A name match can be discounted only where the identifier comparison is clear, retained, and auditable. Weak notes such as common name are not enough.

### Missing source of wealth

High-risk customers require corroborated source-of-wealth evidence. Narrative alone is not evidence.

### Prompt injection in customer documents

AI-assisted review creates a new control risk: customer documents may include instructions designed to manipulate the reviewing model. The agent must ignore those instructions and evaluate only substantive evidence.

## Why this is strategically useful

For AI safety and security research, regulated-finance KYC provides a high-stakes testbed:

- Decisions require judgement, not simple extraction.
- Errors can create regulatory and crime-prevention failures.
- Outputs must be evidence-led and auditable.
- Adversarial inputs are realistic.
- Human oversight remains essential.

## Next research steps

1. Add LLM adapters for Anthropic and OpenAI models.
2. Run comparative evaluations across baseline, small models, and frontier models.
3. Introduce adversarial document packs.
4. Add human-review labels.
5. Publish a short technical report on control failure modes in agentic KYC review.
