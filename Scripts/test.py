import requests
import json
import pandas as pd
import sys
import time
from datetime import date

def populateGameDataHome(seasonGame, teamDict):
    awayteam = seasonGame["away"]["alias"]
    awaypoints = seasonGame["away_points"]
    homepoints = seasonGame["home_points"]
    diff = abs(homepoints - awaypoints)
    outcome = ''
    if homepoints > awaypoints:
        outcome = 'w'
    else:
        outcome = 'l'
    teamDict[awayteam] = [outcome, diff]


def populateGameDataAway(seasonGame, teamDict):
    hometeam = seasonGame["home"]["alias"]
    awaypoints = seasonGame["away_points"]
    homepoints = seasonGame["home_points"]
    diff = abs(homepoints - awaypoints)
    outcome = ''
    if homepoints < awaypoints:
        outcome = 'w'
    else:
        outcome = 'l'
    teamDict[hometeam] = [outcome, diff]


def calculateWinner(team1, team2, team1Dict, team2Dict):
    team1score = 0
    team2score = 0
    running_spread =[]
    for oppTeam1 in team1Dict:
        for oppTeam2 in team2Dict:
            if oppTeam1 == oppTeam2:
                if team1Dict[oppTeam1][0] == 'w' and team2Dict[oppTeam2][0] == 'l':
                    running_spread.append(-(team1Dict[oppTeam1][1] + team2Dict[oppTeam2][1]))
                    team1score += 2
                elif team1Dict[oppTeam1][0] == 'l' and team2Dict[oppTeam2][0] == 'w':
                    running_spread.append((team2Dict[oppTeam2][1] + team1Dict[oppTeam1][1]))
                    team2score += 2
                else:
                    if team1Dict[oppTeam1][0] == 'w':
                        if team1Dict[oppTeam1][1] > team2Dict[oppTeam2][1]:
                            running_spread.append(-(team1Dict[oppTeam1][1] - team2Dict[oppTeam2][1]))
                            team1score += 1
                        elif team1Dict[oppTeam1][1] < team2Dict[oppTeam2][1]:
                            running_spread.append((team2Dict[oppTeam2][1] - team1Dict[oppTeam1][1]))
                            team2score += 1
                    if team1Dict[oppTeam1][0] == 'l':
                        if team1Dict[oppTeam1][1] < team2Dict[oppTeam2][1]:
                            running_spread.append(-(team1Dict[oppTeam1][1] - team2Dict[oppTeam2][1]))
                            team1score += 1
                        elif team1Dict[oppTeam1][1] > team2Dict[oppTeam2][1]:
                            running_spread.append((team2Dict[oppTeam2][1] - team1Dict[oppTeam1][1]))
                            team2score += 1
    spread = 0
    for diff in running_spread:
        spread += diff

    spread = spread/len(running_spread)
    print(str(team1score) + " vs " + str(team2score))

    if spread > 0 :
        print ("spread: +" + str(spread))
    else :
        print ("spread: " + str(spread))


today = date.today()
print("today is = ", today)
print(dir(today))
print()
print(today.day)


sportsrada_key = "8pw73uw6jd2wvkarxwzaz5m5"
odds_key = "189cc69465aaa4b4dba10a780904b03f"

season_url = "https://api.sportradar.us/ncaamb/trial/v4/en/games/2019/reg/schedule.json?api_key=" + sportsrada_key
daily_url = "https://api.sportradar.us/ncaamb/trial/v4/en/games/" + str(today.year) +  "/" + str(today.month) + "/" +  str(today.day) + "/schedule.json?api_key=" + sportsrada_key



daily_response = requests.get(daily_url)
time.sleep(1)
season_response = requests.get(season_url)


if daily_response.status_code != 200:
    print(str(daily_response) + " daily")
    sys.exit()

if season_response.status_code != 200:
    print(str(season_response) + " season")
    sys.exit()



daily_data = daily_response.text
season_data = season_response.text

daily_parsed = json.loads(daily_data)
season_parsed = json.loads(season_data)

# print(json.dumps(daily_parsed, indent=4))


dailyGames = daily_parsed["games"]
seasonGames = season_parsed["games"]

# print(dir(games))

count = 0
# Iterate through every team playing today and create a dictionary of all of its passed games
# and define whether they won or lost and by how much
for dailyGame in dailyGames:
    count += 1
    team1 = dailyGame["away"]["alias"]
    team1Dict ={}
    print(dailyGame["away"]["name"])
    team2 = dailyGame["home"]["alias"]
    team2Dict = {}
    print(dailyGame["home"]["name"])
    for seasonGame in seasonGames :
        # Only iterate to the games that have been played.
        # Limit the amount of iterations.
        if seasonGame["status"] == "scheduled" :
            break
        elif seasonGame["status"] == "closed":
            if seasonGame["home"]["alias"] == team1:
                populateGameDataHome(seasonGame, team1Dict)
            elif seasonGame["away"]["alias"] == team1:
                populateGameDataAway(seasonGame, team1Dict)
            elif seasonGame["home"]["alias"] == team2:
                populateGameDataHome(seasonGame, team2Dict)
            elif seasonGame["away"]["alias"] == team2:
                populateGameDataAway(seasonGame, team2Dict)
    calculateWinner(team1, team2,team1Dict, team2Dict)

print(count)
