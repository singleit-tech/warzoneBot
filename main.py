# bot.py
import os
from api.api import Api
import logging
import traceback
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

intents = discord.Intents.default()
intents.members = True
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logging.debug('Logged in as')
    logging.debug(bot.user.name)
    logging.debug(bot.user.id)
    logging.debug('------')

@bot.command(name="stats", help="User this command to check your WZ stats with '!stats me'\
    or check on other users from this server with '!stats <username>")
async def stats(ctx):
    try:
        user = ctx.message.content.split(" ")[1]

        if(user == "me"):
            user = ctx.author.name

        response = Api(user).get_player_stats();
        if("error" in response.keys()):
            await ctx.send("```diff\n- {}```".format(response['error']))
        else:
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
        
        user = ctx.author.name
        if(" " in ctx.message.content):
            args = ctx.message.content.split(" ")[1]
        else:
            args = ""
        if(args == "me" or args == ""):
            gulag="N/A"
            response = Api(user).get_last_match()
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