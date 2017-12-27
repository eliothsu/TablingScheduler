from simanneal import Annealer
import random

class OfficerAnnealer(Annealer):
    officers = [] # List of officer names
    availabilities = {}

    def __init__(self, state, avail_arg):
        self.availabilities = avail_arg
        super(OfficerAnnealer, self).__init__(state)

    def move(self):
        index1, index2 = random.randint(0, len(self.state) - 1), random.randint(0, len(self.state) - 1)
        self.state.insert(index2, self.state.pop(index1))

    def energy(self):
        energy_value = 0
        for i in range(len(self.state)):
            if i not in self.availabilities[self.state[i]]:
                energy_value += 1
        return energy_value