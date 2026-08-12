from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from config_loader import load_config
from tool.tool1 import database_tools


# Load environment variables
load_dotenv()


# Load YAML configuration
config = load_config()


# --------------------------------------------------
# Read configuration
# --------------------------------------------------

agent_config = config["agent"]

model_config = agent_config["model"]
runtime_config = agent_config["runtime"]
memory_config = agent_config["memory"]


# --------------------------------------------------
# Create LLM
# --------------------------------------------------

llm = ChatOpenAI(
    model=model_config["name"],
    temperature=runtime_config["temperature"],
    base_url=model_config["base_url"],
    api_key=model_config["api_key"],
)


# --------------------------------------------------
# Load prompt dynamically
# --------------------------------------------------

import importlib


prompt_config = agent_config["prompt"]

prompt_module = importlib.import_module(
    prompt_config["module"]
)

prompt1 = getattr(
    prompt_module,
    prompt_config["variable"]
)


# --------------------------------------------------
# Create checkpointer
# --------------------------------------------------

checkpointer = None

if memory_config["enabled"]:

    if memory_config["type"] == "in_memory":
        checkpointer = InMemorySaver()


# --------------------------------------------------
# Create SQL Agent
# --------------------------------------------------

agent_kwargs = {
    "model": llm,
    "system_prompt": prompt1,
    "tools": database_tools,
}


if checkpointer is not None:
    agent_kwargs["checkpointer"] = checkpointer


agent = create_agent(**agent_kwargs)


# --------------------------------------------------
# Invoke Agent
# --------------------------------------------------

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    ""
                ),
            }
        ]
    },
    config={
        "configurable": {
            "thread_id": "sql-user-001"
        }
    },
)


# --------------------------------------------------
# Get final response
# --------------------------------------------------

result_text = result["messages"][-1].content

print(result_text)