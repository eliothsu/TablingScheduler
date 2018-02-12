"""
This script takes in a .json file of the following form:
	[[["email", "email", ..., "email"],
	["email", "email", ..., "email"],
	["email", "email", ..., "email"],
	...
	["email", "email", ..., "email"]]]
and outputs a .json of the following form:
	[[["First Last", ..., "First Last"],
	["First Last", ..., "First Last"],
	["First Last", ..., "First Last"],
	...
	["First Last", ..., "First Last"]]]
"""

import json
import csv
import pprint
import argparse

def convert_to_names(in_file, lookup_csv) :
	input_file = in_file # make sure the input file is there!
	lookup_file = lookup_csv
	dictionary = {} # contains the contents of the input file as a python dictionary
	lookup_table = {} # contain "email": "First Last" pairs

	#populate the lookup_table with contents of lookup.csv
	with open(lookup_file, 'rt') as f:
		for line in csv.reader(f):
			lookup_table[line[1]] = line[0]

	# read the json file (yep its that ez man)
	with open(input_file, 'r') as f:
		dictionary = json.load(f)

	# go thru the dictionary, replace emails with names
	for row in dictionary:
		# print(lookup_table)
		for slot in row:
			for i, val in enumerate(slot):
				if (val in lookup_table):
					slot[i] = lookup_table[val]

	# write back into the json file (yep ez ikr)
	with open(input_file, 'w') as f:
		json.dump(dictionary, f)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Email to name converter for final schedule")
    parser.add_argument("input_file", type=str, help = "Week tabling schedule, .json")
    parser.add_argument("lookup_csv", type=str, help = "Lookup table for emails and names, like \"lookup.csv\"")
    args = parser.parse_args()
    convert_to_names(args.input_file, args.lookup_csv)