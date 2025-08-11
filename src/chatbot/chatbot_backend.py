

from __future__ import annotations
from typing import List, Tuple
from pathlib import Path

from chatbot.load_config import LoadProjectConfig
from agent_graph.load_tools_config import LoadToolsConfig
from agent_graph.build_full_graph import build_graph
from utils.app_utils import create_directory
from chatbot.memory import Memory

PROJECT_CFG = LoadProjectConfig()
TOOLS_CFG = LoadToolsConfig()

create_directory(str(PROJECT_CFG.memory_dir))

_GRAPH = None
def _ensure_graph():
    global _GRAPH
    if _GRAPH is None:
        _GRAPH = build_graph()
    return _GRAPH


class ChatBot:
    @staticmethod
    def respond(chatbot: List[Tuple[str, str]], message: str) -> Tuple[str, List[Tuple[str, str]]]:
        if not message:
            return "", chatbot

        graph = _ensure_graph()
        cfg = {"configurable": {"thread_id": TOOLS_CFG.thread_id}}

        last_event = None
        for event in graph.stream({"messages": [("user", message)]}, cfg, stream_mode="values"):
            last_event = event
            try:
                last_event["messages"][-1].pretty_print()
            except Exception:
                pass

        bot_text = (
            last_event["messages"][-1].content
            if last_event and last_event.get("messages")
            else "Sorry, I couldn't generate a response."
        )

        chatbot.append((message, bot_text))


        try:
            Memory.write_chat_history_to_file(
                gradio_chatbot=chatbot,
                folder_path=str(PROJECT_CFG.memory_dir),
                thread_id=TOOLS_CFG.thread_id,
            )
        except Exception as e:
            print(f"[warn] memory write failed: {e}")

        return "", chatbot
