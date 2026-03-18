from fastapi import FastAPI
from pydantic import BaseModel

from app.memory import get_session, reset_session
from app.extractor import extract_name, extract_date, extract_time, extract_purpose
from app.sheets import save_to_sheet

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    message: str
    session_id: str


@app.post("/chat")
def chat(user: UserInput):

    session = get_session(user.session_id)
    data = session["data"]

    text = user.message.lower()

    # 🧠 Fill missing fields
    if not data["name"]:
        name = extract_name(user.message)
        if name:
            data["name"] = name
            return {"response": f"Nice to meet you {name}. What date would you like?"}
        return {"response": "May I have your full name?"}

    if not data["date"]:
        date = extract_date(text)
        if date:
            data["date"] = date
            return {"response": "What time works for you?"}
        return {"response": "Please tell me the date of appointment."}

    if not data["time"]:
        time = extract_time(text)
        if time:
            data["time"] = time
            return {"response": "What is the purpose of your visit?"}
        return {"response": "Please tell me a valid time."}

    if not data["purpose"]:
        purpose = extract_purpose(text)
        if purpose:
            data["purpose"] = purpose

            # ✅ SAVE HERE
            save_to_sheet(data)

            response = f"Thank you {data['name']}, your appointment is booked on {data['date']} at {data['time']}."

            reset_session(user.session_id)
            return {"response": response}

        return {"response": "What is the purpose of your appointment?"}

    return {"response": "How can I help you?"}