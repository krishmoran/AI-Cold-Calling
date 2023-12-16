import requests
import json
from get_format_transcript import retrieve_transcript
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gspread

# hardcoded placeholder for pulling single call transcript
formatted_transcript = retrieve_transcript()

url = 'https://api.openai.com/v1/chat/completions'
api_key = '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'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {api_key}",
}

# Define the message parameters
messages = [
    {
        "role": "system",
        "content": "Return the output as JSON for information about a real estate property based on the cold call transcript provided by the user. The json should have keys 'address', 'size_sq_ft', 'occupancy_rate', 'no_floors', 'location_info', etc"
    },
    {
        "role": "user",
        "content": formatted_transcript
    },
]

data = {
    'model': 'gpt-4-1106-preview',
    'messages': messages,
    'temperature': 1,
    'max_tokens': 3000,
    'top_p': 1,
    'frequency_penalty': 0,
    'presence_penalty': 0,
    'response_format': { "type":"json_object" }
}

# Send the request
try:
    response = requests.post(url, headers=headers, json=data)
except Exception as e:
    print(f"Error during HTTP request: {str(e)}")

# Print the response
if response.status_code == 200:
    data = response.json()
    content_json = json.loads(data['choices'][0]['message']['content'])
    print(content_json)
else:
    print(f"Error: {response.status_code} - {response.text}")

# Convert JSON to DataFrame
df = pd.DataFrame([content_json])

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