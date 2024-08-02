import asyncio
import streamlit as st
from model import chat_groq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import sqlite3
import pandas as pd
from chat_file import chat

# Function to create a connection to the SQLite database


def create_connection(db_file):
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        st.error(f"Error creating connection to database: {e}")
    return conn

# Function to get the table schema from the database


def get_table_schema(conn, table_name):
    """Retrieve table schema from the SQLite database"""
    query = f"PRAGMA table_info({table_name})"
    cursor = conn.cursor()
    cursor.execute(query)
    schema = cursor.fetchall()
    return schema


# Streamlit app setup
if "messages" not in st.session_state:
    st.session_state.messages = []

if "db_conn" not in st.session_state:
    st.session_state.db_conn = create_connection('election_results.db')

if "table_schema" not in st.session_state:
    if st.session_state.db_conn:
        st.session_state.table_schema = get_table_schema(
            st.session_state.db_conn, "election_results")
    else:
        st.session_state.table_schema = None

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to handle user input and chat response


async def handle_user_input(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = await chat(prompt, st.session_state.table_schema, message_placeholder)
        message_placeholder.markdown(response)
    st.session_state.messages.append(
        {"role": "assistant", "content": response})


def main():
    if st.session_state.table_schema:
        st.write("Table Schema:")
        for column in st.session_state.table_schema:
            st.write(column)
    else:
        st.write("Table schema not available.")

    if prompt := st.chat_input("What is up?"):
        asyncio.run(handle_user_input(prompt))


if __name__ == "__main__":
    main()
