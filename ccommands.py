import discord
from discord.ext import commands 
def clear(client):
    @client.command()
    async def clear(ctx, *, amount):
        await ctx.channel.purge(limit=int(amount) + 1)
        await ctx.send(f'{ctx.author.name} has cleared {amount} lines.')