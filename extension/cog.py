import discord
from discord.ext import commands


class CogExtension(commands.Cog):
    __slots__ = ('bot')
    def __init__(self, bot):
        self.bot = bot
