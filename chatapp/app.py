import streamlit as st
from inference import ask_question

# App Layout and Sidebar
st.set_page_config(page_title="VQA Chat", layout="wide")

st.sidebar.title("VQA Chat Settings")
st.sidebar.write("Ask questions about various objects in a conversational format.")

st.title("VQA Chat Assistant")
st.markdown("""
    <style>
        .chat-container {
            border: 1px solid #e0e0e0;
            padding: 15px;
            background-color: #f3f3f3;
            border-radius: 8px;
            max-width: 750px;
            margin: 20px auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .user-message, .bot-message {
            padding: 10px 15px;
            border-radius: 12px;
            max-width: 80%;
            width: fit-content;
            font-size: 1rem;
            line-height: 1.5;
        }
        .user-message {
            background-color: #dcf8c6; /* Light green for user message */
            align-self: flex-end;
            color: #333;
            box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1);
        }
        .bot-message {
            background-color: #ffffff; /* White for bot message */
            border: 1px solid #e0e0e0;
            align-self: flex-start;
            color: #000;
            box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Display chat history
for message in st.session_state["chat_history"]:
    message_class = "user-message" if message["role"] == "user" else "bot-message"
    st.markdown(
        f'<div class="chat-container"><div class="{message_class}">{message["content"]}</div></div>',
        unsafe_allow_html=True,
    )

# User input form
with st.form("chat_form", clear_on_submit=True):
    question = st.text_input("Ask a question")
    object_name = st.text_input("Optional object name/context")
    submitted = st.form_submit_button("Send")

# Generate response
if submitted and question:
    st.session_state["chat_history"].append({"role": "user", "content": question})
    try:
        answer = ask_question(question, object_name)
        st.session_state["chat_history"].append({"role": "bot", "content": answer})
    except Exception as e:
        st.error(f"An error occurred: {e}")
    st.rerun()
