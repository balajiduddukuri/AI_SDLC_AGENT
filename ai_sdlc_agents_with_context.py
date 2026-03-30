from __future__ import annotations

from typing import Any, Dict, List
from pprint import pprint

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


SDLC_CONTEXT: Dict[str, Any] = {
    "feature_request": "",
    "requirements": "",
    "user_stories": "",
    "code_scaffold": "",
    "code_review": "",
    "test_plan": "",
    "test_execution": "",
    "defects": [],
    "release_decision": "PENDING",
    "history": [],
}


def _record(step: str, content: str) -> None:
    SDLC_CONTEXT["history"].append({"step": step, "content": content})


@tool
def update_feature_request(feature_request: str) -> str:
    """Initialize or update the SDLC context with the latest feature request."""
    SDLC_CONTEXT["feature_request"] = feature_request.strip()
    message = f"[CONTEXT UPDATED]\nFeature Request: {SDLC_CONTEXT['feature_request']}"
    _record("context_update", message)
    return message


@tool
def ba_gather_requirements(_: str = "") -> str:
    """BA tool to gather requirements from the current feature request in shared context."""
    feature = SDLC_CONTEXT.get("feature_request", "").strip()
    if not feature:
        return "No feature request found in context. Please initialize it first."

    output = f"""
[BA — Requirements Document]
Feature     : {feature}

Business Goal:
- Deliver a production-ready capability for: {feature}

Functional Requirements:
- The system shall support {feature}.
- Input validation must be enforced for all mandatory fields.
- All critical user actions must be logged with timestamps.
- Role-based access and error handling must be supported where applicable.

Non-Functional Requirements:
- Response time should remain under 2 seconds for standard operations.
- System availability target should be at least 99.9%.
- Data must be encrypted in transit and at rest.
- The design should support maintainability and future extensibility.

Acceptance Criteria:
- Feature works end-to-end in staging.
- Edge cases are handled gracefully.
- Logs and validation rules are verifiable.
- QA sign-off is required before release.
""".strip()

    SDLC_CONTEXT["requirements"] = output
    _record("ba_gather_requirements", output)
    return output


@tool
def ba_create_user_stories(_: str = "") -> str:
    """BA tool to convert current requirements into user stories and sprint scope."""
    requirements = SDLC_CONTEXT.get("requirements", "").strip()
    feature = SDLC_CONTEXT.get("feature_request", "").strip()

    if not requirements:
        return "No requirements found in context. Run BA requirements gathering first."

    output = f"""
[BA — User Stories]
Based on feature: {feature}

US-001 (5 pts) | As an end user, I want the core {feature} capability so that I can complete my task successfully.
US-002 (3 pts) | As a user, I want validation messages so that I can correct invalid input.
US-003 (5 pts) | As an admin, I want audit visibility so that I can trace important actions.
US-004 (2 pts) | As a user, I want friendly error handling so that failures are understandable.
US-005 (8 pts) | As a system owner, I want the feature to be secure and maintainable so that it is release-ready.

Sprint 1 Scope : US-001, US-002, US-004  [10 pts]
Sprint 2 Scope : US-003, US-005          [13 pts]
Definition of Done:
- Code completed
- Peer review done
- Test cases executed
- No critical defects open
""".strip()

    SDLC_CONTEXT["user_stories"] = output
    _record("ba_create_user_stories", output)
    return output


@tool
def dev_generate_code(_: str = "") -> str:
    """DEV tool to generate a code scaffold from current user stories and requirements."""
    feature = SDLC_CONTEXT.get("feature_request", "").strip()
    user_stories = SDLC_CONTEXT.get("user_stories", "").strip()

    if not user_stories:
        return "No user stories found in context. Create user stories before generating code."

    class_name = "FeatureService"

    output = f'''
[DEV — Code Scaffold]
Feature: {feature}

```python
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class {class_name}:
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

Next steps:
- Implement full business logic.
- Add API/service integration.
- Add unit and integration tests.
'''.strip()

    SDLC_CONTEXT["code_scaffold"] = output
    _record("dev_generate_code", output)
    return output


@tool
def dev_review_code(_: str = "") -> str:
    """DEV tool to review the currently generated code scaffold from shared context."""
    code = SDLC_CONTEXT.get("code_scaffold", "").strip()
    if not code:
        return "No generated code found in context. Generate code first."

    output = """
[DEV — Code Review Report]

Readability:
- The scaffold is structured and easy to follow.
- Methods are small and logically separated.

Security:
- No secrets are hard-coded.
- Input validation exists but should be expanded for field-level sanitization.

Performance:
- Current scaffold is lightweight.
- Consider caching or async handling if downstream integrations are expensive.

Best Practices:
- Add stricter schema validation.
- Replace generic validation with domain-specific checks.
- Add targeted exception handling instead of broad failure paths.
- Ensure observability with correlation IDs in logs.

Overall Score: 8.0 / 10
Recommendation: Proceed to QA after improving validation depth.
""".strip()

    SDLC_CONTEXT["code_review"] = output
    _record("dev_review_code", output)
    return output


@tool
def qa_generate_test_cases(_: str = "") -> str:
    """QA tool to create a test plan from current code review and requirements context."""
    code_review = SDLC_CONTEXT.get("code_review", "").strip()
    feature = SDLC_CONTEXT.get("feature_request", "").strip()

    if not code_review:
        return "No code review found in context. Review code before generating test cases."

    output = f"""
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
TC-010 | Security | Malicious script payload -> escaped/blocked

Automation Framework:
- pytest
- mocks/stubs for external dependencies

Coverage Target:
- 85% minimum
""".strip()

    SDLC_CONTEXT["test_plan"] = output
    _record("qa_generate_test_cases", output)
    return output


@tool
def qa_run_tests(_: str = "") -> str:
    """QA tool to simulate test execution and update defects/release decision in context."""
    test_plan = SDLC_CONTEXT.get("test_plan", "").strip()
    if not test_plan:
        return "No test plan found in context. Generate QA test cases first."

    defects = [
        {
            "id": "DEF-001",
            "severity": "High",
            "test_case": "TC-003",
            "summary": "Missing required field causes server-side failure instead of controlled validation response.",
        },
        {
            "id": "DEF-002",
            "severity": "Medium",
            "test_case": "TC-006",
            "summary": "Empty string payload values are not sanitized consistently.",
        },
    ]

    SDLC_CONTEXT["defects"] = defects
    SDLC_CONTEXT["release_decision"] = "NOT APPROVED"

    output = """
[QA — Test Execution Report]

PASSED  : TC-001, TC-002, TC-007, TC-008
FAILED  : TC-003, TC-006
SKIPPED : TC-009, TC-010

Pass Rate : 60%
Release Recommendation: DO NOT DEPLOY

Defects Logged:
- DEF-001 | High   | Missing required field returns incorrect failure behavior.
- DEF-002 | Medium | Empty string sanitization gap detected.

Recommended Actions:
- Fix validation and sanitization issues.
- Re-run regression tests.
- Obtain QA sign-off before staging deployment.
""".strip()

    SDLC_CONTEXT["test_execution"] = output
    _record("qa_run_tests", output)
    return output


@tool
def summarize_sdlc_context(_: str = "") -> str:
    """Summarize the entire shared SDLC context for final reporting."""
    feature = SDLC_CONTEXT.get("feature_request", "")
    release_decision = SDLC_CONTEXT.get("release_decision", "PENDING")
    defects = SDLC_CONTEXT.get("defects", [])

    defect_lines = "\n".join(
        [f"- {d['id']} ({d['severity']}): {d['summary']}" for d in defects]
    ) or "- No defects logged"

    output = f"""
[SDLC CONTEXT SUMMARY]

Feature Request:
{feature}

Requirements Captured:
{"Yes" if SDLC_CONTEXT.get("requirements") else "No"}

User Stories Created:
{"Yes" if SDLC_CONTEXT.get("user_stories") else "No"}

Code Generated:
{"Yes" if SDLC_CONTEXT.get("code_scaffold") else "No"}

Code Reviewed:
{"Yes" if SDLC_CONTEXT.get("code_review") else "No"}

Test Plan Created:
{"Yes" if SDLC_CONTEXT.get("test_plan") else "No"}

Test Execution Completed:
{"Yes" if SDLC_CONTEXT.get("test_execution") else "No"}

Release Decision:
{release_decision}

Defects:
{defect_lines}
""".strip()

    _record("summarize_sdlc_context", output)
    return output


tools = [
    update_feature_request,
    ba_gather_requirements,
    ba_create_user_stories,
    dev_generate_code,
    dev_review_code,
    qa_generate_test_cases,
    qa_run_tests,
    summarize_sdlc_context,
]


system_prompt = """
You are an AI SDLC orchestration agent that follows a structured BA -> DEV -> QA workflow.

Use the shared SDLC context aggressively:
- Always initialize or confirm the feature request first.
- Then gather requirements.
- Then create user stories.
- Then generate code.
- Then review code.
- Then generate QA test cases.
- Then run QA tests.
- Then summarize the SDLC context.

Rules:
- Prefer using the accumulated context instead of asking for the same information again.
- Keep outputs structured and professional.
- Highlight defects and release status clearly.
- If a prior step is missing, run that step first.
"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


model = ChatOpenAI(model="gpt-4o", temperature=0)


agent = create_react_agent(
    model=model,
    tools=tools,
    prompt=prompt,
)


def run_agent(feature_request: str) -> Dict[str, Any]:
    response = agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"""
Please run the full AI SDLC workflow for this feature request:

{feature_request}

Use the context-aware workflow and provide a final release recommendation.
""".strip(),
                )
            ]
        }
    )
    return response


if __name__ == "__main__":
    feature = "Build a user authentication module with login, registration, and password reset functionality"

    result = run_agent(feature)

    print("=" * 70)
    print("AI SDLC AGENT — FINAL RESPONSE")
    print("=" * 70)

    for message in result.get("messages", []):
        try:
            if getattr(message, "type", "") == "ai":
                print("\n[AI MESSAGE]")
                print(message.content)
        except Exception:
            pass

    print("\n" + "=" * 70)
    print("SHARED SDLC CONTEXT")
    print("=" * 70)
    pprint(SDLC_CONTEXT)
