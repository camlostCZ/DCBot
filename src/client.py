import logging

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cog_common import GeneralCommands
from cog_guessnumber import GuessNumberGame
from cog_hangman import HangmanGame
from creds import GUILD


intents = discord.Intents.default()
bot = Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    logging.info(
        f"{bot.user} is connected to guild: {guild.name} (id: {guild.id})")

    #members = "\n - ".join([member.name for member in guild.members])
    #print(f"Guild Members:\n - {members}")


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"Vítej, {member.name}, na mém Discord serveru!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("Nemáš roli potřebnou pro uvedený příkaz.")
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Neznámý příkaz.")


bot.add_cog(GeneralCommands(bot))
bot.add_cog(GuessNumberGame(bot))
bot.add_cog(HangmanGame(bot))
