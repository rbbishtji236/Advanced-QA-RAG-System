from operator import itemgetter
import re
from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

from agent_graph.load_tools_config import LoadToolsConfig

TOOLS_CFG = LoadToolsConfig()


def _extract_sql(text: str) -> str:
    # Prefer fenced SQL first
    m = re.search(r"```sql\s*(.*?)```", text, flags=re.IGNORECASE|re.DOTALL)
    if m:
        return m.group(1).strip()
    # Else, grab first SELECT/WITH... up to semicolon
    m = re.search(r"\b(SELECT|WITH)\b.*?;", text, flags=re.IGNORECASE|re.DOTALL)
    if m:
        return m.group(0).strip()
    # Last resort, return trimmed text
    return text.strip()


class ChinookSQLAgent:

    def __init__(self, sqldb_directory: str, llm_temperature: float = 0.0):
      
        self.sql_agent_llm = TOOLS_CFG.get_llm("chinook_sqlagent_configs", temperature=llm_temperature)

       
        self.db = SQLDatabase.from_uri(f"sqlite:///{sqldb_directory}")

       
        write_query = create_sql_query_chain(self.sql_agent_llm, self.db)

       
        execute_query = QuerySQLDataBaseTool(db=self.db) 

       
        self.chain = (
            RunnablePassthrough.assign(query=write_query)
            .assign(result=itemgetter("query") | execute_query)
            | (lambda d: d["result"])
        )


@tool
def query_chinook_sqldb(query: str) -> str:
    """Query the Chinook SQLite database. Input should be a natural-language question."""
    agent = ChinookSQLAgent(
        sqldb_directory=TOOLS_CFG.chinook_sqldb_directory,
        
        llm_temperature=TOOLS_CFG.chinook_sqlagent_llm_temperature,
    )
    llm_text=agent.chain.invoke({"question": query})
    sql = _extract_sql(llm_text)
    if not sql.lstrip().upper().startswith(("SELECT", "WITH")):
        return f"Refusing to execute non-SELECT SQL.\nParsed text:\n{sql}"

    executor = QuerySQLDataBaseTool(db=agent.db)
    try:
        return executor.invoke({"query": sql})
    except Exception as e:
        return f"SQL failed.\nSQL:\n{sql}\nError: {e}"
