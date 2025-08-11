from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from agent_graph.load_tools_config import LoadToolsConfig

TOOLS_CFG = LoadToolsConfig()


class TravelSQLAgentTool:
    """
    SQL QA over the travel SQLite DB using the configured chat model (no OpenAI).
    """

    def __init__(self) -> None:
        self.sql_agent_llm = TOOLS_CFG._make_chat_model( 
            provider=TOOLS_CFG.primary_agent_provider,
            model_name=TOOLS_CFG.travel_sqlagent_llm,
            temperature=TOOLS_CFG.travel_sqlagent_llm_temperature,
        )

        self.system_role = (
            "Given the following user question, corresponding SQL query, and SQL result, "
            "answer the user question.\n\n"
            "Question: {question}\n"
            "SQL Query: {query}\n"
            "SQL Result: {result}\n"
            "Answer:"
        )

        self.db = SQLDatabase.from_uri(f"sqlite:///{TOOLS_CFG.travel_sqldb_directory}")
        print(self.db.get_usable_table_names())

        execute_query = QuerySQLDataBaseTool(db=self.db)
        write_query = create_sql_query_chain(self.sql_agent_llm, self.db)
        answer_prompt = PromptTemplate.from_template(self.system_role)

        answer = answer_prompt | self.sql_agent_llm | StrOutputParser()
        self.chain = (
            RunnablePassthrough.assign(query=write_query)
            .assign(result=itemgetter("query") | execute_query)
            | answer
        )


@tool
def query_travel_sqldb(query: str) -> str:
    """Query the Swiss Airline SQL Database and access all the company's information. Input should be a search query."""
    agent = TravelSQLAgentTool()
    return agent.chain.invoke({"question": query})