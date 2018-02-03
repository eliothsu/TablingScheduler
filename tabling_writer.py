import argparse
import json
import numpy as np

class TablingWriter():

    def __init__(self, schedule_file, data_file):
        self.schedule = json.load(open(schedule_file))
        self.initial_data = json.load(open(data_file))
        self.parse_data()
        self.write_data(data_file)

    def parse_data(self):
        for day in self.schedule:
            for slot in day:
                for member_1 in slot:
                    for member_2 in slot:
                        if member_1 != member_2 and member_2 not in self.initial_data[member_1]["tabled_with"]:
                            self.initial_data[member_1]["tabled_with"].append(member_2)

    def write_data(self, final_data):
        with open(final_data, 'w') as out:
            json.dump(self.initial_data, out)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Tabling Writer")
    parser.add_argument("data_file", type=str, help = "Members' data file to write to, .json")
    parser.add_argument("week_schedule", type=str, help = "Tabling schedule for the week, JSON")
    # parser.add_argument("final_data", type=str, help = "Final member's data file to write to (AFTER tabling this week)")
    args = parser.parse_args()
    scheduler = TablingWriter(args.week_schedule, args.data_file)