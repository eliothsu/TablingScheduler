import argparse
import json
import numpy as np

class TablingReporter():
    number_of_days = -1
    slots_per_day = -1

    def __init__(self, schedule_file, output_file, noshow, swap):
        self.schedule = json.load(open(schedule_file))
        self.number_of_days = len(self.schedule)
        self.slots_per_day = len(self.schedule[0])
        self.output_file = output_file
        self.member_list = self.flatten(self.schedule)
        if noshow != None:
            noshow[0].strip("\"")
            self.report_noshow(noshow[0], int(noshow[1]))
        if swap != None:
            swap[0].strip("\"")
            swap[1] = int(swap[1])
            swap[2].strip("\"")
            swap[3] = int(swap[3])
            self.report_swap(swap)
        self.write_schedule(schedule_file)

    def report_noshow(self, name, slot_num):
        self.remove_member(name, slot_num)

    def remove_member(self, name, slot_num):
        self.validate_member_name(name)
        tabling_day = slot_num // self.slots_per_day
        slot = self.schedule[tabling_day][slot_num - tabling_day * self.slots_per_day]
        if name in slot:
            slot.remove(name)
        else:
            print(name + " not found in slot number " + str(slot_num) + ".")

    def add_member(self, name, slot_num):
        self.validate_member_name(name)
        tabling_day = slot_num // self.slots_per_day
        slot = self.schedule[tabling_day][slot_num - tabling_day * self.slots_per_day]
        if name in slot:
            print(name + " already found in slot number " + str(slot_num) + ".")
        else:
            slot.append(name)

    def report_swap(self, swap_data):
        self.validate_member_name(swap_data[0])
        self.validate_member_name(swap_data[2])
        self.remove_member(swap_data[0], swap_data[1])
        self.remove_member(swap_data[2], swap_data[3])
        self.add_member(swap_data[0], swap_data[3])
        self.add_member(swap_data[2], swap_data[1])

    def validate_member_name(self, name):
        if name not in self.member_list:
            raise Exception("\"" + name + "\"" + " not found in list of members.")

    def write_schedule(self, schedule_file):
        with open(schedule_file, 'w') as out:
            json.dump(self.schedule, out)

    def flatten(self, listOfLists):
        """
        Flatten arbitrary levels of nesting for an array of integers.

        Any non list, non int value throws an exception.
        """
        results = []

        for item in listOfLists:
            if isinstance(item, str):
                results.append(item)
            if isinstance(item, list):
                for value in self.flatten(item):
                    results.append(value)
        return results

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Tabling Reporter", epilog = "\"Tabling slot number\" is as follows: 0 for 10-11am Monday, 1 for 11am-12pm Monday... 4 for 10-11am Tuesday, and so on")
    parser.add_argument("week_schedule", type=str, help = "Weekly schedule to modify, JSON")
    parser.add_argument("--outfile", type=str, help = "Write output to member data file: -w week3_data.json")
    parser.add_argument("--noshow", nargs=2, type=str, help = "Report a no-show: --noshow \"Name of person\" [tabling slot number]")
    parser.add_argument("--swap", nargs=4, type=str, help = "Report a tabling swap: -s \"Name 1\" [slot #1] \"Name 2\" [slot #2]")
    args = parser.parse_args()
    scheduler = TablingReporter(args.week_schedule, args.outfile, args.noshow, args.swap)