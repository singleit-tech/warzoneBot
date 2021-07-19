import requests
import json
import os
import traceback

from requests.api import request
from dotenv import load_dotenv
from .team_builder import Team


USER_DICT = {
        "singleit" : "SINGLE#21357"
    }

def assign_rank(avg, mode):
        rank = 'Not Ranked Yet'
        with open('rank.json') as json_file:        
            data = json.load(json_file)
            for item in data[mode]:
                if(item['lowerBound'] < avg and avg < item['upperBound']):
                    rank = str(item['metal']) + ' ' + str(item['number'])
        return rank

class Stats:

    def __init__(self, username, level, wins, kills, deaths, topTen, kdRatio, scorePerMinute, gamesPlayed):
        self.username = username
        self.level = level
        self.wins = wins
        self.kills = kills
        self.deaths = deaths
        self.topTen = topTen
        self.kdr = kdRatio
        self.spm = scorePerMinute
        self.gp = gamesPlayed
    
class Player:

    def __init__(self, username, kills, deaths, damageDone, headshots, kdRatio, gulag):
        self.username = username
        self.kills = kills
        self.deaths = deaths
        self.damageDone = damageDone
        self.headshots = headshots
        self.gulag = gulag

class Match:

    def __init__(self, players, placement):
        self.players = players
        self.placement = placement
        

class Api:
    

    def __init__(self, user):
        self.user = user
    
    

    def get_player_stats(self):
        try:
            user = USER_DICT[str(self.user).lower()]
            stats_url = 'https://app.wzstats.gg/v2/player?username={}&platform=battle'.format(user.replace('#', '%23'))
            #print(stats_url)
            response = self.get(stats_url)
            response_json = response.json()
            stats = Stats(
                username=response_json['data']['uno'], 
                level=response_json['data']['level'],
                wins=response_json['data']['lifetime']['mode']['br']['properties']['wins'],
                kills=response_json['data']['lifetime']['mode']['br']['properties']['kills'],
                deaths=response_json['data']['lifetime']['mode']['br']['properties']['deaths'],
                topTen=response_json['data']['lifetime']['mode']['br']['properties']['topTen'],
                kdRatio=response_json['data']['lifetime']['mode']['br']['properties']['kdRatio'],
                scorePerMinute=response_json['data']['lifetime']['mode']['br']['properties']['scorePerMinute'],
                gamesPlayed=response_json['data']['lifetime']['mode']['br']['properties']['gamesPlayed'])

            return stats
        except Exception as e:
            traceback.print_exc()
            response_dict = {"error" : "Couldn't find data for the user {}".format(self.user)}
            return response_dict
        
    def get_last_match(self):
        try:
            user = USER_DICT[str(self.user).lower()]
            match_url = 'https://app.wzstats.gg/v2/player/match?username={}&platform=battle'.format(user.replace('#', '%23'))
            print(match_url)
            response = self.get(match_url)
            
            response_json = response.json()[0]
            
            avg = response_json['matchStatData']['playerAverage']
            rank = assign_rank(avg, response_json["matchStatData"]["mode"])
            
            players = {}
            for player in response_json["matchTeamStat"]["players"]:
                
                player = Player(
                    username = player['username'],
                    kills = player['kills'],
                    deaths = player['deaths'],
                    kdRatio = int(player['kills'] / player['deaths']),
                    damageDone = player['damageDone'],
                    headshots = player['headshots'],
                    gulag = player["gulag"] if "gulag" in player.keys() else "-",
                )
                players[player.username] = player
            
            
            match = Match(players, response_json["teamPlacement"])
            return match

        except Exception as e:
            traceback.print_exc()
            print("LM : {}".format(match_url))
    
    def get_last_team_match(self):
        try:
            user = USER_DICT[str(self.user).lower()]
            match_url = 'https://app.wzstats.gg/v2/player/match?username={}&platform=battle'.format(user.replace('#', '%23'))
            response = self.get(match_url)
            match_id = response.json()[0]['id']
            if(response.json()[0]['mode'] == "br_brsolos"):
                response_dict = {"message" : "br_brsolos"}
            else:
                stats_url = 'https://app.wzstats.gg/v2/?matchId={}&player={}'.format(match_id, user.replace('#', '%23'))
                stats = self.get(stats_url)
                response_json = stats.json()['data']['players']
                team = Team(response_json).build(user)
                
            return team
        except Exception as e:
            traceback.print_exc()
            print("TEAM : {}".format(stats_url))


    

    def get(self, url):
        return requests.request("GET", url)
#curl --location --request GET 'https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/battle/gamer/iShot%2321899/profile/type/mp'

#email = os.getenv('BATTLE_NET_EMAIL');
#password = os.getenv('BATTLE_NET_PW')


#print(response.text)

