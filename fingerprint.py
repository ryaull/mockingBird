from groq import Groq
from dotenv import load_dotenv
from parse_chat import parse_chat

load_dotenv()
client = Groq()

# 1. read the chat
msgs = parse_chat(r"WhatsApp Chat - Subhankar\_chat.txt")

# 2. keep only the person we want to imitate
target = "Subhankar"
their_msgs = [m["text"] for m in msgs if m["sender"] == target]
sample = "\n".join(their_msgs[:150])   # first 150 of their messages

# 3. ask the model to describe their style
prompt = f"""These are real text messages written by one person named {target}:

{sample}

Describe how {target} texts, in a short list:
- tone
- typical message length
- capitalization habits
- punctuation habits
- emojis they use
- slang or signature words
- any other quirks"""

reply = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
)

print(reply.choices[0].message.content)