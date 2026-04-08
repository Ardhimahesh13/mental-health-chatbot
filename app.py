import streamlit as st
from backend.gemini_client import GeminiClient
from backend.memory import ConversationMemory
from prompts.system_prompt import SYSTEM_PROMPT
from utils.fallback import get_fallback_response
from utils.formatter import format_response

# Initialize
st.set_page_config(page_title='Mental Health chatbot', layout="centered")
st.title('🧠 Mental Health Support Assistant')
st.caption("You're not alone. I'm here to listen and support you.")

if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory()

if "chat" not in st.session_state:
    st.session_state.chat = GeminiClient()

# Display history
for msg in st.session_state.memory.get_history():
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
user_input = st.chat_input("How are you feeling today?")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.memory.add_message("user", user_input)

    # Build full prompt with history
    history = st.session_state.memory.get_history()[-6:]
    full_prompt = f"{SYSTEM_PROMPT}\n\nConversation:\n"

    for msg in history:
        full_prompt += f"{msg['role']}: {msg['content']}\n"

    # Get response
    try:
        with st.spinner("Thinking..."):
            response = st.session_state.chat.get_response(full_prompt)

        if response is None or response.strip() == "":
            response = get_fallback_response()

    except Exception:
        response = get_fallback_response()
    response = format_response(response)

    # Show bot response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.memory.add_message("assistant", response)
