import requests
import json
import pandas as pd
import sys
import time
import common.populate_Data as popData
import common.calculate_Data as calData
from datetime import date



today = date.today()

sportsrada_key = "8pw73uw6jd2wvkarxwzaz5m5"
odds_key = "189cc69465aaa4b4dba10a780904b03f"

season_url = "https://api.sportradar.us/ncaamb/trial/v4/en/games/2019/reg/schedule.json?api_key=" + sportsrada_key
daily_url = "https://api.sportradar.us/ncaamb/trial/v4/en/games/" + str(today.year) +  "/" + str(today.month) + "/" +  str(today.day) + "/schedule.json?api_key=" + sportsrada_key

#-----------------URL's to view response in browswer----------------------#

# Season statistics per team
#https://api.sportradar.us/ncaamb/trial/v7/en/seasons/2019/reg/teams/2f4d21f8-6d5f-48a5-abca-52a30583871a/statistics.json?api_key=8pw73uw6jd2wvkarxwzaz5m5

# Daily games being played
# https://api.sportradar.us/ncaamb/trial/v4/en/games/2020/2/24/schedule.json?api_key=8pw73uw6jd2wvkarxwzaz5m5

# Season to Date games 
# https://api.sportradar.us/ncaamb/trial/v4/en/games/2019/reg/schedule.json?api_key=8pw73uw6jd2wvkarxwzaz5m5

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
                popData.populateGameDataHome(seasonGame, team1Dict)
            elif seasonGame["away"]["alias"] == team1:
                popData.populateGameDataAway(seasonGame, team1Dict)
            elif seasonGame["home"]["alias"] == team2:
                popData.populateGameDataHome(seasonGame, team2Dict)
            elif seasonGame["away"]["alias"] == team2:
                popData.populateGameDataAway(seasonGame, team2Dict)

    calData.calculateWinner(team1, team2,team1Dict, team2Dict)

print(count)
sys.exit()
