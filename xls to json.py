import pandas as pd
import os
import json

# Get the current directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths
excel_file = os.path.join(current_dir, "gallery_json_template.xlsx")
json_file = os.path.join(current_dir, "static", "data.json")  # ✅ Save in /static/

# Load the Excel file
df = pd.read_excel(excel_file, dtype=str)  # Convert all columns to string

# Convert DataFrame to JSON-friendly format
json_data = df.to_dict(orient="records")  # Convert DataFrame to list of dictionaries

# Save the JSON file ensuring slashes are not escaped
with open(json_file, "w", encoding="utf-8") as file:
    json.dump(json_data, file, indent=4, ensure_ascii=False)  # `ensure_ascii=False` prevents escaping `/`

print(f"JSON file saved successfully to: {json_file}")
