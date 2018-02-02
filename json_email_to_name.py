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

input_file = "some_file.json" # make sure the input file is there!
lookup_file = "lookup.csv"
dictionary = {} # contains the contents of the input file as a python dictionary
lookup_table = {} # contain "email": "First Last" pairs

#populate the lookup_table with contents of lookup.csv
with open(lookup_file, 'rb') as f:
	for line in csv.reader(f):
		lookup_table[line[0]] = line[1]

# read the json file (yep its that ez man)
with open(input_file, 'r') as f:
	dictionary = json.load(f)

# go thru the dictionary, replace emails with names
for row in dictionary[0]:
	for i, val in enumerate(row):
		row[i] = lookup_table[val]

# write back into the json file (yep ez ikr)
with open(input_file, 'w') as f:
	json.dump(dictionary, f)
