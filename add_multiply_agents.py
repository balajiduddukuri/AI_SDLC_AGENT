from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature = 0
)

from langchain_core.tools import tool

@tool
def add_numbers(a: int, b: int) -> int:
  """Adds two Numbers"""
  return a + b

@tool
def multiply_numbers(a: int, b: int) -> int:
  """Multiply 2 nos."""
  return a * b


tools = [add_numbers, multiply_numbers]

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate(
    [(
    "system",
    """Answer the following questions as best you can.
You have access to the following tools.

Use the following format internally:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take
Action Input: the input to the action
Observation: the result of the action
(repeat as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
"""
  ),
  MessagesPlaceholder(variable_name = "messages"),
])

from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model = llm,
    tools = tools,
    prompt = prompt
)

result = agent.invoke({
    "messages":[
        ("user", "Add 5 and 7, then multiply it by 3, and then add it by 90")
    ]
})

print(result['messages'][-1].content)

from langchain_core.messages import ToolMessage

for msg in result['messages']:
  if isinstance(msg, ToolMessage):
    print(f"Tool Name: {msg.name}")
    print(f"Tool Output:  {msg.content}")
    print('-'*40)

