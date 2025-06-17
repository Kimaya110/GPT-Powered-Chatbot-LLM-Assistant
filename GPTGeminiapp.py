import os
import streamlit as st
import google.generativeai as genai
import openai
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv()

# --- Set API Keys securely from .env file ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Background Style ---
def set_bg(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            color: white;
        }}
        .stTextArea > div > textarea {{
            background-color: #ffffffcc;
            color: #000;
        }}
        .stButton > button {{
            background-color: #6c63ff;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set custom background
set_bg("https://images.unsplash.com/photo-1542281286-9e0a16bb7366")

# --- App Title ---
st.markdown("<h1 style='text-align: center;'>🤖 GPT-Powered Chatbot & LLM Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ask anything & get smart, real-time answers from advanced AI models</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Model Selection ---
model_choice = st.selectbox("Choose a Model", ["Google Gemini Pro", "OpenAI GPT-4"])

# --- Prompt Box ---
prompt = st.text_area("💬 Enter your query here:")

# --- Generate Button ---
if st.button("🚀 Generate Response"):
    if prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        st.info("Generating response...")

        try:
            # --- Google Gemini Response ---
            if model_choice == "Google Gemini Pro":
                config = {
                    "temperature": 0.8,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
                model = genai.GenerativeModel("gemini-1.5-pro-latest", generation_config=config)
                chat = model.start_chat(history=[])
                response = chat.send_message(prompt)
                st.success("Gemini Response:")
                st.write(response.text)

            # --- OpenAI GPT Response ---
            elif model_choice == "OpenAI GPT-4":
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1024,
                )
                answer = response["choices"][0]["message"]["content"]
                st.success("GPT-4 Response:")
                st.write(answer)

        except Exception as e:
            st.error(f"❌ Error: {e}")
