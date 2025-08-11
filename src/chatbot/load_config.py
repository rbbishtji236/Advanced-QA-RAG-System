
import os
import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from pyprojroot import here

def _to_bool(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() in {"1", "true", "yes", "on"}
    return bool(v)

@dataclass
class ProjectConfig:
    tracing: bool
    project_name: str
    memory_dir: Path
    search_provider: str = "ddg"  # 'ddg' or 'tavily'

class LoadProjectConfig:
    def __init__(self, cfg_path: str = "configs/project_config.yml") -> None:
        load_dotenv()

        with open(here(cfg_path)) as cfg:
            raw = yaml.safe_load(cfg) or {}

        langsmith = raw.get("langsmith", {})
        memory = raw.get("memory", {})
        misc = raw.get("misc", {}) 

        self.config = ProjectConfig(
            tracing=_to_bool(langsmith.get("tracing", False)),
            project_name=str(langsmith.get("project_name", "local-dev")),
            memory_dir=Path(here(memory.get("directory", "data/memory"))),
            search_provider=(misc.get("search_provider") or os.getenv("SEARCH_PROVIDER", "ddg")).lower(),
        )

        os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
        if self.config.tracing and os.environ["LANGCHAIN_API_KEY"]:
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_PROJECT"] = self.config.project_name
        else:
            os.environ["LANGCHAIN_TRACING_V2"] = "false"
            os.environ.pop("LANGCHAIN_PROJECT", None)

        self.config.memory_dir.mkdir(parents=True, exist_ok=True)

        os.environ["SEARCH_PROVIDER"] = self.config.search_provider

        os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    @property
    def memory_dir(self) -> Path:
        return self.config.memory_dir

    @property
    def tracing(self) -> bool:
        return self.config.tracing

    @property
    def project_name(self) -> str:
        return self.config.project_name

    @property
    def search_provider(self) -> str:
        return self.config.search_provider
