import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import json
import amadeus_client

# Initialize Langchain components
template = """Question: {question}

Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)
model = Ollama(model="llama3")
chain = prompt | model

def process_query(user_query):
    our_prompt = """
    i have this following class with two functions
    import amadeus

    def get_flight_offers(self, origin, destination, departure_date, n_adults):
        response = self.amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            adults=n_adults
        )
        return response.data

    def get_hotel_by_city(self, city_code):
        response = self.amadeus.reference_data.locations.hotels.by_city.get(cityCode=city_code)
        return response.data

    (dates in YYYY-MM-DD format)
    based on the function definitions, can you pick the function definition that matches the user query that I am going to give, give the function call for it according to the information in the query? (do not give  ANY explanations, just the function call). You **must** give the response in JSON format where there are two different objects, one for hotels and the other for flights.
    For example:
    {
    "task": "get_flight_offers",
    "params": {
    "origin": "JFK",
    "destination": "LAX",
    "departure_date": "2024-11-11",
    "n_adults": 1
    }
    }
    """

    response = chain.invoke({"question": our_prompt + user_query})
    return json.loads(response)

def get_result(data):
    if data['task'] == 'get_flight_offers':
        origin = data['params']['origin']
        destination = data['params']['destination']
        departure_date = data['params']['departure_date']
        n_adults = data['params']['n_adults']
        flight_data = amadeus_client.getting_flight_offers(origin=origin, destination=destination, departure_date=departure_date, n_adults=n_adults)
        return flight_data
    else:
        city_code = data['params']['city_code']
        hotel_data = amadeus_client.getting_hotels(city_code=city_code)
        return hotel_data

def format_result(user_query, result):
    our_prompt2 = f"""I have provided to you with user question and the JSON answer. Can you present it in a human readable natural language format with only the important information
    : User question: {user_query}. Result: {result}. Can you give the answer in human understandable format?"""
    response2 = chain.invoke({"question": our_prompt2})
    return response2

# Streamlit UI
st.title("Travel Search")

user_query = st.text_input("Search for hotels or flights:", "")

if st.button("Search"):
    if user_query:
        with st.spinner("Processing your request..."):
            # Process the query
            data = process_query(user_query)
            
            # Get the result
            result = get_result(data)
            
            # Format the result
            formatted_result = format_result(user_query, result)
            
            # Display the result
            st.subheader("Search Results:")
            st.write(formatted_result)
    else:
        st.warning("Please enter a search query.")

