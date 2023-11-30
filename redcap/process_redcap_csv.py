import csv
from collections import OrderedDict
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input_csv", help="CSV file with input data")
parser.add_argument("output_csv", help="CSV file to write output to")
parser.add_argument("desired_columns", help="TXT file with the columns to select")

args = parser.parse_args()
input_file = args.input_csv
output_file = args.output_csv
desired_columns_file = args.desired_columns

with open(desired_columns_file) as f:
	desired_columns = f.read().split('\n')

desired_columns =  [x for x in desired_columns if x] # Remove any blank column names (occurs if the last line in the desired_columns text file is empty)

cd_patient_data_dict = dict()
with open(input_file) as csv_file:
	csv_data = csv.DictReader(csv_file, delimiter=',', quotechar='"') # Open input csv
	for row in csv_data:
		new_row = OrderedDict() # Use ordered dictionary to ensure that the column order is maintained
		new_row = {key: row[key] for key in desired_columns} # Select desired columns
		record_id = new_row["Record ID"] # The Record ID is used to identify rows belonging to the same patient
		if record_id in cd_patient_data_dict.keys(): # If a row with this ID has already been processed, fill in any missing values if possible
			for key, value in new_row.items():
				if key != "Record ID":
					if len(value) > 0: # If the column has an entry, it can be added to the dictionary. This ensures that the existing values aren't overwritten with empty ones.
						if len(cd_patient_data_dict[record_id][key]) == 0:
							cd_patient_data_dict[record_id][key] = value
						else:
							print("Warning: Multiple rows were detected with entries for the same column in Record ID: "  + key) # Check if an entry already exists for that column. Print a warning instead of overwritting it
							print("\tEntry: " + cd_patient_data_dict[record_id][key])
							print("\tEntry: " + new_row[key])
		else:
			cd_patient_data_dict[record_id] = new_row


with open(output_file, "w") as output_csv:
	writer = csv.writer(output_csv)
	writer.writerow(desired_columns) # Write header to output csv
	for v in cd_patient_data_dict.values(): # Add rows to csv file
		row = list(v.values())
		writer.writerow(row)
