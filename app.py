import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

st.title("Mockingbird — setup test")

msg = st.text_input("Say something:")
if msg:
    reply = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": msg}],
    )
    st.write(reply.choices[0].message.content)