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

## Generating scheduling

If you run into any issues during this process, contact a member of PBL Dev Team.

1. Download [tabling form responses](https://docs.google.com/spreadsheets/d/1bg3mOqfKi4cB4Kx4sWjYDtvruGovoVpfo7QhI0eWaYE/edit#gid=1206364764) as a `.csv` using *File* -> *Download as* -> *Comma-separated values (.csv, current sheet)*
2. Put the `.csv` file in the same folder as this repo, and rename it to remove spaces (try `tablingform.csv`)
3. Run `py csv_to_json.py [tablingform.csv] [memberdata.json]`, where the first argument is the name (and path) to the `.csv` file from the last step, and `[memberdata.json]` is the name of the `.json` file you'd like to write all member data to; this can either be an existing file (including all previous member data) or a new file
4. Run `py tabling_annealer.py [memberdata.json] [week_schedule.json]` to generate a tabling schedule at `week_schedule.json`
5. Run `py tabling_writer.py [memberdata.json] [week_schedule.json]` to write tabled_with data to `memberdata.json`
6. Run `py json_email_to_name.py [week_schedule.json] [lookup.csv]`, where `lookup.csv` is the email-name lookup file from this repo, to convert the weekly schedule (currently written with emails) to names
7. Copy the contents of `[week_schedule.json]` into BerkeleyPBLTech's repo in ./js/main.js at line 13, next to `var json = ...`. Run the following commands:
```
git add -A
git commit -m "Updating weekly tabling"
git push
```
to propagate the newly generated weekly schedule to [the tabling webpage](https://berkeleypbltech.github.io/PBLPortal/). That's it!

## In-Depth Usage (Partially outdated)

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

Note, tabling_reporter is outdated, as the tabling schedule is currently stored by
name, whereas member data is stored by email.

Finally, to save this schedule to memory (remembering who has tabled with whom for
future weeks), run:

```
py tabling_writer.py \path\to\week1.json \path\to\out_week1.json
```

This will generate a JSON file at `\path\to\week1.json` that is valid as input to
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