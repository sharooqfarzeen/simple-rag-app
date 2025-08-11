import streamlit as st
import requests

# Define the base URL for the FastAPI backend
API_URL = "http://127.0.0.1:8000"

def main():
    # Streamlit app
    st.set_page_config(page_title="Chat with PDF")

    st.title("Chat with your PDF")

    # Initializing chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    # Track if a file has been uploaded
    if "file_uploaded" not in st.session_state:
        st.session_state["file_uploaded"] = False

    # Display chat messages from history on app rerun
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Sidebar for file upload
    with st.sidebar:
        st.header("File Upload")
        uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])
        if st.button("Upload and Process"):
            if uploaded_file:
                with st.spinner("Processing File..."):
                    files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    try:
                        response = requests.post(f"{API_URL}/ingest", files=files)
                        if response.status_code == 200:
                            st.session_state.file_uploaded = True
                            st.success("File uploaded and processed successfully!")
                            st.session_state.messages.append({"role": "assistant", "content": "File uploaded. You can now ask questions."})
                            # This will rerun the script and update the chat
                            st.rerun()
                        else:
                            st.error(f"Error processing file: {response.text}")
                    except requests.exceptions.ConnectionError as e:
                        st.error(f"Could not connect to the server. Please make sure the backend is running. Details: {e}")
            else:
                st.warning("Please upload a PDF file.")

    # Main chat interface
    user_question = st.chat_input("Ask a question about your document.")

    if user_question:
        st.chat_message("user").markdown(user_question)
        st.session_state.messages.append({"role": "user", "content": user_question})

        if not st.session_state.file_uploaded:
            with st.chat_message("assistant"):
                st.markdown("Please upload a document first.")
            st.session_state.messages.append({"role": "assistant", "content": "Please upload a document first."})
        else:
            with st.spinner("Thinking..."):
                try:
                    response = requests.get(f"{API_URL}/retrieve", params={"query": user_question})
                    if response.status_code == 200:
                        answer = response.json().get("answer", "No answer found.")
                        with st.chat_message("assistant"):
                            st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error(f"Error retrieving answer: {response.text}")
                except requests.exceptions.ConnectionError as e:
                    st.error(f"Could not connect to the server. Please make sure the backend is running. Details: {e}")

if __name__ == "__main__":
    main()