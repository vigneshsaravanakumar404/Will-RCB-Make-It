from Methods import iterate, get_standings, get_matches, Update
from prettytable import PrettyTable
from copy import deepcopy
from pprint import pprint
from os import system


# Constants
N_probabilities_NONRR = {
    "Rajasthan Royals": 0,
    "Royal Challengers Bengaluru": 0,
    "Kolkata Knight Riders": 0,
    "Mumbai Indians": 0,
    "Lucknow Super Giants": 0,
    "Gujarat Titans": 0,
    "Punjab Kings": 0,
    "Chennai Super Kings": 0,
    "Delhi Capitals": 0,
    "Sunrisers Hyderabad": 0,
}
N_probabilities_NRR = deepcopy(N_probabilities_NONRR)
can_qualify = {
    "Rajasthan Royals": False,
    "Royal Challengers Bengaluru": False,
    "Kolkata Knight Riders": False,
    "Mumbai Indians": False,
    "Lucknow Super Giants": False,
    "Gujarat Titans": False,
    "Punjab Kings": False,
    "Chennai Super Kings": False,
    "Delhi Capitals": False,
    "Sunrisers Hyderabad": False,
}
TOP = 4


# Update()
system("clear")
teams = get_standings()
matches = get_matches()[:-4]
total = 2 ** len(matches)

# No Winner
N_probabilities_NONRR, N_probabilities_NRR = iterate(
    total,
    teams,
    matches,
    TOP,
    N_probabilities_NONRR,
    N_probabilities_NRR,
)


# Parse Probabilities
N_probabilities_NRR = dict(
    sorted(N_probabilities_NRR.items(), key=lambda x: x[1], reverse=True)
)
for team in N_probabilities_NONRR:
    if N_probabilities_NONRR[team] > 0:
        can_qualify[team] = True
    N_probabilities_NONRR[team] /= total
    N_probabilities_NONRR[team] = "{:.5f}".format(N_probabilities_NONRR[team] * 100)

for team in N_probabilities_NRR:
    N_probabilities_NRR[team] /= total
    N_probabilities_NRR[team] = "{:.5f}".format(N_probabilities_NRR[team] * 100)

# Create Table
table = PrettyTable()
table.field_names = [
    "Team",
    "NRR Probability",
    "No NRR Probability",
    f"Can Reach Top {TOP}",
]
for team in N_probabilities_NRR:
    table.add_row(
        [
            team,
            N_probabilities_NRR[team],
            N_probabilities_NONRR[team],
            can_qualify[team],
        ]
    )
print(table)
