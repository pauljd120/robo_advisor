
from robo_advisor import to_usd, get_response

import pytest
import requests
import python-dotenv
import json

def test_to_usd():
    result = to_usd(50)
    assert result == "$50.00"

def test_get_response():

    symbol = "MSFT"
    
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

    response = get_response(request_url)

    parsed_response = json.loads(response.text)

    list_parsed_response = list(parsed_response)

    assert list_parsed_response[0] == "Meta Data"
