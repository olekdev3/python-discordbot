import discord
from discord.ext import commands 
from commands.moderation import moderation, suggestions
from commands.leagueranking import leaguerankings
from commands.funcommands import eightball, afk, replicate

def main():

    creed_bot = commands.Bot(command_prefix = '#') # initialises bot
    command_file = open('command_log.txt','a')

    # when bot is ready
    @creed_bot.event
    async def on_ready():
        print('Bot is ready.')

    # when a member joins
    @creed_bot.event
    async def on_member_join(member):
        print(f'{member} has joined the server.')

    # when a member leaves
    @creed_bot.event
    async def on_member_remove(member):
        print(f'{member} has left the server.')

    moderation(creed_bot)
    leaguerankings(creed_bot)
    eightball(creed_bot)
    afk(creed_bot)
    suggestions(creed_bot)
    replicate(creed_bot)

    # retrieves discord token
    discord_token_filepath = open('D:/token.txt','r')
    discord_token = discord_token_filepath.readline()
    discord_token_filepath.close()

    creed_bot.run(discord_token)

if __name__ == '__main__':
    main()