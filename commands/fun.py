import discord, os
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError

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

    if tier == "IRON":
        raw_value = 1
    if tier == "BRONZE":
        raw_value = 2
    if tier == "SILVER":
        raw_value = 3
    if tier == "GOLD":
        raw_value = 4
    if tier == "PLATINUM":
        raw_value = 5
    if tier == "DIAMOND":
        raw_value = 6
    final_value = ((raw_value * 4) - deduction) + (leaguepoints / 100)
    return final_value

def fun(client):
    # Sherlock Scan
    @client.command()
    async def findme(ctx, username):
        await ctx.channel.purge(limit=1)
        await ctx.send(f"Running profile scan on: {username}")
        os.system(f'python3 sherlock-master/sherlock/sherlock.py {username}')
        await ctx.send(file=discord.File(f'{username}.txt'))
        os.remove(f'{username}.txt')
        await ctx.send("Results have been sent.")

    @client.command()
    async def getme(ctx, username):
        output = ""
        summoner_stat = watcher.summoner.by_name(my_region, f'{username}')
        rank_stat = watcher.league.by_summoner(my_region, summoner_stat['id'])
        output = f"{summoner_stat['name']} | Level {summoner_stat['summonerLevel']}"
        for x in rank_stat:
            output = f"{output} \nQueue: {x['queueType']} | {x['tier']} {x['rank']} @ {x['leaguePoints']}LP"
        await ctx.send(output)

        # command to add username to list for comparison
        # command to remove username from list
        # command to show ranks
        # function to retrieve integer value based on rank

    @client.command()
    async def leaguerankings(ctx):
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
                elif x['queueType'] == "RANKED_SOLO_SR":
                    pass
            summoner_add = [f"{float(rank_value(summoner_tier, summoner_rank, summoner_points))}", f"{summoner_stat['name']}", summoner_tier, summoner_rank, summoner_points]
            ranking_array.append(summoner_add)
            sorted_rankings = sorted(ranking_array,key=lambda x: x[0])
            sorted_rankings.reverse()
            embed_output = discord.Embed(title="League Rankings!", description="A ranking based on SOLO/DUO queue.", color=0x00ff00)
            counter = 1
            for summs in sorted_rankings:
                embed_output.add_field(name=f"#{counter} | {summs[1]}", value=f"{summs[2]} {summs[3]} @ {summs[4]}LP", inline=False)
                counter = counter + 1
        await ctx.send(embed=embed_output)

    @client.command()
    async def embedtest(ctx):
        embedVar = discord.Embed(title="League Rankings!", description="A ranking based on SOLO/DUO queue.", color=0x00ff00)
        embedVar.add_field(name="Field1", value="Value1", inline=False)
        embedVar.add_field(name="Field2", value="Value2", inline=False)
        await ctx.send(embed=embedVar)

    @client.command()
    async def addrank(ctx, username):
        r = open("textfiles/leagueranking.txt", "a")
        r.write(f"{username}\n")
        r.close()