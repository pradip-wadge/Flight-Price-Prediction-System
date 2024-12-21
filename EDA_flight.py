import pandas as pd
import datetime
import subprocess

data=pd.read_csv("json_folder/all_details_flights.csv")
# Append the data to the existing CSV file
data.to_csv("json_folder/all_data.csv", mode='a', index=False, header=False)

# Group by 'Flight Number' and get the index of the row with the minimum 'Price'
idx_min_price = data.groupby('Flight Number')['Total Price'].idxmin()

# Use the indices to get the rows with the minimum price
cleaned_data = data.loc[idx_min_price]

cleaned_data.to_csv("Cleaned_data.csv", index=False)

subprocess.run(["python", "testing.py"])