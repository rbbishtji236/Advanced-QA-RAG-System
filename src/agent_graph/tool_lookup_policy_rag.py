from langchain_chroma import Chroma
from langchain_core.tools import tool
from agent_graph.load_tools_config import LoadToolsConfig

TOOLS_CFG = LoadToolsConfig()

class SwissAirlinePolicyRAGTool:

    def __init__(self) -> None:
        # HF - BAAI/bge-small-en-v1.5
        self.embeddings = TOOLS_CFG.get_embedding_for_policy()

        self.vectordb = Chroma(
            collection_name=TOOLS_CFG.policy_rag_collection_name,
            persist_directory=TOOLS_CFG.policy_rag_vectordb_directory,
            embedding_function=self.embeddings,
        )
        self.k = TOOLS_CFG.policy_rag_k
        try:
            print("Number of vectors in vectordb:", self.vectordb._collection.count(), "\n")
        except Exception:
            pass
    def search(self, query: str):
        return self.vectordb.similarity_search(query, k=self.k)

@tool
def lookup_swiss_airline_policy(query: str) -> str:
    """Consult the company policies to check whether certain options are permitted."""
    rag= SwissAirlinePolicyRAGTool()
    docs=rag.search(query)
    if not docs:
        return "No relevant policy found for the query."
    return "\n\n".join([doc.page_content for doc in docs])
