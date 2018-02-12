import argparse
import json
import numpy as np
import csv

class TablingWriter():
    lookup = {}

    def __init__(self, schedule_file, data_file, lookup_file):
        self.schedule = json.load(open(schedule_file))
        self.initial_data = json.load(open(data_file))
        self.populate_lookup(lookup_file)
        self.parse_data()
        self.write_data(data_file)

    def populate_lookup(self, lookup_file):
        with open(lookup_file, 'rt') as f:
            for line in csv.reader(f):
                self.lookup[line[0]] = line[1]

    def replace_schedule_with_emails(self):
        print(self.schedule)
        for row in self.lookup:
            for slot in row:
                for i, val in enumerate(slot):
                    if (val in lookup_table):
                        slot[i] = lookup_table[val]
        print(self.schedule)

    def parse_data(self):
        for day in self.schedule:
            for slot in day:
                for member_1 in slot:
                    for member_2 in slot:
                        # print(self.lookup[member_1], self.lookup[member_2])
                        if member_1 != member_2 and self.lookup[member_2] not in self.initial_data[self.lookup[member_1]]["tabled_with"]:
                            self.initial_data[self.lookup[member_1]]["tabled_with"].append(self.lookup[member_2])

    def write_data(self, final_data):
        with open(final_data, 'w') as out:
            json.dump(self.initial_data, out)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Tabling Writer")
    parser.add_argument("data_file", type=str, help = "Members' data file to write to, .json")
    parser.add_argument("week_schedule", type=str, help = "Tabling schedule for the week, JSON")
    parser.add_argument("lookup_filename", type=str, help = "Lookup table for emails and names, .csv")
    # parser.add_argument("final_data", type=str, help = "Final member's data file to write to (AFTER tabling this week)")
    args = parser.parse_args()
    scheduler = TablingWriter(args.week_schedule, args.data_file, args.lookup_filename)