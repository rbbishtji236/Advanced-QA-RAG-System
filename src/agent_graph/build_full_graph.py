from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from agent_graph.tool_chinook_sqlagent import query_chinook_sqldb
from agent_graph.tool_travel_sqlagent import query_travel_sqldb
from agent_graph.tool_lookup_policy_rag import lookup_swiss_airline_policy
from agent_graph.tool_tavily_search import load_tavily_search_tool
from agent_graph.tool_stories_rag import lookup_stories
from agent_graph.load_tools_config import LoadToolsConfig
from agent_graph.agent_backend import State, BasicToolNode, route_tools, plot_agent_schema
import os
from langchain_groq import ChatGroq

TOOLS_CFG = LoadToolsConfig()


def build_graph():
    
    primary_llm = TOOLS_CFG.get_primary_llm() 
    graph_builder = StateGraph(State)
    search_tool = load_tavily_search_tool(TOOLS_CFG.tavily_search_max_results)
    tools = [search_tool,
             lookup_swiss_airline_policy,
             lookup_stories,
             query_travel_sqldb,
             query_chinook_sqldb,
             ]
    primary_llm_with_tools = primary_llm.bind_tools(tools)

    def chatbot(state: State):
        """Executes the primary language model with tools bound and returns the generated message."""
        return {"messages": [primary_llm_with_tools.invoke(state["messages"])]}

    graph_builder.add_node("chatbot", chatbot)
    tool_node = BasicToolNode(
        tools=[
            search_tool,
            lookup_swiss_airline_policy,
            lookup_stories,
            query_travel_sqldb,
            query_chinook_sqldb,
        ])
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_conditional_edges(
        "chatbot",
        route_tools,
  
        {"tools": "tools", "__end__": "__end__"},
    )

    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge(START, "chatbot")
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    plot_agent_schema(graph)
    return graph
