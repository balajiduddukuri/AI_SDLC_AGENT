from __future__ import annotations

from typing import TypedDict, List, Dict, Any, Literal
from pprint import pprint

from langgraph.graph import StateGraph, END


class Defect(TypedDict):
    id: str
    severity: str
    test_case: str
    summary: str


class SDLCAgentState(TypedDict):
    feature_request: str
    requirements: str
    user_stories: str
    code_scaffold: str
    code_review: str
    test_plan: str
    test_execution: str
    defects: List[Defect]
    release_decision: str
    next_step: str
    history: List[Dict[str, str]]


def add_history(state: SDLCAgentState, step: str, content: str) -> None:
    state["history"].append({"step": step, "content": content})


def initialize_state(feature_request: str) -> SDLCAgentState:
    return {
        "feature_request": feature_request,
        "requirements": "",
        "user_stories": "",
        "code_scaffold": "",
        "code_review": "",
        "test_plan": "",
        "test_execution": "",
        "defects": [],
        "release_decision": "PENDING",
        "next_step": "ba_node",
        "history": [],
    }


def ba_node(state: SDLCAgentState) -> SDLCAgentState:
    feature = state["feature_request"]

    requirements = f"""
[BA — Requirements Document]
Feature     : {feature}

Business Goal:
- Deliver a production-ready capability for: {feature}

Functional Requirements:
- The system shall support {feature}.
- Input validation must be enforced for all mandatory fields.
- Critical user actions must be logged with timestamps.
- Error handling and role-aware access must be supported where applicable.

Non-Functional Requirements:
- Response time should remain under 2 seconds.
- Availability target should be at least 99.9%.
- Data must be encrypted in transit and at rest.
- The solution should remain maintainable and extensible.

Acceptance Criteria:
- Feature works end-to-end in staging.
- Edge cases are handled gracefully.
- Validation, logs, and functional paths are verifiable.
- QA sign-off is required before release.
""".strip()

    user_stories = f"""
[BA — User Stories]
Based on feature: {feature}

US-001 (5 pts) | As an end user, I want the core feature to work so that I can complete my goal.
US-002 (3 pts) | As a user, I want validation feedback so that I can correct invalid input.
US-003 (5 pts) | As an admin, I want audit visibility so that I can trace key actions.
US-004 (2 pts) | As a user, I want understandable error messages so that failures are actionable.
US-005 (8 pts) | As a system owner, I want the feature to be secure and maintainable so that it is release-ready.

Sprint 1 Scope : US-001, US-002, US-004  [10 pts]
Sprint 2 Scope : US-003, US-005          [13 pts]
Definition of Done:
- Code completed
- Review completed
- QA executed
- No critical defects open
""".strip()

    state["requirements"] = requirements
    state["user_stories"] = user_stories
    state["next_step"] = "dev_node"

    add_history(state, "ba_node", requirements)
    add_history(state, "ba_node", user_stories)
    return state


def dev_node(state: SDLCAgentState) -> SDLCAgentState:
    feature = state["feature_request"]

    code_scaffold = f'''
[DEV — Code Scaffold]
Feature: {feature}

```python
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FeatureService:
    """Service class for: {feature}"""

    def validate_payload(self, payload: Dict[str, Any]) -> None:
        if not payload:
            raise ValueError("Payload cannot be empty.")

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the feature logic.

        Args:
            payload: Input data from the caller.

        Returns:
            A structured response with status, data, and timestamp.
        """
        self.validate_payload(payload)
        logger.info("Executing feature at %s", datetime.utcnow().isoformat())

        result = {{
            "status": "success",
            "feature": "{feature}",
            "data": payload,
            "timestamp": datetime.utcnow().isoformat()
        }}
        return result
```
'''.strip()

    code_review = """
[DEV — Code Review Report]

Readability:
- The scaffold is clean and easy to follow.
- Methods are logically separated.

Security:
- No hard-coded secrets detected.
- Validation should be expanded to field-level sanitization.

Performance:
- Current scaffold is lightweight.
- Consider async handling or caching for expensive downstream calls.

Best Practices:
- Add stricter schema validation.
- Add domain-specific validation rules.
- Replace generic failure paths with targeted exception handling.
- Improve logging with correlation IDs.

Overall Score: 8.0 / 10
Recommendation: Proceed to QA after validation improvements.
""".strip()

    state["code_scaffold"] = code_scaffold
    state["code_review"] = code_review
    state["next_step"] = "qa_node"

    add_history(state, "dev_node", code_scaffold)
    add_history(state, "dev_node", code_review)
    return state


def qa_node(state: SDLCAgentState) -> SDLCAgentState:
    feature = state["feature_request"]

    test_plan = f"""
[QA — Test Plan]
Feature: {feature}

TC-001 | Positive | Happy path with valid input -> success response
TC-002 | Positive | Optional values omitted -> defaults applied safely
TC-003 | Negative | Missing required field -> validation error
TC-004 | Negative | Invalid data type -> rejected request
TC-005 | Negative | Unauthorized access -> access denied
TC-006 | Edge     | Empty string payload values -> validation error
TC-007 | Edge     | Boundary-size payload -> handled successfully
TC-008 | Edge     | Concurrent execution scenario -> no race condition
TC-009 | Security | Injection attempt -> blocked or sanitized
TC-010 | Security | Malicious script payload -> escaped or blocked

Automation Framework:
- pytest
- mocks/stubs for external dependencies

Coverage Target:
- 85% minimum
""".strip()

    defects: List[Defect] = [
        {
            "id": "DEF-001",
            "severity": "High",
            "test_case": "TC-003",
            "summary": "Missing required field causes incorrect server-side failure behavior.",
        },
        {
            "id": "DEF-002",
            "severity": "Medium",
            "test_case": "TC-006",
            "summary": "Empty string payload values are not sanitized consistently.",
        },
    ]

    test_execution = """
[QA — Test Execution Report]

PASSED  : TC-001, TC-002, TC-007, TC-008
FAILED  : TC-003, TC-006
SKIPPED : TC-009, TC-010

Pass Rate : 60%
Recommendation: DO NOT DEPLOY

Defects Logged:
- DEF-001 | High   | Missing required field returns incorrect failure behavior.
- DEF-002 | Medium | Empty string sanitization gap detected.

Recommended Actions:
- Fix validation and sanitization issues.
- Re-run regression tests.
- Obtain QA sign-off before staging deployment.
""".strip()

    state["test_plan"] = test_plan
    state["test_execution"] = test_execution
    state["defects"] = defects
    state["next_step"] = "release_gate_node"

    add_history(state, "qa_node", test_plan)
    add_history(state, "qa_node", test_execution)
    return state


def release_gate_node(state: SDLCAgentState) -> SDLCAgentState:
    has_high_defect = any(d["severity"].lower() == "high" for d in state["defects"])
    has_any_defect = len(state["defects"]) > 0

    if has_high_defect:
        decision = "NOT_APPROVED"
    elif has_any_defect:
        decision = "CONDITIONAL_APPROVAL"
    else:
        decision = "APPROVED"

    state["release_decision"] = decision
    state["next_step"] = END

    summary = f"""
[RELEASE GATE]

Feature Request:
{state["feature_request"]}

Release Decision:
{decision}

Open Defects:
{len(state["defects"])}

Decision Logic:
- High severity defect present: {"Yes" if has_high_defect else "No"}
- Any defect present: {"Yes" if has_any_defect else "No"}

Final Recommendation:
{"Do not deploy until defects are fixed and QA re-run." if decision == "NOT_APPROVED" else
 "Deploy only with agreed mitigations and stakeholder approval." if decision == "CONDITIONAL_APPROVAL" else
 "Approved for deployment."}
""".strip()

    add_history(state, "release_gate_node", summary)
    return state


def route_from_release_gate(state: SDLCAgentState) -> Literal["end"]:
    return "end"


graph = StateGraph(SDLCAgentState)

graph.add_node("ba_node", ba_node)
graph.add_node("dev_node", dev_node)
graph.add_node("qa_node", qa_node)
graph.add_node("release_gate_node", release_gate_node)

graph.set_entry_point("ba_node")
graph.add_edge("ba_node", "dev_node")
graph.add_edge("dev_node", "qa_node")
graph.add_edge("qa_node", "release_gate_node")
graph.add_conditional_edges(
    "release_gate_node",
    route_from_release_gate,
    {"end": END},
)

app = graph.compile()


def run_sdlc(feature_request: str) -> SDLCAgentState:
    initial_state = initialize_state(feature_request)
    final_state = app.invoke(initial_state)
    return final_state


def print_final_report(state: SDLCAgentState) -> None:
    print("=" * 72)
    print("AI SDLC STATEGRAPH — FINAL REPORT")
    print("=" * 72)
    print(f"Feature Request   : {state['feature_request']}")
    print(f"Release Decision  : {state['release_decision']}")
    print(f"Open Defects      : {len(state['defects'])}")
    print()

    print("[Requirements]")
    print(state["requirements"])
    print()

    print("[User Stories]")
    print(state["user_stories"])
    print()

    print("[Code Review]")
    print(state["code_review"])
    print()

    print("[QA Execution]")
    print(state["test_execution"])
    print()

    print("[Defects]")
    for defect in state["defects"]:
        print(f"- {defect['id']} | {defect['severity']} | {defect['test_case']} | {defect['summary']}")
    print()

    print("[History]")
    for item in state["history"]:
        print(f"- {item['step']}")


if __name__ == "__main__":
    feature = "Build a user authentication module with login, registration, and password reset functionality"
    final_state = run_sdlc(feature)

    print_final_report(final_state)

    print("\n" + "=" * 72)
    print("RAW FINAL STATE")
    print("=" * 72)
    pprint(final_state)
