from Methods import graph_iterate, get_standings, get_all_matches, Update
from copy import deepcopy
from pprint import pprint

probabilities = {
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
other_probabilities = deepcopy(probabilities)
points_table = deepcopy(probabilities)

matches = get_all_matches()

print(len(matches))
for i in range(len(matches)):
    points_table[matches[i][2]] += 2
    pprint(points_table)
    probabilities_NONRR, probabilities_NRR = graph_iterate(
        2 ** (len(matches) - i),
        points_table,
        matches[i:],
        4,
        deepcopy(probabilities),
        deepcopy(probabilities),
    )
    pprint(probabilities_NRR)
