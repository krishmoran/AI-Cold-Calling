import requests
import json

def retrieve_transcript():
    # Headers
    headers = {
        'authorization': 'sk-4bh9aqg9prmlds81iotfcy8t0413n4r2nmb1er3lfc1ne8t4npa333ueoede0etd69'
    }
    # Data
    data = {
        'call_id': '934daaf5-2300-4585-9edc-bfe461a7bac8',
        # 'questions': [ "Who answered the phone?", "text"],
    }

    # API Request
    response = requests.post('https://api.bland.ai/logs', json=data, headers=headers)

    if response.status_code == 200:
        print("Call recording retrieved successfully!")
        response_data = json.loads(response.text)
        transcripts = response_data['transcripts']

        # Initialize an empty string
        full_transcript = ""

        # Iterate over the transcripts
        for transcript in transcripts:
            # Append the user and the text to the full transcript
            full_transcript += f"{transcript['user']}: {transcript['text']}\n"

        # Return the full transcript
        return full_transcript
    else:
        print("Failed to retrieve call recording. Status code:", response.status_code)
        return None

retrieve_transcript()
