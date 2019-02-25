from dotenv import load_dotenv
import json
import os
import requests
import datetime
import csv

load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

# see: https://www.alphavantage.co/support/#api-key
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
#print("API KEY: " + api_key)


#from your walkthrough video
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

symbol = input("Enter the name of a stock: ")


while(symbol.isalpha() == 0 or len(symbol) < 3 or len(symbol) > 5):
    symbol = input("Error: Please enter a valid stock name: ")

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
response = requests.get(request_url)

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys()) #assumes latest day is first in the data structure

latest_day = dates[0]

latest_close = parsed_response["Time Series (Daily)"][latest_day]["4. close"]

high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))


recent_high = max(high_prices)
recent_low = min(low_prices)


print("-----------------")
print(f"STOCK SYMBOL: {symbol}")

current_time = datetime.datetime.now()
print("RUN AT: " + current_time.strftime("%x") + " " + current_time.strftime("%X") + " " + current_time.strftime("%p"))
print("-----------------")
print(f"LATEST DAY OF AVAILABLE DATA: {last_refreshed}")
print(f"LATEST DAILY CLOSING PRICE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-----------------")
print("RECOMMENDATION: Buy!")
print("RECOMMENDATION REASON: Because the latest closing price is within threshold XYZ etc., etc. and this fits within your risk tolerance etc., etc.")
print("-----------------")

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames =csv_headers)
    writer.writeheader()
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"],
        })

print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-----------------")
print("HAPPY INVESTING!")
print("-----------------")
