import requests
import json
import os
import time
from create_google_sheet import create_google_sheet

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
    

def parse_analyzed(data, initial_data):
    try:
        parsed_data = data
        if 'answers' in parsed_data:
            formatted_data = {}
            for call_id, answers in parsed_data['answers'].items():
                formatted_data[call_id] = {
                    "phone number": initial_data['call_data'][int(call_id)]['phone_number'],
                    "address": initial_data['call_data'][int(call_id)]['address'],
                    "call_responder": answers[0],
                    "property_type": answers[1],
                    "number_of_floors": answers[2],
                    "building_age": answers[3],
                    "property_square_footage": answers[4],
                    "occupancy_rate": answers[5],
                    "location_notes": answers[6]
                }
            return formatted_data
        else:
            print("Error: No 'answers' key in the JSON")
            return None
    except Exception as e:
        print("Error:", str(e))
        return None

def analyze_response(batch_id, initial_data, payload):
    analyzed_data = make_request(f"https://api.bland.ai/v1/batches/{batch_id}/analyze", payload, analyze_headers)
    if analyzed_data.get('status') == 'success':
        print('Analysis was successful.')
        return parse_analyzed(analyzed_data, initial_data) 
    else:
        print('Analysis failed:', analyzed_data.get('message'))
        

def main():
    # Data
    data = {
    "base_prompt": "Your name is Matt and you're an interested property buyer of commercial real estate properties. You are calling to gather information about the property at {{address}}, managed by {{prop_manager}}. Introduce yourself by name and mention you are interested in the property to purchase. This information is crucial to your decision making on whether or not you want to purchase the property and make a lot of money. It’s vital that you get the following information about the property: - Size (square footage) - Age of the building - Type of property (e.g., office, retail, industrial) - Number of floors - Current occupancy rate - General Location Information (proximity to highways, zoning laws, etc) Be sure to ask each question individually over multiple interactions so you can gather comprehensive data without overwhelming the respondent in a single call. Only mention the address of the property one time. Once you are done with the call, thank them for their time.",
    "call_data": [
        {   
            "phone_number": "2038896404",
            "address": "123 waiter street",
            "prop_manager": "TRUE realty",
        },
        # {
        #     "phone_number": "2035009260",
        #     "address": "434 Collacle Street",
        #     "prop_manager": "Jing realty",
        # }
        # More data can be added here
    ],
    "label": "property data collection -- youtube voice",
    "voice_id": 1186,
    "request_data": {
        "your_name": "Matt",
    },
    "max_duration": 10,
    "reduce_latency": True,
    "wait_for_greeting": True,
    # "webhook": ***,
    "record": False, 
    "reduce_latency": True
}

    payload = {
    "goal": "to collect different data points about many commercial real estate properties, and output that into structured data",
    "questions": [
      ["Who answered the call?", "human or voicemail"],
      ["What type of property is it? (e.g. office, retail, industrial)", "string"],
      ["How many floors does the property have?", "integer"],
      ["How old is the building?", "integer"],
      ["What is the square footage of the property (in sq ft)?", "integer"],
      ["What is the occupancy rate of the property? ", "float (percentage)"],
      ["Any notes on zoning laws, nearby highways, etc?: ", "string"],  ]
}
    # API Endpoint
    url = "https://api.bland.ai/batch"

    response_data = make_request(url, data, headers)

    if response_data:
        batch_id = response_data.get('batch_id')
        get_url = f"https://api.bland.ai/v1/batches/{batch_id}"
        while True:
            time.sleep(30)  # wait for 60 seconds
            batch_status = requests.request("GET", get_url, headers=headers)
            if batch_status:
                analysis = batch_status.get('analysis', {})
                if analysis.get('in_progress_calls', 0) == 0 and analysis.get('total_calls', 0) == analysis.get('completed_calls', 0):
                    break

        analyzed = analyze_response(response_data, data, payload)
        create_google_sheet(analyzed)

if __name__ == "__main__":
    main()