import requests
import json
import os

from requests.api import request
from dotenv import load_dotenv
from .team_builder import Team
import traceback


USER_DICT = {
        "roguezn" : "ROGUEZN#2376",
        "rimaal" : "MATEUS#2434",
        "singleit" : "SINGLE#21357"
    }
class Api:
    

    def __init__(self, user):
        self.user = user
    
    def get_player_stats(self):
        try:
            user = USER_DICT[str(self.user).lower()]
            stats_url = 'https://app.wzstats.gg/v2/player?username={}&platform=battle'.format(user.replace('#', '%23'))
            print(stats_url)
            response = self.get(stats_url)
            response_json = response.json()
            response_dict = {
                "username" : response_json['data']['uno'],
                "level" : response_json['data']['level'],
                "wins" : response_json['data']['lifetime']['mode']['br']['properties']['wins'],
                "kills" : response_json['data']['lifetime']['mode']['br']['properties']['kills'],
                "deaths" : response_json['data']['lifetime']['mode']['br']['properties']['deaths'],
                "topTen" : response_json['data']['lifetime']['mode']['br']['properties']['topTen'],
                "kdRatio" : response_json['data']['lifetime']['mode']['br']['properties']['kdRatio'],
                "scorePerMinute" : response_json['data']['lifetime']['mode']['br']['properties']['scorePerMinute'],
                "gamesPlayed" : response_json['data']['lifetime']['mode']['br']['properties']['gamesPlayed']
            }
            #print(response_dict)
            return response_dict
        except Exception as e:
            traceback.print_exc()
            response_dict = {"error" : "Couldn't find data for the user {}".format(self.user)}
            return response_dict
        
    def get_last_match(self):
        try:
            user = USER_DICT[str(self.user).lower()]
            match_url = 'https://app.wzstats.gg/v2/player/match?username={}&platform=battle'.format(user.replace('#', '%23'))
            response = self.get(match_url)
            response_json = response.json()
            #print(response_json[0])
            if("mode" in response_json[0].keys()):
                mode = response_json[0]['mode']
                avg = response_json[0]['matchStatData']['playerAverage']
                with open('rank.json') as json_file:
                    data = json.load(json_file)
                    for item in data[mode]:
                        if(item['lowerBound'] < avg and avg < item['upperBound']):
                            rank = str(item['metal']) + ' ' + str(item['number'])
            else:
                rank = "Not Ranked Yet"

            if("gulagWin" in response_json[0].keys()):
                gulag = response_json[0]['gulagWin']
            else:
                gulag = ""

            response_dict = {
                "rank" : rank,
                "username" : response_json[0]['username'],
                "position" : response_json[0]['position'],
                "kills" : response_json[0]['kills'],
                "deaths" : response_json[0]['deaths'],
                "damage" : response_json[0]['damage'],
                "gulag" : gulag
            }
            return response_dict
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

