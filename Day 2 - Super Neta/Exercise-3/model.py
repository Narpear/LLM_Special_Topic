from langchain_groq import ChatGroq
from langchain_community.chat_models import ChatOllama
from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv
import os


def chat_groq():
    """
    Chat with the GROQ model.
    """
    load_dotenv()
    model = ChatGroq(model='llama3-70b-8192', temperature=0, verbose=True,
                     api_key=os.getenv('GROQ_API_KEY'))
    return model


def chatOllama():
    """
    Chat with the Ollama model.
    """
    model = ChatOllama(model='llama3', temperature=0, verbose=True,)
    return model


