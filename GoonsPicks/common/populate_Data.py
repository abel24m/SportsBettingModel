

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