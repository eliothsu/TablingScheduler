import argparse
import json
import annealer, officer_annealer
import random
import numpy as np

class Scheduler():
    member_list = []
    data = {}
    max_people_per_slot = 4

    def __init__(self, json_string, outfile):
        self.data = json.load(open(json_string))
        self.outfile = outfile
        self.run_scheduling()

    def run_scheduling(self):
        officer_list, CM_list, availabilities, overlaps, number_of_slots = self.parse_data(self.data)
        officer_schedule = self.run_officer_scheduling(officer_list, availabilities)
        initial_schedule = self.create_initial_schedule(officer_schedule, availabilities, number_of_slots)
        final_schedule = self.run_member_scheduling(officer_schedule, initial_schedule, availabilities, overlaps)
        self.write_output(final_schedule, number_of_slots)

    def parse_data(self, data):
        officer_list = []
        CM_list = []
        availabilities = {}
        overlaps = {}
        number_of_slots = -1
        # print(data)
        for member, member_data in data.items():
            if member_data["officer"] == "True":
                officer_list.append(member)
            else:
                CM_list.append(member)
        random.shuffle(officer_list)
        random.shuffle(CM_list)
        self.member_list = officer_list[:]
        self.member_list.extend(CM_list) # List of all members, with officers first
        # print(member_list)

        for name in self.member_list:
            data[name]["schedule"] = np.ndarray.flatten(np.array(data[name]["schedule"])).tolist()
            # print(data[name]["schedule"])
            availabilities[name] = []
            for i in range(len(data[name]["schedule"])):
                if data[name]["schedule"][i] == "True":
                    availabilities[name].append(i)
            overlaps[name] = data[name]["tabled_with"]
            # print(name + ": " + str(self.overlaps[name]))
            if data[name]["officer"] == "True":
                for i in range(len(data[name]["schedule"]), len(officer_list)):
                    availabilities[name].append(i)
            # print(str(availabilities[name]) + "\n")
        if number_of_slots == -1:
            number_of_slots = len(data[name]["schedule"])

        return officer_list, CM_list, availabilities, overlaps, number_of_slots

    def write_output(self, schedule, number_of_slots):
        out_schedule = []
        slots_per_day = 4
        number_of_days = 5
        for day in range(number_of_days):
            out_schedule.append([])
            for slot in range(number_of_slots // number_of_days):
                out_schedule[day].append(schedule[day*slots_per_day + slot])

        with open(self.outfile, 'w') as out:
            print("Final schedule:")
            print(json.dumps(out_schedule, indent=4))
            json.dump(out_schedule, out)
            
        print("\nWriting schedule to " + self.outfile)

    def run_officer_scheduling(self, officer_list, availabilities):
        print("Running officer scheduling...")
        officer_scheduler = officer_annealer.OfficerAnnealer(officer_list[:], availabilities)
        Tmax = 10.0
        Tmin = 0.01
        steps = 50000
        
        officer_scheduler.Tmax = Tmax
        officer_scheduler.Tmin = Tmin
        officer_scheduler.steps = steps
        officer_scheduler.updates = 1000

        schedule, number_of_schedule_conflicts = officer_scheduler.anneal()
        print("\n")
        if number_of_schedule_conflicts > 0:
            print("Error, invalid scheduling!")
        print(schedule)
        return schedule

    def create_initial_schedule(self, officer_schedule, availabilities, number_of_slots):
        print("\n\nCreating initial schedule...")
        initial_schedule = []
        for member in self.member_list:
            availabilities[member] = [slot for slot in availabilities[member] if slot < number_of_slots]

        new_member_list = self.member_list[:]
        for i in range(number_of_slots):
            new_member_list.remove(officer_schedule[i])
            initial_schedule.append([])

        members = sorted(new_member_list, key=lambda member: len(availabilities[member]))
        while len(members) > 0:
            current_member = members.pop(0)
            found_slot = False
            random.shuffle(availabilities[current_member])
            for slot in availabilities[current_member]:
                if not found_slot and len(initial_schedule[slot]) + 1 < self.max_people_per_slot:
                    initial_schedule[slot].append(current_member)
                    found_slot = True

        for slot_number in range(number_of_slots):
            slot = initial_schedule[slot_number]
            slot.insert(0, officer_schedule[slot_number])

        # print(initial_schedule)
        return initial_schedule

    def run_member_scheduling(self, officer_schedule, initial_schedule, availabilities, overlaps):
        print("\nRunning member scheduling...")
        # print("Officer schedule: " + str(officer_schedule))
        # print("All members: " + str([member for member in self.member_list if member not in officer_schedule]))
        member_scheduler = annealer.TablingAnnealer([member for member in self.member_list if member not in officer_schedule[:20]], initial_schedule[:], availabilities, overlaps, self.max_people_per_slot)
        Tmax = 10.0
        Tmin = 0.1
        steps = 50000
        
        member_scheduler.Tmax = Tmax
        member_scheduler.Tmin = Tmin
        member_scheduler.steps = steps
        member_scheduler.updates = 1000

        final_schedule, _ = member_scheduler.anneal()
        print("\n")
        # print(final_schedule)
        return final_schedule

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Tabling Scheduler")
    parser.add_argument("json_input_file", type=str, help = "___.json")
    parser.add_argument("json_output_file", type=str, help = "___.json")
    args = parser.parse_args()
    scheduler = Scheduler(args.json_input_file, args.json_output_file)