from requests import get
from bs4 import BeautifulSoup
from pprint import pprint
from json import loads
from collections import OrderedDict
from time import sleep
from tqdm import tqdm
from copy import deepcopy


# Constants
STANDINGS_URL = "https://www.espncricinfo.com/series/indian-premier-league-2024-1410320/points-table-standings"
MATCHES_URL = "https://cricbuzz-cricket.p.rapidapi.com/series/v1/7607"
RAPID_API_HEADER = {
    "X-RapidAPI-Key": "625b1f8556mshc64b0a5805ff3cbp10b139jsnb3e7eae49738",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
}
TEAMS = {
    64: "Rajasthan Royals",
    59: "Royal Challengers Bengaluru",
    63: "Kolkata Knight Riders",
    62: "Mumbai Indians",
    966: "Lucknow Super Giants",
    971: "Gujarat Titans",
    65: "Punjab Kings",
    58: "Chennai Super Kings",
    61: "Delhi Capitals",
    255: "Sunrisers Hyderabad",
    106: "Upcoming Team",
}
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


# Parse Data
def get_standings() -> dict:

    response = get(STANDINGS_URL)
    table = BeautifulSoup(response.text, "html.parser").find_all("table")[0]
    rows = table.find_all("tr")

    data = [[data.text for data in row.find_all("td")] for row in rows[1:]]
    data = [data[i] for i in range(len(data)) if i % 2 == 0]

    teams = {}
    for team in data:
        name = "".join(filter(lambda x: x.isalpha() or x.isspace(), team[0]))
        runs_scored = int(team[10].split("/")[0])
        overs_played = (
            int(team[10].split("/")[1].split(".")[0]) * 6
            + int(team[10].split("/")[1].split(".")[1])
        ) / 6
        runs_conceded = int(team[11].split("/")[0])
        overs_bowled = (
            int(team[11].split("/")[1].split(".")[0]) * 6
            + int(team[11].split("/")[1].split(".")[1])
        ) / 6
        teams[name] = {
            "Matches": int(team[1]),
            "Won": int(team[2]),
            "Lost": int(team[3]),
            "Tied": int(team[4]),
            "N/R": int(team[5]),
            "Points": int(team[6]),
            "NRR": float(team[7]),
            "History": team[8],
            "Next": team[9],
            "runs scored": int(runs_scored),
            "overs played": float(overs_played),
            "runs conceded": int(runs_conceded),
            "overs bowled": float(overs_bowled),
        }

    return teams


def get_matches():

    # response = get(MATCHES_URL, headers=RAPID_API_HEADER)
    response = open("Response.json", "r").read()
    response = loads(response)

    upcoming_matches = []
    matchDetailsMap = response.get("matchDetails", [])
    for matchDetails in matchDetailsMap:
        temp = matchDetails.get("matchDetailsMap", None)
        if temp is not None:
            matches = temp.get("match", [])
            for match in matches:
                if match.get("matchInfo", {}).get("state") == "Upcoming":
                    team1_id = int(match["matchInfo"]["team1"]["teamId"])
                    team2_id = int(match["matchInfo"]["team2"]["teamId"])
                    upcoming_matches.append([TEAMS[team1_id], TEAMS[team2_id]])

    return upcoming_matches


teams = get_standings()
matches = get_matches()[:-4]
total = 2 ** len(matches)


for i in tqdm(range(total)):
    standings = deepcopy(teams)
    binary_i = bin(i)[2:].zfill(len(matches))
    array_i = [int(x) for x in binary_i]

    # O(n)
    for j in range(len(array_i)):
        match = matches[j]
        team1 = match[0]
        team2 = match[1]

        if array_i[j] == 0:
            standings[team1]["Points"] += 2
        else:
            standings[team2]["Points"] += 2

    # O(nlogn)
    standings = OrderedDict(
        sorted(
            standings.items(), key=lambda x: (x[1]["Points"], x[1]["NRR"]), reverse=True
        )
    )

    # O(10)
    top_7_teams = list(standings.keys())[:9]
    for team in top_7_teams:
        probabilities[team] += 1


for team in probabilities:
    probabilities[team] /= total

print("\n")
probabilities = dict(sorted(probabilities.items(), key=lambda x: x[1], reverse=True))
for team in probabilities:
    print(f"{team}: {probabilities[team] * 100}")
