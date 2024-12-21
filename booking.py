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
os.makedirs('json_folder', exist_ok=True)

# API request without specifying airport codes or dates
# querystring = {"sourceAirportCode":"BOM","destinationAirportCode":"DEL","date":"2024-12-21","itineraryType":"ONE_WAY","sortOrder":"PRICE","numAdults":"1","numSeniors":"0","classOfService":"ECONOMY","pageNumber":"1","nearby":"yes","currencyCode":"INR"}

# querystring = {"sourceAirportCode":"BLR","destinationAirportCode":"BOM","date":"2024-12-21","itineraryType":"ROUND_TRIP","sortOrder":"PRICE","numAdults":"1","numSeniors":"0","classOfService":"ECONOMY","returnDate":"2025-01-03","pageNumber":"1","nearby":"yes","currencyCode":"INR"}

temp_data=pd.read_csv("json_folder/temp_flight_data.csv")
# def get_query_string():
#     source_airport = temp_data["Source Airport"][0]
#     destination_airport = temp_data["Destination Airport"][0]
#     date = temp_data["Departure Date"][0]
#     returndate = temp_data["Return Date"][0]
#     adults = temp_data["Adults"][0]
#     class_of_service = temp_data["Class of Service"][0]

#     querystring = {
#         "sourceAirportCode": source_airport,
#         "destinationAirportCode": destination_airport,
#         "date": date,
#         "itineraryType": "ROUND_TRIP",
#         "sortOrder": "PRICE",
#         "numAdults": adults,
#         "numSeniors": "0",
#         "classOfService": class_of_service,
#         "returnDate": returndate,
#         # "nonstop":"no",
#         "pageNumber": "1",
#         "nearby": "yes",
#         "currencyCode": "INR"
#     }
#     return querystring

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
response = requests.get(url, headers=headers, params=get_query_string())

# Check the response status
if response.status_code == 200:
    flights = response.json()

    # Define the file path
    file_path = os.path.join('json_folder', 'flights_data.json')

    # Save the flights data to a file
    with open(file_path, 'w') as f:
        json.dump(flights, f, indent=4)

    print(f"Flights data saved to {file_path}")
else:
    print(f"Error occurred. Status code: {response.status_code}, Message: {response.text}")







# Load the data from flights_data.json
with open("json_folder/flights_data.json", "r") as file:
    data = json.load(file)

# Extract flights and purchase link data

flights = []

for flight in data["data"]["flights"]:
    for segment in flight.get("segments", []):
        for leg in segment.get("legs", []):
            # Extracting flight details from the 'leg'
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
            
            # Loop through the purchaseLinks and merge with the flight data
            for purchase in flight.get("purchaseLinks", []):
                flight_data_with_purchase = flight_details.copy()
                flight_data_with_purchase.update({
                    "Total Price": purchase["totalPrice"],
                    "Currency": purchase["currency"],
                })
                
                # Append the merged data
                flights.append(flight_data_with_purchase)

# Write the data to a CSV file
csv_file_path = 'json_folder/all_details_flights.csv'

# Check if file exists to write header
file_exists = os.path.exists(csv_file_path)

# with open(csv_file_path, mode='a', newline='') as file:
#     fieldnames = ["Origin", "Destination", "Departure", "Arrival", "Class", "Carrier", "Flight Number", "Distance (KM)", "International", "Operating Carrier", "Total Price", "Currency"]
#     writer = csv.DictWriter(file, fieldnames=fieldnames)

#     # Write header if the file doesn't exist
#     if not file_exists:
#         writer.writeheader()

#     # Write the flight data to the CSV file
#     writer.writerows(flights) 

# print(f"Data successfully written to {csv_file_path}.")


with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ["Origin", "Destination", "Departure", "Arrival", "Class", "Carrier", 
                  "Flight Number", "Distance (KM)", "International", 
                  "Operating Carrier", "Total Price", "Currency"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the flight data to the CSV file
    writer.writerows(flights)

print(f"Data successfully written to {csv_file_path}.")



# Run testing.py
subprocess.run(["python", "testing.py"])



# Open output.html in browser
output_file = os.path.abspath("output.html")
webbrowser.open_new_tab(f"file://{output_file}")

# Run testing.pyˀˀ





