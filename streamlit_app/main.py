import streamlit as st
import requests

st.title("Chatbot with RAG")

st.sidebar.header("User Input")
user_input = st.sidebar.text_area("Type your question here:", "")

if st.sidebar.button("Submit"):
    if not user_input.strip():
        st.error("Please provide a question.")
    else:
        try:
            response = requests.post(
                "http://localhost:5000/chat",
                json={"message": user_input}
            )
            if response.status_code == 200:
                st.success(response.json()["response"])
            else:
                st.error(response.json().get("error", "Unknown error"))
        except Exception as e:
            st.error(f"Failed to connect to backend: {str(e)}")
