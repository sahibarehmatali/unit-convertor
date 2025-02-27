import streamlit as st
import time
from google import genai


# Initialize GenAI client with API key
API_KEY = st.secrets["google_key"]
client = genai.Client(api_key=API_KEY)

# Custom CSS for a premium dark-glass UI with a floating chatbox
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #1f1c2c, #928dab);
            color: white;
            font-family: 'Poppins', sans-serif;
        }
        .stApp {
            background: transparent;
            padding: 30px;
        }
        .chat-container {
            max-width: 700px;
            margin: auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: fadeIn 0.5s ease-in-out;
        }
        .user-msg {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 12px;
            text-align: right;
            max-width: 75%;
            float: right;
            clear: both;
            animation: fadeIn 0.4s ease-in-out;
        }
        .ai-msg {
            background: rgba(255, 255, 255, 0.2);
            color: black;
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 12px;
            text-align: left;
            max-width: 75%;
            float: left;
            clear: both;
            animation: fadeIn 0.4s ease-in-out;
        }
        .chat-bubble {
            display: inline-block;
            animation: fadeIn 0.3s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0px); }
        }
        .title {
            text-align: center;
            color: blue;
            font-size: 38px;
            font-weight: bold;
            text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
        }
        .subtitle {
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            font-size: 18px;
            margin-bottom: 25px;
        }
        .chat-input {
            background: rgba(255, 255, 255, 0.1);
            color: black;
            border-radius: 10px;
            padding: 12px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# App title with a stylish glow effect
st.markdown("<h1 class='title'>🤖 AI-Powered Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='subtitle'>Your Intelligent AI Assistant</h4>", unsafe_allow_html=True)

# Initialize chat session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history inside a modern glassmorphic chat container
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "ai"
    msg_class = "user-msg" if role == "user" else "ai-msg"
    st.markdown(f"<div class='chat-bubble {msg_class}'>{message['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# User input field
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Append user message to session history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message instantly
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        with st.spinner("Thinking... 🤔"):
            # Simulate typing effect for a better UX
            time.sleep(1.5)

            # Generate AI response
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"you are a unit convertor. convert given values in a single one line answer on{user_input}"
            )

        ai_response = response.text if hasattr(response, "text") else "⚠️ No valid response received. Please try again."

        # Append AI response to session history
        st.session_state.messages.append({"role": "ai", "content": ai_response})

        # Display AI response with typing animation
        with st.chat_message("assistant"):
            typing_placeholder = st.empty()
            typed_text = ""
            for char in ai_response:
                typed_text += char
                typing_placeholder.markdown(typed_text)
                time.sleep(0.02)  # Typing speed effect

        # Refresh page to display messages instantly
        st.rerun()

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
