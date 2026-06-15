from playwright.sync_api import sync_playwright
from groq import Groq
from dotenv import load_dotenv
from parse_chat import parse_chat
import time

load_dotenv()
client = Groq()

msgs = parse_chat(r"WhatsApp Chat - Subhankar\_chat.txt")
VOICE = "Rahul Neupane"
their_msgs = [m["text"] for m in msgs if m["sender"] == VOICE]
examples = "\n".join(their_msgs[:40])

def generate_reply(incoming):
    prompt = f"""You are replying to a message AS {VOICE}. Copy their exact texting style.

Real examples of how {VOICE} writes:
{examples}

{VOICE} just received: "{incoming}"

Write {VOICE}'s reply in their exact style — lowercase, slang, short. Emojis rarely. Reply with ONLY the message text."""
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content.strip()

def get_last_message(page):
    body_text = page.locator("body").inner_text()
    lines = [l.strip() for l in body_text.split("\n") if l.strip()]
    if "Message..." in lines:
        lines = lines[:lines.index("Message...")]
    noise = {"Seen", "·", "Unread"}
    lines = [l for l in lines if l not in noise and not l.startswith("Seen")]
    return lines[-1] if lines else ""

with sync_playwright() as p:
    # persistent context = remembers your login between runs
    context = p.chromium.launch_persistent_context(
        user_data_dir="./insta_session",
        headless=False,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto("https://www.instagram.com/", timeout=60000, wait_until="domcontentloaded")

    print("If not logged in, log in now (only needed the FIRST time).")
    print("Open the chat, then press Enter to start auto-reply.")
    input()

    print("🤖 Auto-reply running. Press Ctrl+C to STOP.\n")
    last_seen = get_last_message(page)
    last_sent = ""

    try:
        while True:
            time.sleep(5)
            current = get_last_message(page)
            if current and current != last_seen and current != last_sent:
                print(f"📩 New: \"{current}\"")
                reply = generate_reply(current)
                print(f"↩️  Reply: \"{reply}\"")
                box = page.get_by_role("textbox").last
                box.click()
                box.fill(reply)
                time.sleep(1)
                page.keyboard.press("Enter")
                print("✅ Sent\n")
                last_sent = reply
                last_seen = current
                time.sleep(2)
    except KeyboardInterrupt:
        print("\n🛑 Stopped.")
        context.close()