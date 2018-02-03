from simanneal import Annealer
import random

class TablingAnnealer(Annealer):
    members = []
    availabilities = {}
    overlaps = {}
    max_people_per_slot = -1

    def __init__(self, members_arg, state, avail_arg, overlap_arg, max_people):
        self.members = members_arg
        # print("number of members: " + str(len(self.members)))
        self.availabilities = avail_arg
        self.overlaps = overlap_arg
        self.max_people_per_slot = max_people
        super(TablingAnnealer, self).__init__(state)

    def move(self):
        valid_move = False
        random_person = ""
        random_slot = -1
        count = 0
        while not valid_move and count < 100:
            random_person = random.choice(self.members)
            random_slot = random.choice(self.availabilities[random_person])
            for slot_number, slot in enumerate(self.state):
                if random_person in slot:
                    current_slot = slot_number
            if len(self.state[random_slot]) + 1 > self.max_people_per_slot or len(self.state[current_slot]) <= 2:
                valid_move = False
            else:
                valid_move = True
            count += 1
        if valid_move:
            self.state[current_slot].remove(random_person)
            self.state[random_slot].append(random_person)

    def energy(self):
        energy_value = 0
        for slot in self.state:
            for member_1 in slot:
                for member_2 in slot:
                    if member_2 in self.overlaps[member_1]:
                        energy_value += 1
        return energy_value