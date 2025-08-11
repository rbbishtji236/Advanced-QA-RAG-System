# agent_graph/tool_stories_rag.py  (OpenAI -> HF embeddings via config)

from langchain_chroma import Chroma
from langchain_core.tools import tool
from agent_graph.load_tools_config import LoadToolsConfig

TOOLS_CFG = LoadToolsConfig()

class StoriesRAGTool:
    def __init__(self) -> None:
        # Hugging Face embedder (e.g., BAAI/bge-*)
        self.embeddings = TOOLS_CFG.get_embedding_for_stories()

        self.vectordb = Chroma(
            collection_name=TOOLS_CFG.stories_rag_collection_name,
            persist_directory=TOOLS_CFG.stories_rag_vectordb_directory,
            embedding_function=self.embeddings,
        )
        self.k = TOOLS_CFG.stories_rag_k
        try:
            print("Number of vectors in vectordb:", self.vectordb._collection.count(), "\n")
        except Exception:
            pass

    def search(self, query: str):
        return self.vectordb.similarity_search(query, k=self.k)

@tool
def lookup_stories(query: str) -> str:
    """Search among the fictional stories and find the answer to the query. Input should be the query."""
    rag_tool = StoriesRAGTool()
    docs = rag_tool.search(query)
    if not docs:
        return "No matching story snippets found."
    return "\n\n".join(doc.page_content for doc in docs)
