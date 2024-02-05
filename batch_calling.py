import requests
import json

# Headers
headers = {
    'Authorization': 'sk-4bh9aqg9prmlds81iotfcy8t0413n4r2nmb1er3lfc1ne8t4npa333ueoede0etd69',
}

analyze_headers = {
    "authorization": "sk-4bh9aqg9prmlds81iotfcy8t0413n4r2nmb1er3lfc1ne8t4npa333ueoede0etd69",
    "Content-Type": "application/json"
}

def make_request(url, data, headers):
    response = requests.post(url, json=data, headers=headers)
    if response:
        return response.json()
    else:
        print('No response received.')
        return None
    

def parse_analyzed(data):
    try:
        parsed_data = json.loads(data)
        return parsed_data
    except json.JSONDecodeError:
        print("Error: Invalid JSON")
        return None
    
def send_to_google(data):
    return None


def analyze_response(data, payload):
    if data.get('message') == "success":
        batch_id = data.get('batch_id')
        analyzed_data = make_request(f"https://api.bland.ai/v1/batches/{batch_id}/analyze", payload, analyze_headers)
        if analyzed_data.get('status') == 'success':
            print('Analysis was successful.')
            return parse_analyzed(analyzed_data)
            # TODO: parse_analyzed function to parse into proper json
            # TODO: send to google sheet function
        else:
            print('Analysis failed:', analyzed_data.get('message'))
    else:
        print('Batch request failed:', data.get('message'))





def main():
    # Data
    data = {
    "base_prompt": "You are calling {{business}} to renew their subscription to {{service}} before it expires on {{date}}.",
    "call_data": [
        {   
            "phone_number": "2038896404",
            "business": "ABC co.",
            "service": "Netflix",
            "date": "September 4th"
        },
        {
            "phone_number": "2035009260",
            "business": "XYZ inc.",
            "service": "Window Cleaning",
            "date": "December 20th"
        }
        # More data can be added here
    ],
    "label": "Renewal Reminder - Wednesday Afternoon with female voice",
    "voice_id": 0,
    "request_data": {
        "your_name": "Vanessa",
        "day of week": "Wednesday"
    },
    "max_duration": 10,
    "reduce_latency": True,
    "wait_for_greeting": True,
    # "webhook": ***,
    "record": True
}

    payload = {
    "goal": "to collect different data points about many commercial real estate properties, and output that into structured data",
    "questions": [
      ["Who answered the call?", "human or voicemail"],
      ["What is the occupancy rate of the property? ", "float (percentage)"],

      ["Any notes on zoning laws, nearby highways, etc?: ", "string"],
      ["Customer confirmed they were satisfied", "boolean"]
  ]
}
    # API Endpoint
    url = "https://api.bland.ai/batch"

    response_data = make_request(url, data, headers)
    if response_data:
        analyzed = analyze_response(response_data, payload)
        to_google = send_to_google(analyzed)

if __name__ == "__main__":
    main()