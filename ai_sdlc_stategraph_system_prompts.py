from __future__ import annotations

from typing import TypedDict, List, Literal
from pprint import pprint

from langgraph.graph import StateGraph, END


SYSTEM_PROMPT = """
You are an enterprise AI SDLC orchestration assistant.

Your role is to guide a software initiative through a full SDLC lifecycle using structured stages:
1. Vision & Business Case
2. Requirements & Discovery
3. Solution Design & Architecture
4. Implementation (Coding)
5. Testing & Quality Engineering
6. Security & Compliance Gates
7. Deployment & Release Management
8. Operations, Monitoring & Feedback

Operating rules:
- Preserve business intent across all stages.
- Treat every stage as auditable and client-facing.
- Generate concise but structured outputs.
- Include sub-steps relevant to the stage.
- If client enhancements or change requests are provided, incorporate them into the current stage and downstream stages.
- Track impacts to requirements, architecture, implementation, testing, security, release, and operations.
- When enhancements introduce new scope, note them as backlog additions, change requests, or tech debt items.
- Maintain forward traceability from business requirement to deployment and operational feedback.
- Use professional SDLC language suitable for enterprise delivery teams.
- Never discard earlier context unless the client explicitly replaces it.
""".strip()

USER_PROMPT_TEMPLATE = """
Client Initiative:
{product_name}

Business Context:
{business_context}

Requested Enhancements / Updates:
{client_enhancements}

Expected Outcome:
Run the SDLC workflow end-to-end, incorporating the client enhancements into all affected stages.

Special Instructions:
- Highlight impact of enhancements.
- Show where requirements, design, implementation, testing, security, deployment, or operations changed.
- Capture any new risks, dependencies, or backlog items.
""".strip()

VISION_PROMPT = """
You are working on the Vision & Business Case stage.

Inputs:
- Product / initiative name
- Business context
- Client enhancements

Tasks:
- Summarize the initiative vision.
- Clarify business value and expected outcomes.
- Identify business drivers influenced by the client enhancements.
- Note any revised goals, KPIs, or stakeholder expectations.
""".strip()

REQUIREMENTS_PROMPT = """
You are working on the Requirements & Discovery stage.

Tasks:
- Capture stakeholder needs.
- Update personas and use cases if the client enhancements change user behavior.
- Produce FR/NFR considerations.
- Update backlog and acceptance criteria.
- Flag any change requests, dependencies, assumptions, and open questions.
""".strip()

DESIGN_PROMPT = """
You are working on the Solution Design & Architecture stage.

Tasks:
- Reflect enhanced requirements in the high-level architecture.
- Update data flows, integration flows, and sequence/state behavior if needed.
- Identify architecture impacts introduced by client enhancements.
- Highlight any sign-off items needed from architecture, security, or platform teams.
""".strip()

IMPLEMENTATION_PROMPT = """
You are working on the Implementation stage.

Tasks:
- Translate design updates into implementation workstreams.
- Identify coding scope, branch strategy, unit test updates, and review expectations.
- Reflect new modules, APIs, validations, or integrations caused by client enhancements.
- Mention build artifact or merge impacts if relevant.
""".strip()

TESTING_PROMPT = """
You are working on the Testing & Quality Engineering stage.

Tasks:
- Update test plan and test cases to reflect client enhancements.
- Mention test data setup changes.
- Cover both automated and manual testing impacts.
- Identify new regression, integration, or UAT risks introduced by the enhancement.
- Capture expected defect triage focus areas.
""".strip()

SECURITY_PROMPT = """
You are working on the Security & Compliance stage.

Tasks:
- Assess how client enhancements affect threat modeling.
- Identify impacts to static scans, dynamic scans, dependency/SBOM checks, or privacy/compliance review.
- Mention any compliance controls or approvals needed.
- Highlight security risks introduced by new integrations, data flows, or permissions.
""".strip()

RELEASE_PROMPT = """
You are working on the Deployment & Release Management stage.

Tasks:
- Reflect enhancement impact on pre-prod deployment, smoke/canary checks, change approval, production deployment, and rollback readiness.
- Mention if rollout strategy must change because of client-requested enhancements.
- Capture deployment dependencies and operational readiness needs.
""".strip()

OPERATIONS_PROMPT = """
You are working on the Operations, Monitoring & Feedback stage.

Tasks:
- Define how monitoring, alerts, incident handling, RCA, and backlog improvements should adapt to the client enhancements.
- Capture operational feedback loops.
- Distinguish between immediate defects, future improvements, and tech debt.
""".strip()


class StageRecord(TypedDict):
    stage: str
    prompt_used: str
    details: str


class SDLCPipelineState(TypedDict):
    product_name: str
    business_context: str
    client_enhancements: str
    system_prompt: str
    current_user_prompt: str
    vision_business_case: str
    requirements_discovery: str
    solution_design_architecture: str
    implementation_coding: str
    testing_quality_engineering: str
    security_compliance_gates: str
    deployment_release_management: str
    operations_monitoring_feedback: str
    insights_defects: List[str]
    tech_debt_enhancements: List[str]
    backlog_items: List[str]
    risks_dependencies: List[str]
    status: str
    next_step: str
    history: List[StageRecord]


def add_history(state: SDLCPipelineState, stage: str, prompt_used: str, details: str) -> None:
    state["history"].append(
        {
            "stage": stage,
            "prompt_used": prompt_used,
            "details": details,
        }
    )


def initialize_state(product_name: str, business_context: str, client_enhancements: str) -> SDLCPipelineState:
    return {
        "product_name": product_name,
        "business_context": business_context,
        "client_enhancements": client_enhancements,
        "system_prompt": SYSTEM_PROMPT,
        "current_user_prompt": USER_PROMPT_TEMPLATE.format(
            product_name=product_name,
            business_context=business_context,
            client_enhancements=client_enhancements,
        ),
        "vision_business_case": "",
        "requirements_discovery": "",
        "solution_design_architecture": "",
        "implementation_coding": "",
        "testing_quality_engineering": "",
        "security_compliance_gates": "",
        "deployment_release_management": "",
        "operations_monitoring_feedback": "",
        "insights_defects": [],
        "tech_debt_enhancements": [],
        "backlog_items": [],
        "risks_dependencies": [],
        "status": "INITIATED",
        "next_step": "vision_business_case_node",
        "history": [],
    }


def vision_business_case_node(state: SDLCPipelineState) -> SDLCPipelineState:
    prompt = f"""
{SYSTEM_PROMPT}

{VISION_PROMPT}

Client Initiative:
{state['product_name']}

Business Context:
{state['business_context']}

Client Enhancements:
{state['client_enhancements']}
""".strip()

    details = f"""
Vision & Business Case
- Product / initiative: {state['product_name']}
- Business context: {state['business_context']}
- Client enhancements considered: {state['client_enhancements']}
- Define business objective, target users, expected value, and success metrics.
- Establish why the initiative should be funded and delivered.
- Updated goals, stakeholder expectations, and business outcomes documented.
""".strip()

    state["current_user_prompt"] = prompt
    state["vision_business_case"] = details
    state["next_step"] = "requirements_discovery_node"
    add_history(state, "Vision & Business Case", prompt, details)
    return state


def requirements_discovery_node(state: SDLCPipelineState) -> SDLCPipelineState:
    prompt = f"""
{SYSTEM_PROMPT}

{REQUIREMENTS_PROMPT}

Client Initiative:
{state['product_name']}

Business Context:
{state['business_context']}

Client Enhancements:
{state['client_enhancements']}
""".strip()

    details = f"""
Requirements & Discovery
- Stakeholder Interviews
- Personas & Use Cases
- FR/NFR Draft
- Backlog & Acceptance Criteria

Enhancement Impact:
- Client enhancements reviewed and mapped to new/updated functional requirements.
- Non-functional requirements adjusted where scale, performance, security, or compliance are affected.
- Acceptance criteria updated to reflect enhancement scope.
""".strip()

    state["current_user_prompt"] = prompt
    state["requirements_discovery"] = details
    state["backlog_items"].extend(
        [
            "Enhancement stories added to backlog",
            "Acceptance criteria updated for new client-requested flows",
        ]
    )
    state["risks_dependencies"].extend(
        [
            "Clarify stakeholder sign-off for enhancement scope",
            "Validate downstream integration dependency impacts",
        ]
    )
    state["next_step"] = "solution_design_architecture_node"
    add_history(state, "Requirements & Discovery", prompt, details)
    return state


def solution_design_architecture_node(state: SDLCPipelineState) -> SDLCPipelineState:
    prompt = f"""
{SYSTEM_PROMPT}

{DESIGN_PROMPT}

Client Initiative:
{state['product_name']}

Business Context:
{state['business_context']}

Client Enhancements:
{state['client_enhancements']}
""".strip()

    details = f"""
Solution Design & Architecture
- High-Level Architecture
- Data / Integration Flows
- Sequence / State Diagrams
- Design Review & Sign-off

Enhancement Impact:
- Architecture updated to include enhancement-driven changes.
- Integration and state behavior reviewed for compatibility.
- Design sign-off required for updated flows introduced by the client.
""".strip()

    state["current_user_prompt"] = prompt
    state["solution_design_architecture"] = details
    state["risks_dependencies"].extend(
        [
            "Architecture review needed for enhancement-driven design changes",
            "Sequence/state updates may affect existing service contracts",
        ]
    )
    state["next_step"] = "implementation_coding_node"
    add_history(state, "Solution Design & Architecture", prompt, details)
    return state


def implementation_coding_node(state: SDLCPipelineState) -> SDLCPipelineState:
    prompt = f"""
{SYSTEM_PROMPT}

{IMPLEMENTATION_PROMPT}

Client Initiative:
{state['product_name']}

Business Context:
{state['business_context']}

Client Enhancements:
{state['client_enhancements']}
""".strip()

    details = f"""
Implementation (Coding)
- Branch From Main
- Code + Unit Tests
- Pull Request & Review
- Merge & Build Artifact

Enhancement Impact:
- Development scope updated to include enhancement-specific modules, validations, APIs, or integrations.
- Unit tests expanded for enhancement coverage.
- PR review checklist updated for new business and technical rules.
""".strip()

    state["current_user_prompt"] = prompt
    state["implementation_coding"] = details
    state["tech_debt_enhancements"].append("Refactor impacted modules after enhancement delivery to keep codebase maintainable")
    state["next_step"] = "testing_quality_engineering_node"
    add_history(state, "Implementation (Coding)", prompt, details)
    return state


def testing_quality_engineering_node(state: SDLCPipelineState) -> SDLCPipelineState:
    prompt = f"""
{SYSTEM_PROMPT}

{TESTING_PROMPT}

Client Initiative:
{state['product_name']}

Business Context:
{state['business_context']}

Client Enhancements:
{state['client_enhancements']}
""".strip()

    details = f"""
Testing & Quality Engineering
- Test Plan & Cases
- Test Data Setup
- Automated & Manual Tests
- Defect Triage

Enhancement Impact:
- New test cases added for client enhancements.
- Regression scope expanded where existing flows are affected.
- UAT considerations updated for enhancement acceptance.
""".strip()

    state["current_user_prompt"] = prompt
    state["testing_quality_engineering"] = details
    state["insights_defects"].extend(
        [
            "Enhancement-related regression risk identified",
            "Additional validation scenarios needed for updated user flows",
        ]
    )
    state["next_step"] = "security_compliance_gates_node"
    add_history(state, "Testing & Quality Engineering", prompt, details)
    return state


def security_compliance_gates_node(state: SDLCPipelineState) -> SDLCPipelineState:
    prompt = f"""
{SYSTEM_PROMPT}

{SECURITY_PROMPT}

Client Initiative:
{state['product_name']}

Business Context:
{state['business_context']}

Client Enhancements:
{state['client_enhancements']}
""".strip()

    details = f"""
Security & Compliance Gates
- Threat Modeling
- Static / Dynamic Scans
- SBOM + Supply Chain Checks
- Privacy / Compliance Review

Enhancement Impact:
- Security posture reviewed for enhancement-related data flow or permission changes.
- Additional privacy/compliance review needed if the enhancement expands personal or regulated data handling.
""".strip()

    state["current_user_prompt"] = prompt
    state["security_compliance_gates"] = details
    state["risks_dependencies"].extend(
        [
            "Threat model updates required for enhancement scope",
            "Compliance review may delay release if data handling changes are significant",
        ]
    )
    state["next_step"] = "deployment_release_management_node"
    add_history(state, "Security & Compliance Gates", prompt, details)
    return state


def deployment_release_management_node(state: SDLCPipelineState) -> SDLCPipelineState:
    prompt = f"""
{SYSTEM_PROMPT}

{RELEASE_PROMPT}

Client Initiative:
{state['product_name']}

Business Context:
{state['business_context']}

Client Enhancements:
{state['client_enhancements']}
""".strip()

    details = f"""
Deployment & Release Management
- Pre-prod Deploy
- Smoke / Canary
- Change Approval
- Prod Deploy & Post-Deploy Checks
- Rollback Plan Ready

Enhancement Impact:
- Release strategy reviewed for enhancement-sensitive rollout.
- Smoke/canary checks updated for newly introduced capabilities.
- Rollback readiness validated for enhancement changes.
""".strip()

    state["current_user_prompt"] = prompt
    state["deployment_release_management"] = details
    state["next_step"] = "operations_monitoring_feedback_node"
    add_history(state, "Deployment & Release Management", prompt, details)
    return state


def operations_monitoring_feedback_node(state: SDLCPipelineState) -> SDLCPipelineState:
    prompt = f"""
{SYSTEM_PROMPT}

{OPERATIONS_PROMPT}

Client Initiative:
{state['product_name']}

Business Context:
{state['business_context']}

Client Enhancements:
{state['client_enhancements']}
""".strip()

    details = f"""
Operations, Monitoring & Feedback
- Monitoring & Alerts
- Incident Response
- Root Cause Analysis
- Backlog Improvements

Feedback Loops:
- Insights & Defects -> Requirements & Discovery
- Tech Debt & Enhancements -> Solution Design & Architecture

Enhancement Impact:
- Monitoring updated to observe enhancement-related behavior.
- Backlog improvements captured from post-release learning.
- Tech debt and future enhancements documented for next iteration.
""".strip()

    state["current_user_prompt"] = prompt
    state["operations_monitoring_feedback"] = details
    state["tech_debt_enhancements"].extend(
        [
            "Observability tuning for enhancement-driven workflows",
            "Backlog follow-up for deferred enhancement refinements",
        ]
    )
    state["status"] = "COMPLETED"
    state["next_step"] = "end"
    add_history(state, "Operations, Monitoring & Feedback", prompt, details)
    return state


def route_after_operations(state: SDLCPipelineState) -> Literal["end"]:
    return "end"


graph = StateGraph(SDLCPipelineState)

graph.add_node("vision_business_case_node", vision_business_case_node)
graph.add_node("requirements_discovery_node", requirements_discovery_node)
graph.add_node("solution_design_architecture_node", solution_design_architecture_node)
graph.add_node("implementation_coding_node", implementation_coding_node)
graph.add_node("testing_quality_engineering_node", testing_quality_engineering_node)
graph.add_node("security_compliance_gates_node", security_compliance_gates_node)
graph.add_node("deployment_release_management_node", deployment_release_management_node)
graph.add_node("operations_monitoring_feedback_node", operations_monitoring_feedback_node)

graph.set_entry_point("vision_business_case_node")
graph.add_edge("vision_business_case_node", "requirements_discovery_node")
graph.add_edge("requirements_discovery_node", "solution_design_architecture_node")
graph.add_edge("solution_design_architecture_node", "implementation_coding_node")
graph.add_edge("implementation_coding_node", "testing_quality_engineering_node")
graph.add_edge("testing_quality_engineering_node", "security_compliance_gates_node")
graph.add_edge("security_compliance_gates_node", "deployment_release_management_node")
graph.add_edge("deployment_release_management_node", "operations_monitoring_feedback_node")
graph.add_conditional_edges(
    "operations_monitoring_feedback_node",
    route_after_operations,
    {"end": END},
)

app = graph.compile()


def run_pipeline(product_name: str, business_context: str, client_enhancements: str) -> SDLCPipelineState:
    initial_state = initialize_state(product_name, business_context, client_enhancements)
    return app.invoke(initial_state)


def print_report(state: SDLCPipelineState) -> None:
    print("=" * 90)
    print("AI SDLC IMAGE-BASED STATEGRAPH WITH CLIENT ENHANCEMENT PROMPTS")
    print("=" * 90)
    print(f"Product Name        : {state['product_name']}")
    print(f"Business Context    : {state['business_context']}")
    print(f"Client Enhancements : {state['client_enhancements']}")
    print(f"Status              : {state['status']}")
    print()

    ordered_sections = [
        ("Vision & Business Case", state["vision_business_case"]),
        ("Requirements & Discovery", state["requirements_discovery"]),
        ("Solution Design & Architecture", state["solution_design_architecture"]),
        ("Implementation (Coding)", state["implementation_coding"]),
        ("Testing & Quality Engineering", state["testing_quality_engineering"]),
        ("Security & Compliance Gates", state["security_compliance_gates"]),
        ("Deployment & Release Management", state["deployment_release_management"]),
        ("Operations, Monitoring & Feedback", state["operations_monitoring_feedback"]),
    ]

    for title, content in ordered_sections:
        print(f"[{title}]")
        print(content)
        print()

    print("[Backlog Items]")
    for item in state["backlog_items"]:
        print(f"- {item}")
    print()

    print("[Risks & Dependencies]")
    for item in state["risks_dependencies"]:
        print(f"- {item}")
    print()

    print("[Insights & Defects]")
    for item in state["insights_defects"]:
        print(f"- {item}")
    print()

    print("[Tech Debt & Enhancements]")
    for item in state["tech_debt_enhancements"]:
        print(f"- {item}")
    print()

    print("[History]")
    for item in state["history"]:
        print(f"- {item['stage']}")


if __name__ == "__main__":
    final_state = run_pipeline(
        product_name="Enterprise Customer Onboarding Platform",
        business_context="A regulated enterprise platform used to onboard business customers across regions with workflow approvals, integrations, and auditability requirements.",
        client_enhancements="Add multilingual onboarding, new KYC validation workflow, enhanced audit reporting, and region-specific compliance rules."
    )

    print_report(final_state)

    print("\n" + "=" * 90)
    print("RAW FINAL STATE")
    print("=" * 90)
    pprint(final_state)
