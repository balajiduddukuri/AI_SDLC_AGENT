# AI SDLC Image-Based StateGraph with Client Enhancement Prompts

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Compatible-brightgreen)](https://langchain-ai.github.io/langgraph/)
[![Status](https://img.shields.io/badge/Status-Completed-success)]()

## Overview

This project implements an enterprise AI SDLC orchestration workflow using LangGraph. It takes a product initiative, business context, and client enhancement requests as input, then produces a structured end-to-end SDLC state across vision, discovery, design, implementation, testing, security, release, and operations.

The workflow is designed for regulated enterprise delivery environments where auditability, traceability, and change impact management are important.

## Business Context

The reference use case is an enterprise customer onboarding platform used to onboard business customers across regions with workflow approvals, integrations, and auditability requirements.

The pipeline is especially useful when client enhancements introduce new scope that must be propagated through downstream SDLC stages.

## Client Enhancements

The current enhancement set includes:

- Multilingual onboarding.
- New KYC validation workflow.
- Enhanced audit reporting.
- Region-specific compliance rules.

These enhancements influence requirements, architecture, implementation, test coverage, compliance checks, release planning, and operational feedback.

## What This Project Does

The program:

- Defines a structured SDLC state model.
- Runs a sequential LangGraph workflow.
- Updates each stage with enhancement-aware content.
- Captures backlog items, risks, insights, and tech debt.
- Produces a final auditable state object and printable report.

## SDLC Workflow Stages

The pipeline follows these stages:

1. Vision & Business Case.
2. Requirements & Discovery.
3. Solution Design & Architecture.
4. Implementation (Coding).
5. Testing & Quality Engineering.
6. Security & Compliance Gates.
7. Deployment & Release Management.
8. Operations, Monitoring & Feedback.

Each stage preserves earlier context and adds enhancement-specific impact where relevant.

## Enhancement Handling

Client enhancements are not treated as isolated changes. They are propagated across the workflow to ensure downstream consistency.

Examples of tracked impacts include:

- Updated functional and non-functional requirements.
- Architecture changes for integrations or state behavior.
- Coding scope changes such as validations, APIs, or modules.
- New test cases and expanded regression coverage.
- Threat model and compliance review updates.
- Release strategy and rollback considerations.
- Monitoring, backlog, and tech-debt follow-ups.

## Output Structure

The final output includes:

- Product name.
- Business context.
- Client enhancements.
- Stage-wise SDLC outputs.
- Backlog items.
- Risks and dependencies.
- Insights and defects.
- Tech debt and enhancement follow-ups.
- Execution history.
- Final status and next step.

## Project Files

### Core Components

- `SYSTEM_PROMPT`: Defines the enterprise orchestration role and operating rules.
- `USER_PROMPT_TEMPLATE`: Builds the user-facing prompt from the initiative inputs.
- Stage prompts: One prompt per SDLC phase.
- `SDLCPipelineState`: Typed state definition for the workflow.
- Stage nodes: Functions that populate each SDLC stage.
- `StateGraph`: LangGraph orchestration for the full lifecycle.
- `run_pipeline()`: Entry point to execute the workflow.
- `print_report()`: Formats and prints the final state.

## Requirements

- Python 3.10 or later.
- `langgraph`.
- `typing` and `pprint` from the standard library.
- A compatible LangGraph runtime environment.

Example installation:

```bash
pip install langgraph
```

If your environment also uses LangChain-related packages, install them according to your project stack.

## How to Run

Save the program as `main.py`, then execute:

```bash
python main.py
```

The script will:

1. Initialize the pipeline state.
2. Run the LangGraph workflow.
3. Print the stage-by-stage report.
4. Print the raw final state object.

## Example Input

The default execution in the script uses:

- Product name: `Enterprise Customer Onboarding Platform`
- Business context: a regulated enterprise onboarding platform.
- Client enhancements: multilingual onboarding, KYC validation, audit reporting, and region-specific compliance rules.

## Example Output

The output includes structured sections such as:

- Vision & Business Case.
- Requirements & Discovery.
- Solution Design & Architecture.
- Implementation (Coding).
- Testing & Quality Engineering.
- Security & Compliance Gates.
- Deployment & Release Management.
- Operations, Monitoring & Feedback.

It also includes tracked backlog items, risks, insights, and tech debt entries.

## Extending the Workflow

You can extend the workflow by:

- Adding new SDLC stages.
- Replacing hardcoded stage details with model-generated outputs.
- Passing structured enhancement objects instead of plain strings.
- Writing outputs to JSON, Markdown, or a database.
- Adding conditional routing for rework loops or approvals.
- Integrating approvals, notifications, or ticketing systems.

## Known Limitations

- The current implementation is deterministic and template-driven.
- Stage outputs are predefined rather than dynamically generated by an LLM.
- The workflow is linear and does not yet support branching, retries, or exception handling.
- There is no persistence layer for storing state across runs.

## Contributing

Contributions are welcome. Good improvement areas include:

- Better state normalization.
- More detailed compliance tracking.
- Dynamic prompt generation.
- Structured output export.
- Error handling and validation.
- Multi-path workflow routing.

## License

Add your preferred license here, such as MIT or Apache-2.0.

## Acknowledgments

This project demonstrates how enterprise SDLC workflows can be modeled using LangGraph and structured state management.


# AI SDLC Image-Based StateGraph with Client Enhancement Prompts

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Compatible-brightgreen)](https://langchain-ai.github.io/langgraph/)
[![Status](https://img.shields.io/badge/Status-Completed-success)]()

> An enterprise SDLC orchestration workflow that tracks client enhancements across vision, discovery, design, implementation, testing, security, release, and operations.

---

## Overview

This repository contains a structured AI-assisted SDLC pipeline built with LangGraph. It models an end-to-end enterprise delivery lifecycle and preserves traceability across all stages while incorporating client-requested enhancements.

The workflow is designed for regulated business environments where auditability, compliance, and change impact management are critical.

---

## Business Context

The reference solution is an **Enterprise Customer Onboarding Platform** used to onboard business customers across regions with workflow approvals, system integrations, and auditability requirements.

Client enhancements in this workflow include:

- Multilingual onboarding
- New KYC validation workflow
- Enhanced audit reporting
- Region-specific compliance rules

---

## Workflow Stages

The pipeline follows these SDLC stages:

1. Vision & Business Case
2. Requirements & Discovery
3. Solution Design & Architecture
4. Implementation (Coding)
5. Testing & Quality Engineering
6. Security & Compliance Gates
7. Deployment & Release Management
8. Operations, Monitoring & Feedback

Each stage carries forward business intent and captures enhancement-driven impact.

---

## Key Capabilities

- Structured SDLC state management.
- Enhancement-aware stage outputs.
- Backlog, risk, and dependency tracking.
- Operational feedback and tech-debt capture.
- Final auditable state generation.
- Human-readable report output.

---

## Output Highlights

The final state includes:

- Product and business context.
- Enhancement scope.
- Stage-wise SDLC outputs.
- Backlog items.
- Risks and dependencies.
- Insights and defects.
- Tech debt and future enhancements.
- Execution history.

---

## Project Structure

| Component | Purpose |
|---|---|
| `SYSTEM_PROMPT` | Defines enterprise orchestration behavior |
| `USER_PROMPT_TEMPLATE` | Builds the input prompt for the initiative |
| Stage prompt constants | Define stage-specific instructions |
| `SDLCPipelineState` | Typed workflow state definition |
| Stage node functions | Populate each SDLC phase |
| `StateGraph` | Orchestrates the end-to-end flow |
| `run_pipeline()` | Executes the workflow |
| `print_report()` | Prints the final structured output |

---

## Requirements

- Python 3.10+
- `langgraph`

Install dependencies:

```bash
pip install langgraph
```

If your environment also uses related LangChain packages, install them as needed for your stack.

---

## Usage

Run the script:

```bash
python <>.py
```

The program will:

1. Initialize the SDLC state.
2. Run through all workflow stages.
3. Print a stage-by-stage report.
4. Display the raw final state.

---

## Example Input

The default execution uses:

- Product Name: `Enterprise Customer Onboarding Platform`
- Business Context: regulated enterprise onboarding across regions
- Enhancements: multilingual onboarding, KYC validation, audit reporting, compliance rules

---

## Extending the Workflow

You can extend this repository by:

- Adding more SDLC stages.
- Introducing conditional routing or approval loops.
- Converting static stage content into LLM-generated outputs.
- Exporting results to JSON or Markdown.
- Connecting to Jira, Confluence, or CI/CD systems.
- Adding persistence for workflow state and audit logs.

---

## Limitations

- The current implementation is deterministic and template-based.
- It does not yet support branching or retries.
- It does not persist state externally.
- Stage content is predefined rather than dynamically generated.

---

## Contributing

Contributions are welcome. Useful improvements include:

- Better schema validation.
- Dynamic prompt generation.
- More detailed compliance and risk tracking.
- Persistence and audit logging.
- Structured export formats.
- Exception handling and workflow recovery.

---

## License

Add your preferred license here, such as MIT or Apache-2.0.
