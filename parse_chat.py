import re

def parse_chat(filepath):
    pattern = re.compile(r'^\[(.*?)\]\s*([^:]+?):\s(.*)$')
    messages = []
    skip = ["end-to-end encrypted", "is a contact"]

    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.replace("\u200e", "").replace("\u202f", " ").strip()
            if not line:
                continue

            m = pattern.match(line)
            if m:
                sender = m.group(2)
                text = m.group(3)

                if any(phrase in text for phrase in skip):
                    continue

                messages.append({"sender": sender, "text": text})
            else:
                if messages:
                    messages[-1]["text"] += " " + line

    return messages