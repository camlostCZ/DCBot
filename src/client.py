from math import exp
import re
from urllib import response
import requests

from lxml import html

import discord
from discord.ext.commands import Bot

import conf
from creds import *
from helpcmd import PBotHelpCmd

# Pattern used to validate input before calling eval()
# Allowed chars: 0-9, *, /, +, -, space, (, ), and ^.
PATTERN_CALC_VALIDATION = r"^[0-9+\-*\/^\(\)\. ]+$"


intents = discord.Intents.default()
bot = Bot(command_prefix="!", intents=intents)


@bot.command(name="calc", help="Jednoduchá kalkulačka")
async def calc(ctx, *args):
    expression = "".join(args)
    print(f"Calc parameter: {expression}")
    response = "Neplatné zadání. Povolené znaky: 0-9, *, /, +, -, mezera, (, ), ^"

    if re.match(PATTERN_CALC_VALIDATION, expression):
        expr_translated = expression.replace("^", "**")
        print(f"Calc - fixed expression: {expr_translated}")
        try:
            result = eval(expr_translated)
            response = f"Výsledek:  {result}"
        except:
            response = "Neplatný výraz."
    await ctx.send(response)


@bot.command(name="ping", help="Odpoví 'pong'.")
async def ping(ctx):
    response = f"pong ({round(bot.latency * 1000)} ms)"
    await ctx.send(response)


@bot.command(name="vtip", help="Zobrazí náhodný vtip.")
async def vtip(ctx):
    page = requests.get(conf.URL_JOKES)
    tree = html.fromstring(page.content)
    jokes = tree.xpath('//div[@class="joke"]')
    #print(f"DBG: Jokes found: {len(jokes)}")

    response = "Chyba: Vtip nebyl nalezen."
    if not jokes is None and len(jokes) > 0:
        response = ""
        for each in jokes[0].iter():
            if each.text:
                response += each.text
            if each.tail:
                response += each.tail
    await ctx.send(response)


@bot.command(name="mc", help="Vyhledávání v oficiální Minecraft Wiki.")
async def mc_search(ctx, query: str):
    response = f"https://minecraft.gamepedia.com/Special:Search?search={query}"
    await ctx.send(response)


@bot.command(name="py", help="Python help")
async def python_docs(ctx, query: str):
    url = f"https://docs.python.org/3/search.html?q={query}&check_keywords=yes&area=default"
    print(f"DBG: url={url}")
    page = requests.get(url)
    tree = html.fromstring(page.content)
    results = tree.xpath('//ul[@class="search"]//a')

    response = "WIP"
    await ctx.send(response)

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f"{bot.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )

    members = "\n - ".join([member.name for member in guild.members])
    print(f"Guild Members:\n - {members}")


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Vítej, {member.name}, na mém Discord serveru!")
