# Tabling Scheduler for Berkeley PBL

A set of Python scripts that schedule tabling shifts for PBL members, based on
schedule preferences and the officer constraint (at least one officer per timeslot).
Each week, it tries to minimize the total number of people tabling together who have
tabled together in the past.

## Requirements

* Requires `python` version 3.0+
* `sudo pip install numpy`
* `sudo pip install simanneal` 

## Installation

1. Install the requirements above
2. Either clone this repo or download ZIP and unzip the repo.
3. Navigate into the repo's main directory (./TablingScheduler).

## Usage

Given an input file `week1.json` of member data (tabling preferences, officer/CM, etc.),
run the following command to generate a scheduling for one week:

```
py tabling_annealer.py \path\to\week1.json \path\to\out_week1.json
```

Following the completion of that week's tabling, run `tabling_reporter.py` as many times
as needed to report no-shows and tabling swaps that happened during that week.

```
py tabling_reporter.py \path\to\out_week1.json --noshow "Vanessa Lin" 0
py tabling_reporter.py \path\to\out_week1.json --noshow "Jessica Tzeng" 14
py tabling_reporter.py \path\to\out_week1.json --swap "Eliot Hsu" 3 "Corey Gibbel" 9
```

This set of commands would indicate the following:
* Vanessa Lin did not show up to her tabling slot on Monday at 10am
* Jessica Tzeng did not show up to her tabling slot on Thursday at 12pm
* Eliot Hsu, originally scheduled on Monday at 1pm, swapped with Corey Gibbel,
	who was originally scheduled on Wednesday at 11am

The numbers next to each name represent the "tabling slot number" to which each person
was originally assigned. The "tabling slot number" can be found by counting the number
of slots that have preceeded that slot in the week: 0 for Monday at 10am, 1 for Monday
at 11am, etc. up to 19 for Friday at 1pm.

Finally, to save this schedule to memory (remembering who has tabled with whom for
future weeks), run:

```
py tabling_writer.py \path\to\out_week1.json \path\to\week1.json \path\to\week2.json
```

This will generate a JSON file at `\path\to\week2.json` that is valid as input to
`tabling_annealer.py`, such that the entire process above can be repeated for future weeks.

## Computer Science Background

Tabling Scheduling for PBL is a generalization of the [Nurse Scheduling Problem](https://en.wikipedia.org/wiki/Nurse_scheduling_problem),
and as such has NP-Hard complexity. This specific set of algorithms performs the following general steps:
1. Greedy solution (can fail in edge cases) to schedule one officer to each tabling slot:
	* Order all officers in ascending order of number of availabilities (chosen tabling slots)
	* Attempt to place each officer in this list into an unfilled slot from their availabilities
2. Greedy solution to construct a valid scheduling of all members:
	* Order members (who are not officers on duty) by number of availabilities
	* Attempt to place each member in a slot from their availabilities that is not full
3. Run [simulated annealing](https://en.wikipedia.org/wiki/Simulated_annealing) to minimize the total
number of people tabling together who have tabled together in the past.
	* One "move" is defined by moving a random member (not an officer on duty) to a random
		tabling slot that they have expressed as an availability.
	* The "energy" of each state is defined as: for each member, count the number of people in their
		tabling slot that have tabled with them before. Sum this quantity over all members. Simulated
		annealing will attempt to minimize this quantity by "moving" between states.