import discord
from discord.ext import commands
from commands.logging import log_command

# clear | showcommands/commands |

def moderation(client):
    @client.command()
    async def clear(ctx, *, amount):
        log_command(f"{ctx.author.display_name} | clear {amount}")
        await ctx.channel.purge(limit=int(amount) + 1)
        await ctx.send(f'{ctx.author.name} has cleared {amount} lines.')

    @client.command(aliases=['commands'])
    async def showcommands(ctx):
        log_command(f"{ctx.author.display_name} | commands")
        command_file = open("textfiles/commandlist.txt","r")
        commands = command_file.readlines()
        command_list = ''
        for command in commands:
            command_list = f'{command_list}{command}'
        await ctx.send(command_list)

def suggestions(client):
    @client.command()
    async def addsuggestion(ctx, *, suggest):
        log_command(f"{ctx.author.display_name} | addsuggestion")
        f = open("textfiles/suggestions.txt", "a")
        f.write(f'{suggest} | {ctx.author.display_name}\n')
        f.close()
        await ctx.send('Suggestion added.')

    @client.command()
    async def suggestions(ctx):
        log_command(f"{ctx.author.display_name} | suggestions")
        f = open("textfiles/suggestions.txt", "r")
        lines = f.readlines()
        all_suggestions = ""
        counter = 1
        for line in lines:
            all_suggestions = f"{all_suggestions}#{counter} | {line}"
            counter = counter + 1
        await ctx.send(all_suggestions)