import csv
import json

# the cleaned csv data set should have valid and proper headers

def csv_to_json(input_file, output_file):
    # List to store the JSON data
    json_data = []
    
    # Read the CSV file with '+' as delimiter
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        # Use csv.reader with '+' as delimiter
        csvreader = csv.reader(csvfile, delimiter='+')
        
        # Read the header
        headers = [header.strip() for header in next(csvreader)]
        
        # Process each row
        for row in csvreader:
            # Create a dictionary for each row
            # Strip whitespace from each value
            row_dict = {headers[i].strip(): value.strip() for i, value in enumerate(row)}
            
            # Add to JSON data list
            json_data.append(row_dict)
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(json_data, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"Converted {len(json_data)} records to JSON")

# Example usage
input_csv = '2_ALL INDIA QUOTA AYUSH ROUND-1 ALLOTMENTS.txt'
output_json = '2_ALL INDIA QUOTA AYUSH ROUND-1 ALLOTMENTS.json'
csv_to_json(input_csv, output_json)