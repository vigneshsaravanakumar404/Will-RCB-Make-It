from requests import get
from json import dump

STANDINGS_URL = "https://www.espncricinfo.com/series/indian-premier-league-2024-1410320/points-table-standings"
MATCHES_URL = "https://cricbuzz-cricket.p.rapidapi.com/series/v1/7607"
RAPID_API_HEADER = {
    "X-RapidAPI-Key": "625b1f8556mshc64b0a5805ff3cbp10b139jsnb3e7eae49738",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
}


def Update():
    response = get(MATCHES_URL, headers=RAPID_API_HEADER)
    response = response.json()

    with open("Response.json", "w") as f:
        dump(response, f, indent=4)
