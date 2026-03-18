import json
import re

def extract_name(text):
    if len(text.split()) <= 3:
        return text
    return None

def extract_date(text):
    if "march" in text.lower():
        return text
    return None

def extract_time(text):
    match = re.search(r'\d{1,2}(:\d{2})?\s?(am|pm)', text.lower())
    return match.group() if match else None

def extract_purpose(text):
    if any(word in text.lower() for word in ["consult", "check", "follow"]):
        return text
    return None