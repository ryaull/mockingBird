from groq import Groq
from dotenv import load_dotenv
from parse_chat import parse_chat

load_dotenv()
client = Groq()

msgs = parse_chat(r"WhatsApp Chat - Subhankar\_chat.txt")

target = "Subhankar"
their_msgs = [m["text"] for m in msgs if m["sender"] == target]
examples = "\n".join(their_msgs[:40])   # 40 real examples of how he writes

# the message we want him to reply to
incoming = "yo are you coming to college tomorrow?"

prompt = f"""You are replying to a text message AS a person named {target}.
Copy his exact texting style. Here are real examples of how {target} writes:

{examples}

Now {target} receives this message:
"{incoming}"

Write {target}'s reply in his exact style — same lowercase, slang, emojis, and short length.
Reply with ONLY the message text, nothing else."""

reply = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
)

print("Them:", incoming)
print(f"{target} (AI):", reply.choices[0].message.content)