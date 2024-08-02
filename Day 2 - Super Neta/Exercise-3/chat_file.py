from model import chat_groq
from langchain_core.prompts import PromptTemplate
import sqlite3
from langchain_core.output_parsers import StrOutputParser


def create_connection(db_file):
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error creating connection to database: {e}")
    return conn


def sql_query(question, table_schema):
    model = chat_groq()
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
            Generate a SQL query for the following question:
            {question}
            User has provide the table schema
            The output should only contain the SQL query
            remember the name of the table is election_results
            <|eot_id|><|start_header_id|>user<|end_header_id>
            Here is the table schema: {table}
            <|eot_id|><|start_header_id|>assistant<|end_header_id>
            """, input_variables=["question", "table"]
    )

    rag_chain = prompt | model | StrOutputParser()
    response = rag_chain.invoke(
        input={"question": question, "table": table_schema})
    print(response)
    return response


async def chat(question, table_schema, message_placeholder):
    message_placeholder.markdown("Generating SQL...")
    model = chat_groq()
    sql = sql_query(question, table_schema)
    table_conection = create_connection('election_results.db')
    cursor = table_conection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    message_placeholder.markdown("Generating Response...")
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
            User has provided question
            Answer the query using the result from the context {result}
            <|eot_id|><|start_header_id|>user<|end_header_id>
            Here is the user question : {question}
            <|eot_id|><|start_header_id|>assistant<|end_header_id>
            """, input_variables=["result", "question"]
    )

    rag_chain = prompt | model | StrOutputParser()

    response = ""
    async for part in rag_chain.astream(input={"result": result, "question": question}):
        response += part
        message_placeholder.markdown(response)
    return response
