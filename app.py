import streamlit as st
from openai import OpenAI

# ----------------------------
# Load API key from Streamlit secrets
# ----------------------------
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("API key not found in Streamlit secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Student Assistant Bot",
    page_icon="📚",
    layout="wide"
)

# ----------------------------
# Language Selector
# ----------------------------
language = st.selectbox(
    "🌐 Choose language / Choisissez la langue / Safidio ny fiteny",
    ["English", "French", "Malagasy"]
)

# ----------------------------
# Multilingual interface text
# ----------------------------
if language == "English":
    title_text = "📚 Student Assistant Bot"
    description_text = "Ask questions about Physics, Maths, and Natural Science!"
    input_placeholder = "Type your question here..."
    footer_text = "Created by Milanto | + OpenAI API"
elif language == "French":
    title_text = "📚 Assistant Étudiant"
    description_text = "Posez des questions sur la Physique, les Maths et les Sciences Naturelles !"
    input_placeholder = "Tapez votre question ici..."
    footer_text = "Créé par Milanto | + OpenAI API"
else:  # Malagasy
    title_text = "📚 Mpanampy Mpianatra"
    description_text = "Manontania momba ny Fisika, Matematika, ary Siansa voajanahary!"
    input_placeholder = "Soraty eto ny fanontanianao..."
    footer_text = "Noforonin'i Milanto | + OpenAI API"

# ----------------------------
# Page Title
# ----------------------------
st.markdown(f"<h1 style='text-align:center; color:#4B0082;'>{title_text}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#555;'>{description_text}</p>", unsafe_allow_html=True)
st.markdown("---")

# ----------------------------
# Chat History Initialization
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                f"You are a friendly high school teacher. "
                f"Answer questions about Physics, Maths, and Natural Science. "
                f"Always answer in {language}. Explain clearly and step by step."
            )
        }
    ]

# ----------------------------
# Display Chat History
# ----------------------------
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages[1:]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Bot:** {msg['content']}")

# ----------------------------
# User Input Box
# ----------------------------
user_input = st.text_input(input_placeholder, key="input_box")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        # Update system prompt with current language
        st.session_state.messages[0]["content"] = (
            f"You are a friendly high school teacher. "
            f"Answer questions about Physics, Maths, and Natural Science. "
            f"Always answer in {language}. Explain clearly and step by step."
        )

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            temperature=0.4
        )

    bot_reply = response.choices[0].message.content

    # Append bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # Refresh chat container
    chat_container.empty()
    with chat_container:
        for msg in st.session_state.messages[1:]:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**Bot:** {msg['content']}")

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown(f"<p style='text-align:center; color:#888;'>{footer_text}</p>", unsafe_allow_html=True)
