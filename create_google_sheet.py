import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

def create_google_sheet(data):
    # Convert JSON to DataFrame
    df = pd.DataFrame([data])

    # Use credentials to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Create a new Google Sheets file
    spreadsheet = client.create('Test Cold Calling Output')

    # Share the Google Sheets file with your email (or any other email)
    spreadsheet.share('krishmoran0@gmail.com', perm_type='user', role='writer')

    # Open the first sheet
    sheet = spreadsheet.sheet1

    # Write DataFrame to Google Sheets
    set_with_dataframe(sheet, df)

    # Get the link to access the Google Sheets file
    spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"



    print(spreadsheet_url)

    return spreadsheet_url