import discord, os
from discord.ext import commands
import requests, urllib.request
from commands.logging import log_command

# eightball/8ball | afk | findusername

def eightball(client):
    @client.command(aliases=['8ball','eightball'])
    async def _8ball(ctx, *, question):
        log_command(f"{ctx.author.display_name} | 8ball")
        await ctx.send(f'Question: {question}\nAnswer: No, fuck off.')

def afk(client):
    @client.command()
    async def afk(ctx):
        log_command(f"{ctx.author.display_name} | afk")
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
        log_command(f"{ctx.author.display_name} | findusername")
        await ctx.channel.purge(limit=1)
        await ctx.send(f"Running profile scan on: {username}")
        os.system(f'python3 sherlock-master/sherlock/sherlock.py {username}')
        await ctx.send(file=discord.File(f'{username}.txt'))
        os.remove(f'{username}.txt')
        await ctx.send("Results have been sent.")

def replicate(client):
    @client.command()
    async def botme(ctx):
        log_command(f"{ctx.author.display_name} | botme")
        user_avatar = ctx.author.avatar_url
        r = requests.get(user_avatar, allow_redirects=True)
        filepath = f'./images/{ctx.author.display_name}.jpeg'
        open(filepath, 'wb').write(r.content)
        image_fp = open(filepath, 'rb')
        new_image = image_fp.read()

        await client.user.edit(avatar=new_image, username=f'{ctx.author.display_name}')