"""
This script takes in a .csv file of the form:
	Timestamp,Email Address,officer,schedule [Monday],schedule [Tuesday],schedule [Wednesday],schedule [Thursday],schedule [Friday]
Each row in the .csv file is for a single person. The script converts all the information to a .json of the form:
	Email: {
		"officer": "",
		"schedule" : [],
		"tabled_with": []
	}
Example:
	input: csv, of the form 
		2/1/2018 13:57:02,tae.kim@berkeley.edu,TRUE,10AM~11AM,n/a,12PM~1PM,"11AM~12PM, 12PM~1PM, 1PM~2PM",11AM~12PM
	output: json, of the form:
		{"tae.kim@berkeley.edu": {
			"officer": "True",
			"schedule": [["True", "False", "False", "False"],
						 ["False", "False", "False", "False"],
						 ["False", "True", "True", "True"],
						 ["False", "True", "False", "False"]]
			"tabled_with": []
		}}

"""
import csv # wow i wonder wat dis is used for
import json # wow i wonder wat dis is used for pt.2
import pprint # so i can print dictionaries nicely when debugging

import argparse

def process_data(csv_input, json_starter):
	dictionary = {} # this stores all the data
	input_file_name = csv_input # make sure this input csv file exists in the same directory as this script
	output_file_name = 'formatted_preferences.json' #eh dw the script will make the .json file if it isn't there

	# print(input_file_name)

	#read csv line by line
	with open(input_file_name, 'rt') as f: # why do i use with? it's like a try statement, and it closes the reader when done (cause im too lazy to close lol)
		line_num = 1 #keep track of which line in csv file you're on
		for line in csv.reader(f, quotechar = '"', delimiter = ',', # basically cleverly splits csv by cell (not by comma) cause cells may have multiple elements separated by commas
								quoting = csv.QUOTE_ALL, skipinitialspace = True): # lol thanks stackoverflow how the hell would i have figured this out otherwise?
			if line_num != 1: #skip the first line (column headers)

				email = line[1]
				is_officer = line[2].capitalize() #i love python i mean srsly a capitalize function? omg i luv it
				schedule = line[3:]

				formatted_schedule = [] # format the schedule because rn its a bunch of strings
				for slots in schedule:
					day_slots = ['False', 'False', 'False', 'False'] #[10AM~11AM, 11AM~12PM, 12PM~1PM, 1PM~2PM]
					if '10AM~11AM' in slots:
						day_slots[0] = 'True'
					if '11AM~12PM' in slots:
						day_slots[1] = 'True'
					if '12PM~1PM' in slots:
						day_slots[2] = 'True'
					if '1PM~2PM' in slots:
						day_slots[3] = 'True'

					formatted_schedule.append(day_slots) #yeah add that fucker into that list

				# add everything into dictionary
				dictionary[email] = {}
				dictionary[email]["officer"] = is_officer
				dictionary[email]["schedule"] = formatted_schedule
				dictionary[email]["tabled_with"] = []

			line_num = line_num + 1 # dont forget to keep track of line number

	#export dictionary to a json
	with open(output_file_name, 'w') as f:
		json.dump(dictionary, f) #yep it's that ez hail python fuck c


if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "CSV to JSON Converter")
    parser.add_argument("csv_input", type=str, help = "Member availabilities, .csv")
    parser.add_argument("json_starter", type=str, help = "Previous week's Member data, .json; if no previous data, use \"none.json\"")
    args = parser.parse_args()
    process_data(args.csv_input, args.json_starter)