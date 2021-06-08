# bot.py
import os
from api.api import Api
import logging
import traceback
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import timeit
from api.canvas_manipulation import Canvas
import io

intents = discord.Intents.default()
intents.members = True
load_dotenv()

"""
    You have 2 options
     1. You'll need to create a .env file to store your discord Token
     2. You can simply paste the TOKEN string instead of os.getenv('DISCORD_TOKEN') 
"""
TOKEN = os.getenv('DISCORD_TOKEN') 

bot = commands.Bot(command_prefix='!', intents=intents)

### LOGGING CONFIG JUST TO CHECK ON SOEM OUTPUT
logging.basicConfig(level=logging.INFO, datefmt="%H:%M:%S",
                      format='[%(levelname)s] %(asctime)s (%(threadName)-9s) (%(processName)-9s) %(message)s')

@bot.event
async def on_ready():
    logging.info('Logged in as')
    logging.info(bot.user.name)
    logging.info(bot.user.id)
    logging.info('------')

@bot.command(name="stats", help="User this command to check your WZ stats with '!stats me'\
    or check on other users from this server with '!stats <username>")
async def stats(ctx):
    try:
        start_time = timeit.default_timer()
        user = ctx.message.content.split(" ")[1]

        if(user == "me"):
            user = ctx.author.name

        response = Api(user).get_player_stats();
        #stats_card = Canvas.user_canvas(response)
        #f = io.BytesIO()
        #stats_card.save(f, format='PNG')
        end_time = timeit.default_timer() - start_time
        logging.info(f'Elapsed Time : {end_time} seconds')
        if("error" in response):
            await ctx.send("```diff\n- {}```".format(response['error']))
        else:
           # f.seek(0)
           # await ctx.send(file=discord.File(f, "stats.png"))
            await ctx.send("**{}**'s stats:\n"
                    "\t> **Level** : {}\n\t> **Wins** : {}\n"
                    "\t> **Kills** : {}\n\t> **Deaths** : {}\n\t> **K/D Ratio** : {:.2f}\n"
                    "\t> **Score Per Minute** : {:.2f}\n"
                    "\t> **Games Played** : {}\n"
                    "\t> **Placed Top 10** : {} times".format(response['username'], response['level'],
                                                    response['wins'], response['kills'],
                                                    response['deaths'], response['kdRatio'],
                                                    response['scorePerMinute'], response['gamesPlayed'],
                                                    response['topTen']))
    except Exception :
        help="Use this command to check your WZ stats with ```!stats me``` or check on other users from this server with ```!stats <username>```"
        traceback.print_exc()
        await ctx.send(help) 

@bot.command(name="lm")
async def last_match(ctx):
    try:
        start_time = timeit.default_timer()
        user = ctx.author.name
        if(" " in ctx.message.content):
            args = ctx.message.content.split(" ")[1]
        else:
            args = ""
        if(args == "me" or args == ""):
            gulag="N/A"
            response = Api(user).get_last_match()
            end_time = timeit.default_timer() - start_time
            logging.info(f'Elapsed Time : {end_time} seconds')
            if(response['gulag'] is not None):
                    if(response['gulag'] == True):
                        gulag = "Win"
                    elif(not response['gulag']):
                        gulag = "Loss"
            else:
                gulag = "N/A"
                
            await ctx.send("**{}**'s last match stats:\n"
                        "\t> **Match Rank** : {}\n"
                        "\t> **Position** : {}\n"
                        "\t> **kiils** : {}\n"
                        "\t> **Deaths** : {}\n"
                        "\t> **Damage** : {}\n"
                        "\t> **Gulag** : {}".format(response['username'], response['rank'], response['position'],
                                                        response['kills'], response['deaths'],response['damage'],gulag))
        elif(args == "team"):
            response = Api(user).get_last_team_match()
            end_time = timeit.default_timer() - start_time
            logging.info(f'Elapsed Time : {end_time} seconds')
            leaderboard = ""
            gulag = "N/A"
            players = response['players'];
            print(players)
            for player in players:
                if(player['gulag'] is not None):
                    if(player['gulag'] == True):
                        gulag = "Win"
                    elif(not player['gulag']):
                        gulag = "Loss"
                else:
                    gulag = "N/A"
                    
                leaderboard += """\t> **Player** : **{}**
                \t> \t **kills** : {}\t **Deaths** : {}\t **K/D Ratio** : {:.2f}\t **Damage Given** : {}
                \t> \t **Headshots** : {}\t **Gulag** : {}\n""".format(player['username'], player['kills'], player['deaths'], player['kdRatio'], player['damageDone'], player['headshots'], gulag) 
            
            await ctx.send("**LAST MATCH TEAM STATS**:\n"
                            "**Team Placement** : {}\t**Total kills** : {}\t**Total Deaths** : {}\t **Total Damage Given** : {}\n"
                            "".format(
                response['team']['placement'], response['team']['kills'], response['team']['deaths'], response['team']['totalDamageDone']
            ))
            #print(leaderboard)
            await ctx.send(leaderboard)

    except Exception as e:
        traceback.print_exc()
        await ctx.send("An Error Occurred retrieving match data")



bot.run(TOKEN)