import json
import re

import re

def extract_name(text):
    text = text.strip()

    # ignore useless inputs
    if len(text.split()) > 3:
        return None

    if any(word in text.lower() for word in ["thank", "hello", "hi"]):
        return None

    return text


def extract_date(text):
    text = text.lower()

    # Match formats like: 20th March, 20 March
    match = re.search(r'(\d{1,2})(st|nd|rd|th)?\s?(march)', text)
    if match:
        return match.group()

    return None


def extract_time(text):
    text = text.lower().strip()

    # normalize variations
    text = text.replace("p.m.", "pm").replace("a.m.", "am")
    text = text.replace("morning", "am").replace("evening", "pm")
    text = text.replace("night", "pm")

    # match: 10, 10:30, 10 am, 10:30 pm
    match = re.search(r'(\d{1,2})(:\d{2})?\s?(am|pm)?', text)

    if match:
        hour = int(match.group(1))
        minute = match.group(2) if match.group(2) else ":00"
        meridian = match.group(3)

        # auto-assign if missing
        if not meridian:
            if 8 <= hour <= 11:
                meridian = "am"
            else:
                meridian = "pm"

        return f"{hour}{minute} {meridian}"

    return None


def extract_purpose(text):
    text = text.lower()

    if any(word in text for word in ["consult", "check", "follow", "appointment"]):
        return text

    return None