import subprocess
import webbrowser
from flask import Flask, render_template, request
import requests
import json
import os
import csv
import pandas as pd

# URL for API
url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchFlights"

# API headers
headers = {
    "x-rapidapi-key": "5505cd9695msh40c90536601370cp195338jsnd49a5fad5745",
    "x-rapidapi-host": "tripadvisor16.p.rapidapi.com"
}

# Directory to save flight data
# os.makedirs('json_folder', exist_ok=True)

# Load the temporary flight data from CSV
temp_data = pd.read_csv("temp_flight_data.csv")


def get_query_string():
    source_airport = temp_data["Source Airport"][0]
    destination_airport = temp_data["Destination Airport"][0]
    date = temp_data["Departure Date"][0]
    returndate = temp_data["Return Date"][0]
    adults = temp_data["Adults"][0]
    class_of_service = temp_data["Class of Service"][0]

    # Validate Class of Service
    valid_classes = ["ECONOMY", "PREMIUM_ECONOMY", "BUSINESS", "FIRST"]
    if class_of_service not in valid_classes:
        raise ValueError(f"Invalid class of service: {class_of_service}. Must be one of {valid_classes}.")

    querystring = {
        "sourceAirportCode": source_airport,
        "destinationAirportCode": destination_airport,
        "date": date,
        "itineraryType": "ROUND_TRIP",
        "sortOrder": "PRICE",
        "numAdults": adults,
        "numSeniors": "0",
        "classOfService": class_of_service,
        "returnDate": returndate,
        "pageNumber": "1",
        "nearby": "yes",
        "currencyCode": "INR"
    }
    print("Final Query String:", querystring)  # Debugging
    return querystring

# Make the API request
try:
    response = requests.get(url, headers=headers, params=get_query_string())
    response.raise_for_status()  # Raise an exception for HTTP errors
    flights = response.json()

    # Save the flights data to a file
    file_path = os.path.join( 'flights_data.json')
    with open(file_path, 'w') as f:
        json.dump(flights, f, indent=4)

    print(f"Flights data saved to {file_path}")
except requests.exceptions.RequestException as e:
    print(f"API request error: {e}")

# Load the data from flights_data.json
with open("flights_data.json", "r") as file:
    data = json.load(file)

flights = []
for flight in data["data"]["flights"]:
    for segment in flight.get("segments", []):
        for leg in segment.get("legs", []):
            flight_details = {
                "Origin": leg["originStationCode"],
                "Destination": leg["destinationStationCode"],
                "Departure": leg["departureDateTime"],
                "Arrival": leg["arrivalDateTime"],
                "Class": leg["classOfService"],
                "Carrier": leg["marketingCarrierCode"],
                "Flight Number": leg["flightNumber"],
                "Distance (KM)": leg["distanceInKM"],
                "International": leg["isInternational"],
                "Operating Carrier": leg["operatingCarrier"]["displayName"],
            }
            for purchase in flight.get("purchaseLinks", []):
                flight_data_with_purchase = flight_details.copy()
                flight_data_with_purchase.update({
                    "Total Price": purchase["totalPrice"],
                    "Currency": purchase["currency"],
                })
                flights.append(flight_data_with_purchase)

# Write to CSV
csv_file_path = 'all_details_flights.csv'
file_exists = os.path.exists(csv_file_path)

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ["Origin", "Destination", "Departure", "Arrival", "Class", "Carrier", 
                  "Flight Number", "Distance (KM)", "International", 
                  "Operating Carrier", "Total Price", "Currency"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(flights)

print(f"Data successfully written to {csv_file_path}.")

# Run testing.py
try:
    subprocess.run(["python", "testing.py"], check=True)
    # subprocess.run(['python', '../flight/another/booking.py'], check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while running testing.py: {e}")

# Open output.html in browser
output_file = os.path.abspath("output.html")
webbrowser.open_new_tab(f"file://{output_file}")
