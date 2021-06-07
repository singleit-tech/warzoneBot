
class Team:
    def __init__(self, data):
        self.data = data

    def build(self, user):
        #print(user)
        players = []
        team = ""
        for player in self.data:
            if(player['playerStat'] is not None):
                if(player['playerStat']['battle'] == user.lower()):
                    team = player['playerMatchStat']['player']['team']
                
        #sys.exit()
        for player in self.data:
            if(player['playerMatchStat']['player']['team'] == team):
                #print(player)
                
                if(player['playerMatchStat']['playerStats']['deaths'] == 0):
                    kd = player['playerMatchStat']['playerStats']['kills'] / 1
                else:
                    kd = player['playerMatchStat']['playerStats']['kills'] / player['playerMatchStat']['playerStats']['deaths']

                if("gulagWin" in player['playerMatchStat']['playerStats'].keys()):
                    gulag = player['playerMatchStat']['playerStats']['gulagWin']
                else:
                    gulag = None

                players.append(
                        {
                            "username" : player['playerMatchStat']['player']['username'],
                            "kills" : player['playerMatchStat']['playerStats']['kills'],
                            "deaths" : player['playerMatchStat']['playerStats']['deaths'],
                            "kdRatio" : kd,
                            "damageDone" : player['playerMatchStat']['playerStats']['damageDone'],
                            "headshots" : player['playerMatchStat']['playerStats']['headshots'],
                            "gulag" : gulag,
                            "teamPlacement" : player['playerMatchStat']['playerStats']['teamPlacement']
                        }
                    )
        team_dict = {
            "placement" : str(players[0]['teamPlacement']),
            "kills" : 0,
            "deaths" : 0,
            "kdRatio" : 0,
            "totalDamageDone" : 0
        }
        kills = 0
        deaths = 0
        totalDamage = 0
        for player in players:
            kills += int(player['kills'])
            deaths += int(player['deaths'])
            totalDamage += int(player['damageDone'])
        
        
        #print(players)
        team_dict['kills'] = kills
        team_dict['deaths'] = deaths
        team_dict['totalDamageDone'] = totalDamage
        if(int(team_dict['deaths']) == 0):
            team_kd = int(team_dict['kills']) / 1
        else:
            team_kd = int(team_dict['kills']) / int(team_dict['deaths'])
        
        team_dict['kdRatio'] = team_kd

        #print(team_dict)
        team_stats = {
            "team" : team_dict,
            "players" : players
        }
        return team_stats