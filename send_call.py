import streamlit as st
import requests

# Headers
headers = {
    'authorization': 'sk-4bh9aqg9prmlds81iotfcy8t0413n4r2nmb1er3lfc1ne8t4npa333ueoede0etd69'
}

st.title('Tidecove AI Cold Calling Demo')
# Streamlit input
phone_number = st.text_input('Enter your phone number')


if st.button('Make Call'):
    # Data
    data = {
        'phone_number': phone_number,
        'task': "Your name is Matt and you're an interested property buyer of commercial real estate properties. You are calling to figure out information about the property at 123 waiter street. managed by TRUE realty. Introduce yourself by name and mention you are interested in the property to purchase. This information is crucial to your decision making on whether or not you want to purchase the property and make a lot of money. It’s vital that you get the following information about the property:\n\n- Size (square footage)\n- Age and condition of the building\n- Type of property (e.g., office, retail, industrial)\n- Number of floors\n- Current occupancy rate\n- General Location Information (proximity to highways, zoning laws, etc)\n\nBe sure to ask each question individually over multiple interactions so you can gather comprehensive data without overwhelming the respondent in a single call. Once you are done with the call, thank them for their time.",
        'voice_id': 1185,
        'request_data': {
            'calling': 'TRUE realty',
            'property_address': '123 waiter street'
        },
        'record': True,
        'reduce_latency': True,
        'amd': True,
        'webhook': 'YOUR-WEBHOOK-HERE'
    }

    # API request
    response = requests.post('https://api.bland.ai/call', json=data, headers=headers)
    st.write('Call sent successfully!')