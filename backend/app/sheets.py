import gspread
from oauth2client.service_account import ServiceAccountCredentials

def save_to_sheet(data):
    scope = ["https://spreadsheets.google.com/feeds", 
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("Appointments").get_worksheet(0)

    sheet.append_row([
        data["name"],
        data["date"],
        data["time"],
        data["purpose"]
    ])