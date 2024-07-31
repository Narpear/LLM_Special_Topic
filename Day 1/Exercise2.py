import streamlit as st
from transformers import pipeline

st.title("Sentiment analysis application")

sentiment_pipeline = pipeline("sentiment-analysis")

user_input = st.text_input("Write your text here")

if user_input:
    result = sentiment_pipeline(user_input)[0]
    sentiment = result["label"]
    score = result["score"]

    st.write(f"Sentiment: {sentiment}")
    st.write(f"Confidence: {score:.2f}")
