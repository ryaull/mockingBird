\# 🐦 Mockingbird



I got curious whether an AI could learn to text like a specific person — not "a chatbot," but \*you\*, lowercase typos and "bro" and all. So I built this.



Mockingbird reads your chat history with someone, figures out how they actually write, and then drafts replies in that exact voice. You can keep it on a leash (review every reply before it sends) or let it run on its own.



\## How it works



You feed it a WhatsApp export. It cleans that up into real messages, then studies one person — their tone, how long their texts are, whether they bother with capital letters, which emojis they lean on, their slang. From there it can answer incoming messages the way that person would.



The fun part: when I pointed it at my own chats, the replies were close enough to be unsettling. The interesting part (for the paper): it tends to \*exaggerate\* — grab the most obvious habit, like emojis, and overdo it. Turns out measuring that gap is half the research.



\## Built with



Python, Streamlit for the interface, and Groq running Llama 3.3 for the language stuff.



\## Running it yourself







pip install -r requirements.txt



streamlit run mockingbird\_app.py



You'll need a Groq API key in a `.env` file:

GROQ\_API\_KEY=your\_key\_here



\## A note on ethics



This obviously gets weird fast, so: the chat data I tested on was used with permission and is never committed to this repo. Auto-reply mode is only meant for situations where the other person knows they might be talking to a bot — not for quietly pretending to be someone. There's no official API for personal WhatsApp/Instagram accounts, so any live-messaging piece here is a proof-of-concept, not something meant to run at scale.



\## Where it's at



Working prototype. The style mimicry holds up; next up is properly measuring \*how well\* it captures a voice.

