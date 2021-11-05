import discord
from discord.ext import commands

from extension.cog import CogExtension
from tools import message

class DayoffSys(CogExtension):
    @commands.command()
    async def dayoff(self, *ctx):
        await ctx.send(message.codeblock(f"function is work in progress currently..."))
        
def setup(bot):
    bot.add_cog(DayoffSys(bot))