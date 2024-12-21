import pandas as pd
import os
                                # Departure Date,Departure Time,Arrival Date,Arrival Time
# Load the data from CSV
data = pd.read_csv("../json_folder/all_details_flights.csv")

# Append the data to an existing CSV file
data.to_csv("../json_folder/all_data.csv", mode='a', index=False, header=False)

#ata= pd.DataFrame(data)

idx_min_price = data.groupby('Flight Number')['Total Price'].idxmin()

# Use the indices to get the rows with the minimum price
data2 = data.loc[idx_min_price]

# Create DataFrame
# data = cleaned_data

# Loop through columns to split date and time
for col in ['Departure', 'Arrival']:
    data2[f'{col} Date'] = data2[col].apply(lambda x: x.split('T')[0])  # Extract date
    data2[f'{col} Time'] = data2[col].apply(lambda x: x.split('T')[1].split('+')[0])  # Extract time without timezone

# Drop original columns if needed
cleaned_data=data2.drop(columns=['Departure', 'Arrival'])




# Save the cleaned data to a new CSV file
cleaned_data.to_csv("../json_folder/Cleaned_data.csv", index=False)

total_flight= cleaned_data["Flight Number"].count()


# Read the cleaned data from the CSV file
csv_file_path = "Cleaned_data.csv"
cleaned_data = pd.read_csv(csv_file_path)

# HTML template for a single flight card
html_template = """

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Flight Info Card</title>
  <link rel="stylesheet" href="json_folder/test.css">
</head>
<body>
  <div class="container">
    
    <!-- Airline Section -->
    <div class="airline">
        <h2>{operating_carrier}</h2>
        
        <p>{flight_class}</p>
    </div>

    <!-- Flight Timings -->
    <div class="flight-details">
        <div class="departure">
            <h2>{departure_date}</h2>  <!-- Updated placeholder -->
            <h2>{departure_time}</h2>  <!-- Updated placeholder -->

            <p>{origin}</p>
        </div>
        <div class="layover">
            <div class="duration">
                <hr>
                <span>Duration</span>
                <hr>
            </div>
            <p>Non-stop</p>
        </div>
        <div class="arrival">
            <h2>{arrival_date}</h2>  <!-- Updated placeholder -->
            <h2>{arrival_time}</h2>  <!-- Updated placeholder -->
            <p>{destination}</p>
        </div>
    </div>

    <!-- Price and Discount Section -->
    <div class="price-details">
        <p class="discount">Get <b>₹ 500</b> discount using <span class="code">DEALCODE</span></p>
        <h1 class="price">${total_price}</h1>
        <p class="per-adult">per adult ({currency})</p>
    </div>

    <!-- Refundable and Lock Price -->
    <div class="options">
        <p class="refundable">{refund_status}</p>
        <a href="#" class="lock-price">🔒 Lock this price starting from <b>₹ 50</b></a>
    </div>

    <!-- Additional Flight Info -->
    <div class="flight-info">
        <p> Flight Number: {flight_number}</p>
    </div>
</div>
"""

# Generate the HTML for all flights
html_output = ""
for _, row in cleaned_data.iterrows():
    html_output += html_template.format(
        operating_carrier=row["Operating Carrier"],
        departure_time=row["Departure Time"],  # Updated to use 'Departure Time'
        departure_date=row["Departure Date"],  # Updated to use 'Departure Date'
        origin=row["Origin"],
        arrival_time=row["Arrival Time"],      # Updated to use 'Arrival Time'
        arrival_date=row["Arrival Date"],      # Updated to use 'Arrival Date'
        destination=row["Destination"],
        total_price=row["Total Price"],
        currency=row["Currency"],
        refund_status=row.get("Refundable", "N/A"),  # Default to 'N/A' if column doesn't exist
        flight_class=row["Class"],
        flight_number=row["Flight Number"]
    )

# Write the output to an HTML file
output_file = "flight_output.html"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_output)

print(f"HTML file generated successfully: {output_file}")

# Write the output to an HTML file
output_file = "flight_output.html"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_output)

print(f"HTML file generated successfully: {output_file}")

# Optional: Open the HTML file in the default web browser
# os.system(f"start {output_file}")  # Windows
os.system(f"open {"output.html"}")  # macOS
# os.system(f"xdg-open {output_file}")  # Linux
