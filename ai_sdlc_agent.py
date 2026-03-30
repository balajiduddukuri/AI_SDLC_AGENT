# ============================================================
# AI SDLC Agent  — LangGraph + LangChain ReAct Agent
# Roles: Business Analyst (BA), Developer (DEV), QA Engineer
# ============================================================

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import create_react_agent

# ----------------------------------------------------------
# 1. LLM Setup
# ----------------------------------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# ===========================================================
# 2. SDLC Tools
# ===========================================================

# ---- Business Analyst (BA) Tools -------------------------

@tool
def ba_gather_requirements(feature_request: str) -> str:
    """
    Business Analyst tool.
    Accepts a raw feature request and returns structured
    functional & non-functional requirements as a BRD snippet.
    """
    return f"""
[BA — Requirements Document]
Feature     : {feature_request}
User Stories:
  - As a user, I want to {feature_request.lower()} so that I can achieve my goal.
Functional Requirements:
  - The system shall support {feature_request}.
  - Input validation must be enforced.
  - All actions must be logged with a timestamp.
Non-Functional Requirements:
  - Response time < 2 seconds.
  - System availability >= 99.9%.
  - Data must be encrypted at rest and in transit.
Acceptance Criteria:
  - Feature works end-to-end in staging environment.
  - All edge cases from UAT session are covered.
"""

@tool
def ba_create_user_stories(requirements: str) -> str:
    """
    Business Analyst tool.
    Converts requirements text into INVEST-compliant user stories
    with story points (Fibonacci scale).
    """
    return f"""
[BA — User Stories]
Based on: {requirements[:120]}...

US-001 (5 pts)  | As a user, I can log in with email & password.
US-002 (3 pts)  | As a user, I can reset my password via email OTP.
US-003 (8 pts)  | As an admin, I can view a dashboard of all active users.
US-004 (2 pts)  | As a user, I receive a confirmation email after registration.
US-005 (5 pts)  | As a user, I can update my profile information.

Sprint 1 Scope  : US-001, US-002, US-004   [10 pts]
Sprint 2 Scope  : US-003, US-005           [13 pts]
"""

# ---- Developer (DEV) Tools --------------------------------

@tool
def dev_generate_code(user_story: str) -> str:
    """
    Developer tool.
    Accepts a user story and returns a Python code scaffold
    with docstrings, type hints, and basic error handling.
    """
    return f"""
[DEV — Code Scaffold]
User Story : {user_story}

```python
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FeatureService:
    \"\"\"Service class implementing: {user_story}\"\"\"

    def execute(self, payload: dict) -> dict:
        \"\"\"
        Execute the feature logic.

        Args:
            payload (dict): Input data from the API layer.

        Returns:
            dict: Response with status, data, and timestamp.

        Raises:
            ValueError: If payload is invalid.
        \"\"\"
        if not payload:
            raise ValueError("Payload cannot be empty.")

        logger.info("Executing feature at %s", datetime.utcnow())

        # TODO: Implement business logic here
        result = {{"status": "success", "data": payload, "timestamp": str(datetime.utcnow())}}
        return result
```

Next steps:
  - Implement business logic inside execute().
  - Add unit tests (see QA tool).
  - Raise a PR against the 'develop' branch.
"""

@tool
def dev_review_code(code_snippet: str) -> str:
    """
    Developer tool.
    Performs a static code review and returns a structured
    feedback report covering readability, security, and performance.
    """
    return f"""
[DEV — Code Review Report]
Snippet reviewed (truncated): {code_snippet[:100]}...

Readability  : ✅  Functions are small and single-purpose.
               ⚠️  Add docstrings to all public methods.
Security     : ✅  No hard-coded secrets detected.
               ⚠️  Validate and sanitize all user inputs before processing.
Performance  : ✅  No obvious N+1 query patterns.
               ⚠️  Consider caching repeated DB reads with Redis.
Best Practices:
  - Use type hints throughout.
  - Replace bare 'except' with specific exception types.
  - Ensure logging is in place for every critical operation.
Overall Score: 7.5 / 10  — Minor improvements recommended before merge.
"""

# ---- QA Engineer Tools ------------------------------------

@tool
def qa_generate_test_cases(feature_description: str) -> str:
    """
    QA tool.
    Generates a test plan with positive, negative, and edge-case
    test cases for the given feature description.
    """
    return f"""
[QA — Test Plan]
Feature: {feature_description}

TC-001 | Positive | Happy path — valid inputs → 200 OK
TC-002 | Positive | Optional fields omitted → 200 OK with defaults applied
TC-003 | Negative | Missing required field → 400 Bad Request
TC-004 | Negative | Invalid data type → 422 Unprocessable Entity
TC-005 | Negative | Unauthorized access → 401 Unauthorized
TC-006 | Edge     | Empty string input → 400 Bad Request
TC-007 | Edge     | Payload at max size boundary → 200 OK
TC-008 | Edge     | Concurrent requests (load test, 100 RPS) → no data race
TC-009 | Security | SQL injection attempt → 400 / sanitized
TC-010 | Security | XSS payload in text field → escaped in response

Automation Framework : pytest + requests
Coverage Target      : ≥ 85%
"""

@tool
def qa_run_tests(test_cases: str) -> str:
    """
    QA tool.
    Simulates test execution and returns a pass/fail report
    with a coverage summary and defect log.
    """
    return f"""
[QA — Test Execution Report]
Tests run based on: {test_cases[:100]}...

PASSED  : TC-001, TC-002, TC-007, TC-008
FAILED  : TC-003, TC-006
SKIPPED : TC-009, TC-010 (pending security review sign-off)

Pass Rate : 60%  ⚠️  Below 85% threshold — do NOT deploy.

Defects Logged:
  DEF-001 | TC-003 | Missing-field validation not returning 400 (returns 500).
  DEF-002 | TC-006 | Empty string passes validation — logic gap in sanitizer.

Recommended Actions:
  - Fix DEF-001 and DEF-002 before re-run.
  - Re-execute full regression suite after fixes.
  - Obtain QA sign-off before promoting to staging.
"""

# ===========================================================
# 3. Tool Registry
# ===========================================================
tools = [
    ba_gather_requirements,
    ba_create_user_stories,
    dev_generate_code,
    dev_review_code,
    qa_generate_test_cases,
    qa_run_tests,
]

# ===========================================================
# 4. Prompt Template
# ===========================================================
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an AI SDLC Orchestrator managing a software delivery pipeline.
You coordinate three specialist roles:

  🔵 Business Analyst (BA)
     - ba_gather_requirements  : Converts a feature request into structured BRD.
     - ba_create_user_stories  : Produces INVEST user stories with story points.

  🟢 Developer (DEV)
     - dev_generate_code       : Scaffolds Python code from a user story.
     - dev_review_code         : Reviews code and returns a quality report.

  🔴 QA Engineer (QA)
     - qa_generate_test_cases  : Creates a full test plan for a feature.
     - qa_run_tests            : Simulates test execution and returns results.

RULES:
  1. Always follow the SDLC sequence:
       BA (requirements) → BA (user stories) → DEV (code) → DEV (review) → QA (test cases) → QA (run tests)
  2. Pass the output of each step as input to the next step.
  3. After all steps are complete, produce a concise SDLC Summary Report.
  4. Do NOT skip any step.
  5. Do NOT repeat a tool call unnecessarily.
"""
    ),
    MessagesPlaceholder(variable_name="messages"),
])

# ===========================================================
# 5. Create ReAct Agent
# ===========================================================
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=prompt
)

# ===========================================================
# 6. Run the SDLC Pipeline
# ===========================================================
if __name__ == "__main__":
    feature_request = (
        "Build a user authentication module with login, "
        "registration, and password reset functionality"
    )

    print("=" * 60)
    print("  AI SDLC Agent — Starting Pipeline")
    print(f"  Feature: {feature_request}")
    print("=" * 60)

    result = agent.invoke({
        "messages": [
            ("user", f"Run the full SDLC pipeline for: {feature_request}")
        ]
    })

    # ---- Final Answer ------------------------------------
    print("\n📋  FINAL SDLC REPORT\n")
    print(result["messages"][-1].content)

    # ---- Tool Call Log -----------------------------------
    print("\n" + "=" * 60)
    print("  TOOL EXECUTION LOG")
    print("=" * 60)
    for msg in result["messages"]:
        if isinstance(msg, ToolMessage):
            print(f"\n🔧  Tool   : {msg.name}")
            print(f"   Output : {msg.content[:300]}...")
            print("-" * 60)
