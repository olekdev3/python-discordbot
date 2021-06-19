import discord, os
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError
from commands.logging import log_command

# getsummoner | leaguerankings | addrank

riot_file = open('D:/riotapi.txt','r')
riot_token = riot_file.readline()

watcher = LolWatcher(riot_token)
my_region = 'euw1'

def rank_value(tier, rank, leaguepoints):

    if rank == "I":
        deduction = 0
    elif rank == "II":
        deduction = 1
    elif rank == "III":
        deduction = 2
    elif rank == "IV":
        deduction = 3
    else:
        deduction = 0

    if tier == "IRON":
        raw_value = 4
    elif tier == "BRONZE":
        raw_value = 5
    elif tier == "SILVER":
        raw_value = 6
    elif tier == "GOLD":
        raw_value = 7
    elif tier == "PLATINUM":
        raw_value = 8
    elif tier == "DIAMOND":
        raw_value = 9
    else:
        raw_value = 4

    final_value = ((raw_value * 4) - deduction) + (leaguepoints / 100)
    return final_value

def leaguerankings(client):
    @client.command()
    async def getsummoner(ctx, username):
        log_command(f"{ctx.author.display_name} | getsummoner {username}")
        output = ""
        summoner_stat = watcher.summoner.by_name(my_region, f'{username}')
        rank_stat = watcher.league.by_summoner(my_region, summoner_stat['id'])
        summoner_embed = discord.Embed(title=f"{summoner_stat['name']}'s Profile", description=f"Level {summoner_stat['summonerLevel']} Summoner", color=0x00ff00)
        queue_type = ""
        for x in rank_stat:
            if x['queueType'] == "RANKED_SOLO_5x5":
                queue_type = "SOLO/DUO"
            elif x['queueType'] == "RANKED_FLEX_SR":
                queue_type = "FLEX 5v5"
            summoner_embed.add_field(name=f"Queue | {queue_type}", value=f"{x['tier']} {x['rank']} @ {x['leaguePoints']}LP", inline=False)
        await ctx.send(embed=summoner_embed)
        await ctx.send(f"Rank Value: {rank_value({x['tier']}, {x['rank']}, {x['leaguePoints']})}")

    @client.command()
    async def leaguerankings(ctx):
        log_command(f"{ctx.author.display_name} | leaguerankings")
        ranking_array = []
        ranking_file = open('textfiles/leagueranking.txt', 'r')
        ranking_summoners = ranking_file.readlines()
        ranking_file.close()
        for summoner in ranking_summoners:
            summoner = summoner.rstrip()
            summoner_stat = watcher.summoner.by_name(my_region, f'{summoner}')
            rank_stat = watcher.league.by_summoner(my_region, summoner_stat['id'])
            for x in rank_stat:
                if x['queueType'] == "RANKED_SOLO_5x5":
                    summoner_tier = x['tier']
                    summoner_rank = x['rank']
                    summoner_points = x['leaguePoints']
                else:
                    pass
            summoner_add = [f"{rank_value(summoner_tier, summoner_rank, summoner_points)}", f"{summoner_stat['name']}", summoner_tier, summoner_rank, summoner_points]
            ranking_array.append(summoner_add)
            sorted_rankings = sorted(ranking_array,key=lambda x: x[0])
            ranking_array.sort(key = lambda element : element[0])
            sorted_rankings.reverse()
            embed_output = discord.Embed(title="League Rankings!", description="A ranking based on SOLO/DUO queue.", color=0x00ff00)
            counter = 1
            for summs in sorted_rankings:
                embed_output.add_field(name=f"#{counter} | {summs[1]}", value=f"{summs[2]} {summs[3]} @ {summs[4]}LP", inline=False)
                counter = counter + 1
        await ctx.send(embed=embed_output)

    @client.command()
    async def addrank(ctx, username):
        log_command(f"{ctx.author.display_name} | addrank")
        r = open("textfiles/leagueranking.txt", "a")
        r.write(f"{username}\n")
        r.close()