import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from parse_chat import parse_chat
import html

load_dotenv()
client = Groq()
if "thread" not in st.session_state:
    st.session_state["thread"] = []
st.set_page_config(page_title="Mockingbird", page_icon="🐦", layout="centered")

# ---------- styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600..800&family=Inter:wght@400;500;600&display=swap');

.stApp {
    background: radial-gradient(1100px 550px at 15% -10%, #2a1f38 0%, #14151b 55%);
    color: #f1ede4;
}
footer {visibility: hidden;}
.block-container { padding-top: 4rem; }

/* nav bar */
.nav { display:flex; align-items:center; justify-content:space-between;
       padding-bottom: 14px; border-bottom: 1px solid rgba(241,237,228,.10); }
.brand { font-family:'Bricolage Grotesque',sans-serif; font-size:34px; font-weight:800;
         letter-spacing:-.02em; }
.brand .b { color:#6e9bff; }
.sub { color:#9aa0b0; font-family:'Inter'; font-size:14px; margin:10px 0 0; }

/* headings */
h2, h3, .stSubheader { font-family:'Bricolage Grotesque',sans-serif !important; }

/* buttons */
.stButton button {
    background:#6e9bff; color:#0c1018; border:none; border-radius:9px;
    font-family:'Inter'; font-weight:600; padding:9px 18px; transition:.15s;
}
.stButton button:hover { filter:brightness(1.1); transform:translateY(-1px);
    box-shadow:0 6px 18px rgba(110,155,255,.25); }

/* inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
    background:#0f1016 !important; color:#f1ede4 !important;
    border-radius:9px !important; border:1px solid rgba(241,237,228,.15) !important;
}

/* toggle accent */
[data-baseweb="checkbox"] [aria-checked="true"] div { background:#6e9bff !important; }

/* fingerprint card */
.card { background:#1c1e27; border:1px solid rgba(241,237,228,.10);
        border-radius:14px; padding:18px 20px; margin-top:6px; }

/* chat bubbles */
.bubble-row { display:flex; margin:7px 0; }
.row-them { justify-content:flex-start; }
.row-me { justify-content:flex-end; }
.bubble {
    max-width:78%; padding:11px 15px; font-family:'Inter'; font-size:15px;
    line-height:1.45; border-radius:18px; animation:pop .25s ease;
}
@keyframes pop { from{opacity:0; transform:translateY(8px) scale(.97);} to{opacity:1; transform:none;} }
.them { background:#43351f; border:1px solid rgba(232,161,75,.35); border-bottom-left-radius:5px; }
.me   { background:#2c3a5e; border:1px solid rgba(110,155,255,.4); border-bottom-right-radius:5px; }
.lbl  { font-size:10px; letter-spacing:.12em; text-transform:uppercase;
        color:#9aa0b0; margin:3px 7px 0; font-family:'Inter'; }
</style>
""", unsafe_allow_html=True)

def bubble(side, label, text):
    cls = "me" if side == "me" else "them"
    row = "row-me" if side == "me" else "row-them"
    align = "right" if side == "me" else "left"
    safe = html.escape(text)
    st.markdown(
        f"<div class='lbl' style='text-align:{align}'>{label}</div>"
        f"<div class='bubble-row {row}'><div class='bubble {cls}'>{safe}</div></div>",
        unsafe_allow_html=True,
    )

# ---------- nav bar ----------
nav_l, nav_r = st.columns([3, 1], vertical_alignment="center")
with nav_l:
    st.markdown("<div class='brand'>🐦 Mocking<span class='b'>bird</span></div>", unsafe_allow_html=True)
with nav_r:
    auto = st.toggle("Auto-send", value=False)
mode = "Auto-send" if auto else "Review first"

st.markdown("<p class='sub'>Learns how someone texts, then replies in their voice.</p>", unsafe_allow_html=True)
if mode == "Auto-send":
    st.warning("⚠ Auto-send only when the other person knows a bot may reply.")
st.divider()

uploaded = st.file_uploader("Upload your WhatsApp chat export (.txt)", type="txt")

if uploaded:
    with open("uploaded_chat.txt", "wb") as f:
        f.write(uploaded.getbuffer())

    msgs = parse_chat("uploaded_chat.txt")
    people = list({m["sender"] for m in msgs})

    st.success(f"Found {len(msgs)} messages")

    target = st.selectbox("Whose voice should the bot reply in?", people)
    their_msgs = [m["text"] for m in msgs if m["sender"] == target]
    st.caption(f"{target} sent {len(their_msgs)} messages.")

    # --- learn style ---
    if st.button(f"Learn {target}'s style"):
        sample = "\n".join(their_msgs[:150])
        prompt = f"""These are real text messages by {target}:

{sample}

Describe how {target} texts in a short list: tone, message length, capitalization, punctuation, emojis, slang/signature words, and any quirks."""
        with st.spinner(f"Studying how {target} writes..."):
            reply = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
        st.session_state["fingerprint"] = reply.choices[0].message.content
        st.session_state["target"] = target
        st.session_state["thread"] = []

    # --- show fingerprint ---
    if "fingerprint" in st.session_state:
        st.subheader("Style fingerprint")
        st.markdown(f"<div class='card'>{st.session_state['fingerprint']}</div>", unsafe_allow_html=True)

    # --- draft a reply ---
    if "fingerprint" in st.session_state:
        st.divider()
        st.subheader("Conversation")

        # render the running thread
        for m in st.session_state.get("thread", []):
            bubble(m["side"], m["label"], m["text"])

        incoming = st.text_input("Message you received:")

        if st.button("Draft reply") and incoming:
            voice = st.session_state["target"]
            examples = "\n".join(their_msgs[:40])
            prompt = f"""You are replying to a message AS {voice}. Copy their exact texting style.

Real examples of how {voice} writes:
{examples}

Their style summary:
{st.session_state['fingerprint']}

{voice} just received this message:
"{incoming}"

Write {voice}'s reply in their exact style — same lowercase, slang, and short length. Use emojis RARELY, only when it genuinely fits, never more than one, and usually none. Most messages should have no emoji at all. Reply with ONLY the message text."""
            with st.spinner("Writing..."):
                reply = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                )
            st.session_state["draft"] = reply.choices[0].message.content
            st.session_state["last_incoming"] = incoming

        # --- pending draft ---
        if "draft" in st.session_state:
            voice = st.session_state["target"]
            bubble("them", "Them", st.session_state.get("last_incoming", ""))

            if mode == "Review first":
                edited = st.text_area("Draft (edit before sending):", st.session_state["draft"])
                col1, col2 = st.columns(2)
                if col1.button("✅ Approve & send"):
                    st.session_state["thread"].append({"side": "them", "label": "Them", "text": st.session_state["last_incoming"]})
                    st.session_state["thread"].append({"side": "me", "label": f"{voice} · sent", "text": edited})
                    del st.session_state["draft"]
                    st.rerun()
                if col2.button("🔄 Regenerate"):
                    del st.session_state["draft"]
                    st.rerun()
            else:  # Auto-send
                bubble("me", f"{voice} · auto-sent", st.session_state["draft"])
                st.session_state["thread"].append({"side": "them", "label": "Them", "text": st.session_state["last_incoming"]})
                st.session_state["thread"].append({"side": "me", "label": f"{voice} · auto-sent", "text": st.session_state["draft"]})
                del st.session_state["draft"]