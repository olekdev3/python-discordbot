import discord, os, random
from discord.ext import commands
import requests, urllib.request
from commands.logging import log_command
from requests_html import HTMLSession
from bs4 import BeautifulSoup

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

def anime(client):
    @client.command()
    async def randomanime(ctx, *, amount):
        log_command(f"{ctx.author.display_name} | randomanime")
        session = HTMLSession()
        counter = 0
        embed_output = discord.Embed(title=f"{amount} Random Anime Titles", description=f"A list of {amount} random animes!", color=0x00ff00)
        await ctx.send(f'Requested: {amount} animes.')
        while counter < int(amount):
            url = f'https://myanimelist.net/anime/{random.randint(0, 16450)}'
            response = session.get(url)
            if response.status_code == 200:
                counter += 1
                soup = BeautifulSoup(urllib.request.urlopen(url))
                title = str(soup.title.string)
                title = title.strip('\n')
                rating = soup.find('div', {'class': 'score-label'}).text.strip()
                embed_output.add_field(name=f"# {counter} | {title[0:len(title) - 18]}", value=f"Link: {url}\nRating: {rating}\n", inline=False)

        await ctx.send(embed = embed_output)