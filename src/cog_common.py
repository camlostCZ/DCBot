import logging
import re

import requests
from discord.ext import commands
from lxml import html

import conf


class GeneralCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self._bot = bot


    @commands.command(name="calc", help="Jednoduchá kalkulačka")
    async def calc(self, ctx, *args):
        expression = "".join(args)
        logging.debug(f"Calc parameter: {expression}")
        response = "Neplatné zadání. Povolené znaky: 0-9, *, /, +, -, mezera, (, ), ^"

        if re.match(conf.PATTERN_CALC_VALIDATION, expression):
            expr_translated = expression.replace("^", "**")
            logging.debug(f"Calc - fixed expression: {expr_translated}")
            try:
                result = eval(expr_translated)
                response = f"Výsledek:  {result}"
            except:
                response = "Neplatný výraz."
        await ctx.send(response)


    @commands.command(name="joke", help="Zobrazí náhodný vtip.")
    async def joke(self, ctx):
        page = requests.get(conf.URL_JOKES)
        tree = html.fromstring(page.content)
        jokes = tree.xpath('//div[@class="joke"]')
        logging.debug(f"Jokes found: {len(jokes)}")

        response = "Chyba: Vtip nebyl nalezen."
        if not jokes is None and len(jokes) > 0:
            response = ""
            for each in jokes[0].iter():
                if each.text:
                    response += each.text
                if each.tail:
                    response += each.tail
        await ctx.send(response)


    @commands.command(name="mc", help="Vyhledávání v oficiální Minecraft Wiki.")
    async def mc_search(self, ctx, query: str):
        response = f"https://minecraft.gamepedia.com/Special:Search?search={query}"
        await ctx.send(response)


    @commands.command(name="ping", help="Odpoví 'pong'.")
    async def ping(self, ctx):
        response = f"pong ({round(self._bot.latency * 1000)} ms)"
        await ctx.send(response)
