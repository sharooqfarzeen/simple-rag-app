"""Streamlit UI for RAG Server"""
import streamlit as st
import requests
import os

# Define the base URL for the FastAPI server
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")

st.title("Simple RAG AI")

# File Ingestion
st.header("1. Ingest a document")
uploaded_file = st.file_uploader("Choose a file to ingest", type=["pdf", "txt", "md"])

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    with st.spinner("Ingesting document..."):
        try:
            response = requests.post(f"{FASTAPI_URL}/ingest", files=files)
            if response.status_code == 200:
                st.success("Document ingested successfully!")
            else:
                st.error(f"Error during ingestion: {response.text}")
        except requests.exceptions.ConnectionError as e:
            st.error(f"Could not connect to the RAG server. Please ensure it is running. Details: {e}")


# Retrieval
st.header("2. Retrieve information")
query = st.text_input("Enter your query")

if st.button("Retrieve"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Retrieving information..."):
            try:
                response = requests.get(f"{FASTAPI_URL}/retrieve", params={"query": query})
                if response.status_code == 200:
                    st.success("Information retrieved successfully!")
                    st.write(response.json()["answer"])
                else:
                    st.error(f"Error during retrieval: {response.text}")
            except requests.exceptions.ConnectionError as e:
                st.error(f"Could not connect to the RAG server. Please ensure it is running. Details: {e}")
