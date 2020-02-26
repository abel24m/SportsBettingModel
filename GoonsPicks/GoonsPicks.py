# decoding=utf-8
import requests
import json
import pandas as pd
import sys
import time
import collections
import common.populate_Data as popData
import common.calculate_Data as calData
from decimal import Decimal
from datetime import date

def fixSyntax(team):
    if "State" in team:
        team = team.replace("State", "St")
    if "Mississippi" in team:
        team = team.replace("Mississippi" , "Miss")
    if "Jose" in team:
        team = team.replace("Jose", "Jose" + u'\u0301')
    return team

today = date.today()

sportsrada_key = "8pw73uw6jd2wvkarxwzaz5m5"
odds_key = "189cc69465aaa4b4dba10a780904b03f"

season_url = "https://api.sportradar.us/ncaamb/trial/v4/en/games/2019/reg/schedule.json?api_key=" + sportsrada_key
daily_url = "https://api.sportradar.us/ncaamb/trial/v4/en/games/" + str(today.year) +  "/" + str(today.month) + "/" +  str(today.day) + "/schedule.json?api_key=" + sportsrada_key
odds_url = "https://api.the-odds-api.com/v3/odds/?sport=basketball_ncaab&region=us&mkt=spreads&apiKey=" + odds_key

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
odds_response = requests.get(odds_url)


if daily_response.status_code != 200:
    print(str(daily_response) + " daily")
    sys.exit()

if season_response.status_code != 200:
    print(str(season_response) + " season")
    sys.exit()

if odds_response.status_code !=200:
    print(str(odds_response) + " odds")
    sys.exit() 



daily_data = daily_response.text
season_data = season_response.text
odds_data = odds_response.text

daily_parsed = json.loads(daily_data)
season_parsed = json.loads(season_data)
odds_parsed = json.loads(odds_data)

# print(json.dumps(daily_parsed, indent=4))


dailyGames = daily_parsed["games"]
seasonGames = season_parsed["games"]
odds = odds_parsed["data"]

# print(dir(games))

count = 0
# Iterate through every team playing today and create a dictionary of all of its passed games
# and define whether they won or lost and by how much
spreads = []
for dailyGame in dailyGames:
    count += 1
    team1 = dailyGame["away"]["name"]
    team1Dict ={}
    # print(dailyGame["away"]["name"])
    team2 = dailyGame["home"]["name"]
    team2Dict = {}
    # print(dailyGame["home"]["name"])

    for seasonGame in seasonGames :
        # Only iterate to the games that have been played.
        # Limit the amount of iterations.
        if seasonGame["status"] == "scheduled" :
            break
        elif seasonGame["status"] == "closed":
            if seasonGame["home"]["name"] == team1:
                popData.populateGameDataHome(seasonGame, team1Dict)
            elif seasonGame["away"]["name"] == team1:
                popData.populateGameDataAway(seasonGame, team1Dict)
            elif seasonGame["home"]["name"] == team2:
                popData.populateGameDataHome(seasonGame, team2Dict)
            elif seasonGame["away"]["name"] == team2:
                popData.populateGameDataAway(seasonGame, team2Dict)

    calData.calculateWinner(team1, team2,team1Dict, team2Dict, spreads)

count = 0

def findDifference(mySpread, lvSpread):
    lvSpread = Decimal(lvSpread)
    diff = 0
    if mySpread > 0 :
        if lvSpread < 0:
            diff = lvSpread - mySpread
        else :
            diff = lvSpread - mySpread
    elif mySpread < 0 :
        if lvSpread > 0:
            diff = lvSpread - mySpread
        else :
            diff = lvSpread - mySpread
    return diff

for game_spread in reversed(spreads):
    game_spread[0] = fixSyntax(game_spread[0])
    game_spread[1] = fixSyntax(game_spread[1])
    odd_not_exist = 1
    for lv_odd in odds:
        if game_spread[0] in lv_odd["teams"]:
            if lv_odd["sites_count"] != 0 :
                index = lv_odd["teams"].index(game_spread[0])
                vegas_spread = lv_odd["sites"][0]["odds"]["spreads"]["points"][index]
                game_spread.append(vegas_spread)
                game_spread.append(Decimal(vegas_spread)*-1)
                game_spread.append(findDifference(game_spread[2], vegas_spread))
                game_spread.append(findDifference(game_spread[3], Decimal(vegas_spread)*-1))
            odd_not_exist = 0
            count += 1
            break
        elif game_spread[1] in lv_odd["teams"]:
            if lv_odd["sites_count"] != 0 :
                index = lv_odd["teams"].index(game_spread[1])
                vegas_spread = lv_odd["sites"][0]["odds"]["spreads"]["points"][index]
                game_spread.append(Decimal(vegas_spread)*-1)
                game_spread.append(vegas_spread)
                game_spread.append(findDifference(game_spread[2], vegas_spread))
                game_spread.append(findDifference(game_spread[3], vegas_spread))
            odd_not_exist = 0
            count += 1
            break
    if odd_not_exist:
        spreads.remove(game_spread)

lock = collections.namedtuple('lock',['Team', 'MySpread', 'Vegasline', 'Diff'])

# for game_spread in spreads:
#     if 

LOD = []
for spread in spreads:
    if len(spread) >= 5:
        for x in range(6,8): 
            if len(LOD) < 3:
                LOD.append(lock(spread[x-6],spread[x-4],spread[x-2],spread[x]))
            elif spread[x] > LOD[0].Diff :
                if x == 6:
                    LOD.insert(0,lock(spread[0],spread[2],spread[4],spread[6]))
                if x == 7:
                    LOD.insert(0,lock(spread[1],spread[3],spread[5],spread[7]))
            elif spread[x] > LOD[1].Diff :
                if x == 6:
                    LOD.insert(1,lock(spread[0],spread[2],spread[4],spread[6]))
                if x == 7:
                    LOD.insert(1,lock(spread[1],spread[3],spread[5],spread[7]))
            elif spread[x] > LOD[2].Diff :
                if x == 6:
                    LOD.insert(2,lock(spread[0],spread[2],spread[4],spread[6]))
                if x == 7:
                    LOD.insert(2,lock(spread[1],spread[3],spread[5],spread[7]))
            if len(LOD) > 3:
                LOD.pop()
for x in range(0,4):
    print("")
print("Your locks of the day BIG DAWG")
print("==================================")
for lock in LOD:
        print(lock)
print"===================================="
print("             Goodluck DEGEN")

for x in range(0,4):
    print("")
sys.exit()
sys.exit()



