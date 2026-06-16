# 🐦 Mockingbird

**An AI that learns how you text — and replies in your voice.**

Feed it your chat history, and Mockingbird picks up how a person actually writes:
their slang, their lowercase, the emojis they overuse, the way they say "bhai."
Then it can answer messages as that person. I wired it into live Instagram as a
proof of concept — it reads the chat and replies on its own, in my voice.

---

## 🎥 Demo

[![Mockingbird Demo][(https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://youtu.be/VIDEO_ID)](https://youtu.be/gTq9uq3DYKc)s

*Click to watch it reply on a real Instagram conversation.*

---

## What it does

- **Reads** a WhatsApp chat export and cleans it into structured messages
- **Learns** a chosen person's texting style — tone, length, slang, emoji habits
- **Generates** replies in that voice (review-first, or fully autonomous)
- **Connects** to live Instagram (proof-of-concept) to auto-reply in real time

## How it's built

| Part | Tech |
|------|------|
| Style engine | Python + Groq (Llama 3.3) |
| App interface | Streamlit |
| Live messaging | Playwright browser automation |

## A finding worth noting

The model doesn't just copy a style — it **exaggerates** it. Point it at someone
who uses the odd emoji, and it'll stuff one in every line. Measuring that gap
between real and imitated style is where this stops being a toy and starts being
research.

## Running it

```bash
pip install -r requirements.txt
streamlit run mockingbird_app.py
```

Add a `.env` file with your key:


GROQ_API_KEY=your_key_here

## On ethics

Chat data was used with consent and is never committed to this repo. The
autonomous Instagram mode is a research demo, not a product — there's no official
API for personal accounts, and auto-replying to someone who thinks they're talking
to a human isn't something this is meant for. Disclosure matters.

## Status

Working prototype. Style mimicry holds up convincingly; next up is formally
**evaluating** how well it captures a voice — automatic metrics plus a
human "can you tell which is real?" test.

---

*Built over one very productive afternoon.* 🐦
That last line's a nice touch — recruiters/committees love a builder who ships.
