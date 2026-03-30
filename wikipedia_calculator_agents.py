import wikipedia
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent

@tool
def wikipedia_search(aquery: str) -> str:
    """Search Wikipedia and return a short summary"""
    try:
        return wikipedia.summary(aquery, sentences=2)
    except Exception as e:
        return f"Wikipedia error: {str(e)}"

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {str(e)}"

tools = [wikipedia_search, calculator]


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an intelligent research scientist

        RULES:
        1. Use wikipedia once to get factual information
        2. Use calculator if numerical calculation is required
        3. After using tools, produce final answer
        4. Do not repeat tool usage after final answer
        """
    ),
    MessagesPlaceholder(variable_name="messages"),
])


agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=prompt
)

result = agent.invoke({
    "messages": [
        ("user", "What is the population of India according to Wikipedia, what is 20% of it?")
    ]
})

print(result["messages"][-1].content)
     
