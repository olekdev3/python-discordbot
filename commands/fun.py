import discord, os
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError
import pandas as pd

watcher = LolWatcher('RGAPI-465d03ce-06dc-450a-82e7-76723a719aa2')
my_region = 'euw1'

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
        output = f"Name: {summoner_stat['name']}\nLevel: {summoner_stat['summonerLevel']}\nRank: {rank_stat[0]['tier']} {rank_stat[0]['rank']}"
        await ctx.send(output)

        # command to add username to list for comparison
        # command to remove username from list
        # command to show ranks
        # function to retrieve integer value based on rank
        """
        iron = 1
        bronze = 2
        silver = 3

        int * 4 = top of rank

        I = -0
        II = -1
        III = -2
        IV = -3

        """