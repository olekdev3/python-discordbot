import discord
from discord.ext import commands

def moderation(client):
    @client.command()
    async def clear(ctx, *, amount):
        await ctx.channel.purge(limit=int(amount) + 1)
        await ctx.send(f'{ctx.author.name} has cleared {amount} lines.')

    @client.command(aliases=['commands'])
    async def showcommands(ctx):
        command_file = open("textfiles/commandlist.txt","r")
        commands = command_file.readlines()
        command_list = ''
        for command in commands:
            command_list = f'{command_list}{command}\n'
        await ctx.send(command_list)