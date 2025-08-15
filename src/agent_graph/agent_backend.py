import json
from IPython.display import Image, display
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langchain_core.messages import ToolMessage
from langgraph.graph.message import add_messages
from langchain_core.tools import BaseTool
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from typing import Annotated, Literal, Sequence, Mapping, Any, Union, List, Dict

class State(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]


class BasicToolNode:
    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: Mapping[str, Any]) -> Dict[str, List[ToolMessage]]:
        messages: List[BaseMessage] = list(inputs.get("messages", []))
        if not messages:
            raise ValueError("No message found in input")

        message = messages[-1]

        if not isinstance(message, AIMessage) or not message.tool_calls:
            return {"messages": []}

        outputs: List[ToolMessage] = []
        for call in message.tool_calls:
            name = call.get("name")
            args = call.get("args", {})
            call_id = call.get("id")

            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
            
                    args = {"input": args}

            tool = self.tools_by_name.get(name or "")
            if tool is None:
                raise KeyError(f"Tool '{name}' not registered in BasicToolNode.")

            result = tool.invoke(args)

            content = result if isinstance(result, str) else json.dumps(result)
            outputs.append(
                ToolMessage(
                    content=content,
                    name=name or "",
                    tool_call_id=call_id,
                )
            )

        return {"messages": outputs}


def route_tools(state: State) -> Literal["tools", "__end__"]:
    messages = state.get("messages", [])
    if not messages:
        raise ValueError("No messages found in input state to tool_edge")

    last = messages[-1]
    if isinstance(last, AIMessage) and last.tool_calls:
        return "tools"
    return "__end__"


def plot_agent_schema(graph):
    try:
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception:
        return print("Graph could not be displayed.")
