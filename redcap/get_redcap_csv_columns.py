import csv
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input_csv", help="CSV file with input data")
parser.add_argument("clean_csv", help="CSV file to write output to")
parser.add_argument("column_names", help="TXT file to write the column names to")

args = parser.parse_args()
csv_file = args.input_csv
csv_cleaned_cols_file = args.clean_csv
column_names_file = args.column_names

def fix_header(header): # Some of the columns are empty. Find empty columns and rename using the previous column title with a ".2" suffix
	header_names = []
	blank_column_names = [] # Store the names given to blank columns
	duplicate_column_names = []

	for idx, x in enumerate(header):
		if x == "": # If column is empty, use the previous one to derive the name
			previous_column = header[idx-1] # Get the previous column
			new_column = previous_column + ".2" # Add suffux to column name
			blank_column_names.append(new_column)
			header[idx] = new_column # Rename the empty column

		else:
			x = x.rstrip() # Remove any extra whitespace from the right hand side
			previous_columns = header[0:idx]


			if x in previous_columns:
				duplicate_column_names.append(x)
				number_of_previous_duplicates = duplicate_column_names.count(x) + 1 # If there are duplicates, rename using a number as suffix
				x = x + "." + str(number_of_previous_duplicates)

			header[idx] = x


	if len(blank_column_names) > 0: # If blank columns found, print the new names for them
		print("Number of blank columns found: " + str(len(blank_column_names)))
		print("Blank columns renamed to:")
		for col in blank_column_names:
			print(col)

	if len(duplicate_column_names) > 0: # If duplicate columns found, print the new names for them
		print("\nDuplicate columns found")
		duplicate_set = set(duplicate_column_names)

		for name in duplicate_set:
			name_count = duplicate_column_names.count(name)
			print("\t" + name + ": " + str(name_count))

	return(header)


with open(csv_file, "r") as input_csv, open(csv_cleaned_cols_file, "w") as output_csv:
	csv_data = csv.reader(input_csv, delimiter=',', quotechar='"')
	header = next(csv_data) # Get the column names (i.e., categories)
	new_header = fix_header(header) # Get the fixed header
	writer = csv.writer(output_csv)
	writer.writerow(new_header) # Create csv with fixed header
	for row in csv_data:
		writer.writerow(row)

with open(column_names_file, "w") as outfile:
	for row in new_header: # Write the column names to text file
		outfile.write(row + "\n")
