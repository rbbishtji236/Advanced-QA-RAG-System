import os
import yaml
from typing import Optional

from dotenv import load_dotenv
from pyprojroot import here

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings as HFEmbeddings

load_dotenv(here(".env"), override=True)



class LoadToolsConfig:
    """
    Central place to read tool config AND return ready-to-use
    LLM / Embedding instances (no OpenAI hardcoding).
    """

    def __init__(self) -> None:
        with open(here("configs/tools_config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key
        tavily_key = os.getenv("TAVILY_API_KEY")
        if tavily_key:
            os.environ["TAVILY_API_KEY"] = tavily_key

        
        pa = app_config["primary_agent"]
        self.primary_agent_provider: str = pa.get("provider", "groq")
        self.primary_agent_llm_name: str = pa["llm"]                      # e.g., "llama-3.1-70b-versatile"
        self.primary_agent_llm_temperature: float = float(pa.get("llm_temperature", 0.0))

       
        self.tavily_search_max_results: int = int(
            app_config["tavily_search_api"]["tavily_search_max_results"]
        )

        
        pol = app_config["swiss_airline_policy_rag"]
        self.policy_rag_llm: str = pol.get("llm", "default")
        self.policy_rag_llm_temperature: float = float(pol.get("llm_temperature", 0.0))
        self.policy_rag_embedding_model: str = pol["embedding_model"]     # HF model name
        self.policy_rag_vectordb_directory: str = str(here(pol["vectordb"]))
        self.policy_rag_unstructured_docs_directory: str = str(here(pol["unstructured_docs"]))
        self.policy_rag_k: int = int(pol["k"])
        self.policy_rag_chunk_size: int = int(pol["chunk_size"])
        self.policy_rag_chunk_overlap: int = int(pol["chunk_overlap"])
        self.policy_rag_collection_name: str = pol["collection_name"]

        
        st = app_config["stories_rag"]
        self.stories_rag_llm: str = st.get("llm", "default")
        self.stories_rag_llm_temperature: float = float(st.get("llm_temperature", 0.0))
        self.stories_rag_embedding_model: str = st["embedding_model"]     # HF model name
        self.stories_rag_vectordb_directory: str = str(here(st["vectordb"]))
        self.stories_rag_unstructured_docs_directory: str = str(here(st["unstructured_docs"]))
        self.stories_rag_k: int = int(st["k"])
        self.stories_rag_chunk_size: int = int(st["chunk_size"])
        self.stories_rag_chunk_overlap: int = int(st["chunk_overlap"])
        self.stories_rag_collection_name: str = st["collection_name"]

        
        tsa = app_config["travel_sqlagent_configs"]
        self.travel_sqldb_directory: str = str(here(tsa["travel_sqldb_dir"]))
        self.travel_sqlagent_llm: str = tsa.get("llm", "default")
        self.travel_sqlagent_llm_temperature: float = float(tsa.get("llm_temperature", 0.0))

        csa = app_config["chinook_sqlagent_configs"]
        self.chinook_sqldb_directory: str = str(here(csa["chinook_sqldb_dir"]))
        self.chinook_sqlagent_llm: str = csa.get("llm", "default")
        self.chinook_sqlagent_llm_temperature: float = float(csa.get("llm_temperature", 0.0))

        
        self.thread_id: str = str(app_config["graph_configs"]["thread_id"])


    def _make_chat_model(self, provider: str, model_name: str, temperature: float = 0.0):
        provider = provider.lower()
        if provider == "groq":
            return ChatGroq(model=model_name, temperature=temperature)
        raise ValueError(f"Unsupported chat provider: {provider}")

    def get_primary_llm(self):
        return self._make_chat_model(
            provider=self.primary_agent_provider,
            model_name=self.primary_agent_llm_name,
            temperature=self.primary_agent_llm_temperature,
        )

    def get_llm(self, section_key: str, temperature: Optional[float] = None):
        
        temp = self.primary_agent_llm_temperature if temperature is None else temperature
        return self._make_chat_model(
            provider=self.primary_agent_provider,
            model_name=self.primary_agent_llm_name,
            temperature=temp,
        )

    def _make_hf_embedder(self, model_name: str):
        return HFEmbeddings(model_name=model_name, encode_kwargs={"normalize_embeddings": True})

    def get_embedding_for_policy(self):
        return self._make_hf_embedder(self.policy_rag_embedding_model)

    def get_embedding_for_stories(self):
        return self._make_hf_embedder(self.stories_rag_embedding_model)
