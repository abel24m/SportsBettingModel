

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
                # else:
                #     if team1Dict[oppTeam1][0] == 'w':
                #         if team1Dict[oppTeam1][1] > team2Dict[oppTeam2][1]:
                #             running_spread.append(-(team1Dict[oppTeam1][1] - team2Dict[oppTeam2][1]))
                #             team1score += 1
                #         elif team1Dict[oppTeam1][1] < team2Dict[oppTeam2][1]:
                #             running_spread.append((team2Dict[oppTeam2][1] - team1Dict[oppTeam1][1]))
                #             team2score += 1
                #     if team1Dict[oppTeam1][0] == 'l':
                #         if team1Dict[oppTeam1][1] < team2Dict[oppTeam2][1]:
                #             running_spread.append(-(team1Dict[oppTeam1][1] - team2Dict[oppTeam2][1]))
                #             team1score += 1
                #         elif team1Dict[oppTeam1][1] > team2Dict[oppTeam2][1]:
                #             running_spread.append((team2Dict[oppTeam2][1] - team1Dict[oppTeam1][1]))
                #             team2score += 1
    spread = 0
    for diff in running_spread:
        spread += diff

    spread = spread/len(running_spread)
    print(str(team1score) + " vs " + str(team2score))

    if spread > 0 :
        print ("spread: +" + str(spread))
    else :
        print ("spread: " + str(spread))