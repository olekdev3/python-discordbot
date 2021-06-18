import discord, os
from discord.ext import commands 

def eightball(client):
    @client.command(aliases=['8ball','eightball'])
    async def _8ball(ctx, *, question):
        await ctx.send(f'Question: {question}\nAnswer: No, fuck off.')

def afk(client):
    @client.command()
    async def afk(ctx):
        display_name = ctx.author.display_name
        await ctx.channel.purge(limit=1)
        if display_name[0:5] == '[AFK]':
            new_name = display_name[5:]
            await ctx.author.edit(nick=new_name)
            await ctx.send(f'{new_name} is no longer AFK')
        else:
            print( display_name[0:5])
            await ctx.send(f'{ctx.author.display_name} is now AFK')
            await ctx.author.edit(nick=f'[AFK]{display_name}')

def sherlock(client):
    @client.command()
    async def findusername(ctx, username):
        await ctx.channel.purge(limit=1)
        await ctx.send(f"Running profile scan on: {username}")
        os.system(f'python3 sherlock-master/sherlock/sherlock.py {username}')
        await ctx.send(file=discord.File(f'{username}.txt'))
        os.remove(f'{username}.txt')
        await ctx.send("Results have been sent.")