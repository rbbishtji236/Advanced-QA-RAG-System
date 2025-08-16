from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
try:
    from langchain_community.tools.sql_database import QuerySQLDatabaseTool
except Exception:
    from langchain_community.tools.sql_database.tool import (
        QuerySQLDataBaseTool as QuerySQLDatabaseTool
    )
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
import re
from agent_graph.load_tools_config import LoadToolsConfig

TOOLS_CFG = LoadToolsConfig()


def _looks_like_sql(text: str) -> bool:
    return bool(re.match(r"(?is)^\s*(select|with|pragma|explain)\b", text or ""))


class TravelSQLAgentTool:

    def __init__(self) -> None:
        self.sql_agent_llm = TOOLS_CFG._make_chat_model( 
            provider=TOOLS_CFG.primary_agent_provider,
            model_name=TOOLS_CFG.travel_sqlagent_llm,
            temperature=TOOLS_CFG.travel_sqlagent_llm_temperature,
        )

        self.system_role = (
            "Given the following user question, corresponding SQL query, and SQL result,\n "
            "Answer the question as briefly as possible using only the result; do not explain the SQL"
            "or include extra commentary. If the result is a single column of strings, return a "
            "comma-separated list. If it's a count/aggregate, return just the value."
            "\n\nQuestion: {question}\n"
            "SQL Query: {query}\n"
            "SQL Result: {result}\n"
            "Answer:"
        )

        self.db = SQLDatabase.from_uri(f"sqlite:///{TOOLS_CFG.travel_sqldb_directory}",
                                       sample_rows_in_table_info=0)
        print(self.db.get_usable_table_names())

        self.execute_query = QuerySQLDatabaseTool(db=self.db)
        self.write_query = create_sql_query_chain(self.sql_agent_llm,self.db)
        answer_prompt = PromptTemplate.from_template(self.system_role)

        self.answer = answer_prompt | self.sql_agent_llm | StrOutputParser()
        self.generated_chain = (
            RunnablePassthrough.assign(query=self.write_query)
            .assign(result=itemgetter("query") | self.execute_query)
            | self.answer
        )

        self.direct_sql_chain = (
            RunnablePassthrough.assign(query=lambda x: x["question"])
            .assign(result=itemgetter("query") | self.execute_query)
            | self.answer
        )
    def run(self, question: str) -> str:
        if _looks_like_sql(question):
            sql = question.strip()
            low = sql.lower()
            if not (low.startswith("select") or low.startswith("with") or low.startswith("pragma") or low.startswith("explain")):
                raise ValueError("Only SELECT/WITH/PRAGMA/EXPLAIN are allowed.")
            return self.direct_sql_chain.invoke({"question": sql})
        else:
            return self.generated_chain.invoke({"question": question})


@tool
def query_travel_sqldb(query: str) -> str:
    """Query the Swiss Airline SQL Database and access all the company's information. Input should be a search query."""
    agent = TravelSQLAgentTool()
    return agent.run(query)