import argparse
import json
import numpy as np

class TablingReporter():

    def __init__(self, schedule_file, output_file, noshow, swap):
        self.schedule = json.load(open(schedule_file))
        self.output_file = output_file
        self.member_list = self.flatten(self.schedule)
        print(self.member_list)
        if noshow != None:
            noshow = noshow[0]
            noshow.strip("\"")
            self.report_noshow(noshow)

        self.write_schedule(schedule_file)
        if output_file != None:
            self.write_output()

    def report_noshow(self, name):
        if name not in self.member_list:
            print("\"" + name + "\"" + " not in list of members.")
            return
        for day in self.schedule:
            for slot in day:
                if name in slot:
                    slot.remove(name)
                    return

    def write_schedule(self, schedule_file):
        print(self.schedule)
        with open(schedule_file, 'w') as out:
            json.dump(self.schedule, out)

    def write_output(self):
        print("meh")

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
            # else:
            #     raise Exception("Not a list or string: {}".format(item))
        return results

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Tabling Reporter", epilog = "Tabling slot number is as follows: 0 for 10-11am Monday, 1 for 11am-12pm Monday... 4 for 10-11am Tuesday, and so on")
    parser.add_argument("week_schedule", type=str, help = "Weekly schedule to modify, JSON")
    parser.add_argument("-w", "--outfile", type=str, help = "Write output to member data file, JSON")
    parser.add_argument("--noshow", nargs=2, type=str, help = "Report a no-show: --noshow \"Name of person\" [tabling slot number]")
    parser.add_argument("-s", "--swap", nargs=2, type=str, help = "Report a tabling swap")
    args = parser.parse_args()
    scheduler = TablingReporter(args.week_schedule, args.outfile, args.noshow, args.swap)