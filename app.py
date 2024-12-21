from flask import Flask, render_template, request, send_from_directory
import csv
import os
import subprocess
import webbrowser
import threading

app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Collect data from the form
    data = {
        "Source Airport": request.form['sourceAirport'],
        "Destination Airport": request.form['destinationAirport'],
        "Departure Date": request.form['departureDate'],
        "Return Date": request.form.get('returnDate', ''),
        "Adults": request.form['adults'],
        "Class of Service": request.form['classOfService']
    }

    # Specify the temporary CSV file path
    temp_csv = "temp_flight_data.csv"

    # Read existing data from CSV if it exists
    if os.path.exists(temp_csv):
        with open(temp_csv, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            existing_data = [row for row in reader]
    else:
        existing_data = []

    # Write the new data at the top of the existing data
    existing_data.insert(0, data)

    # Write the updated data back to the CSV file
    with open(temp_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writeheader()  # Write the header only once
        writer.writerows(existing_data)  # Write all rows with new data at the top

    # Run booking.py script after form submission
    try:
        subprocess.run(['python', 'booking.py'], check=True)
        return "Data successfully submitted, CSV updated, and booking.py executed!"
    except subprocess.CalledProcessError as e:
        return f"An error occurred while running booking.py: {e}"

# Function to open the browser automatically
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/static/index.html")

if __name__ == '__main__':
    # Start Flask app in a thread and open the browser after 1 second
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
