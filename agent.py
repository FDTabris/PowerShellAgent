import json
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langchain import hub  # To pull react prompt
from langchain.agents import create_react_agent, AgentExecutor

# In-memory store for todos
todos = []

# Tool implementations
@tool
def add_todo_item(item: str) -> str:
    """
    Add a new todo item to the list.
    Input: free-text description of the task.
    """
    todos.append(item)
    return f"Added todo: '{item}'"

@tool
def list_todos(_: None = None) -> str:
    """
    Return all current todo items, numbered.
    """
    if not todos:
        return "No todos yet."
    return "\n".join(f"{i+1}. {todo}" for i, todo in enumerate(todos))

@tool
def remove_todo_item(index: str) -> str:
    """
    Remove a todo by its 1-based index.
    Input: index as string or integer.
    """
    try:
        idx = int(index)
        removed = todos.pop(idx - 1)
        return f"Removed todo: '{removed}'"
    except (ValueError, IndexError):
        return "Invalid index. Please provide a valid number."

# List of tools
tools = [add_todo_item, list_todos, remove_todo_item]

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

endpoint = config.get("endpoint")
# model_name = config.get("model_name")
deployment = config.get("deployment")

subscription_key = config.get("subscription_key")
api_version = config.get("api_version")

# Initialize Azure-backed LLM
llm = AzureChatOpenAI(
    azure_deployment= deployment,
    openai_api_version=api_version,
    temperature=1.0,
    api_key=subscription_key,
    azure_endpoint=endpoint,
)

# Get the ReAct prompt
prompt = hub.pull("hwchase17/react")    # Pull the ReAct prompt from LangChain Hub (https://smith.langchain.com/hub/hwchase17/react)

# Create the ReAct agent
agent = create_react_agent(llm, tools, prompt)

# Create an agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Simple REPL demo
if __name__ == "__main__":
    print("Welcome to your ReAct Todo Agent! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Agent: Goodbye! 👋")
            break
        # Use invoke on the executor
        result = agent_executor.invoke({"input": user_input})
        print(f"Agent: {result['output']}\n")
