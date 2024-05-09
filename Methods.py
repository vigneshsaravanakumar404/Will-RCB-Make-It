from collections import OrderedDict
from bs4 import BeautifulSoup
from copy import deepcopy
from requests import get
from json import loads
from tqdm import tqdm

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


def iterate(
    total: int,
    teams: dict,
    matches: list,
    TOP: int,
    probabilities_NONRR: dict,
    probabilities_NRR: dict,
):
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
                standings.items(),
                key=lambda x: (x[1]["Points"], x[1]["NRR"]),
                reverse=True,
            )
        )

        # If the team is top 4 or tied for top 4 then add 1
        fourth_points = list(standings.values())[TOP - 1]["Points"]
        for team in standings:
            if standings[team]["Points"] >= fourth_points:
                probabilities_NONRR[team] += 1

        top_4 = list(standings.keys())[:TOP]
        for team in top_4:
            probabilities_NRR[team] += 1

    return probabilities_NONRR, probabilities_NRR


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

    response = open("Response.json", "r").read()
    response = loads(response)

    upcoming_matches = []
    matchDetailsMap = response.get("matchDetails", [])
    for matchDetails in matchDetailsMap:
        temp = matchDetails.get("matchDetailsMap", None)
        if temp is not None:
            matches = temp.get("match", [])
            for match in matches:
                if match.get("matchInfo", {}).get("state") in [
                    "Upcoming",
                    "In Progress",
                    "Preview",
                ]:
                    team1_id = int(match["matchInfo"]["team1"]["teamId"])
                    team2_id = int(match["matchInfo"]["team2"]["teamId"])
                    upcoming_matches.append([TEAMS[team1_id], TEAMS[team2_id]])

    return upcoming_matches
