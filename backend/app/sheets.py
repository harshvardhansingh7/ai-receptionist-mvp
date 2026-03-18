import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

def save_to_sheet(data):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    if os.getenv("GOOGLE_CREDS"):
        # 🌍 Production (Render)
        creds_dict = json.loads(os.getenv("GOOGLE_CREDS"))
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    else:
        # 💻 Local
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open("Appointments").get_worksheet(0)

    sheet.append_row([
        data.get("name"),
        data.get("date"),
        data.get("time"),
        data.get("purpose")
    ])