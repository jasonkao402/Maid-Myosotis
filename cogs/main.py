import discord
from discord.ext import commands

import datetime as dt

from extension.cog import CogExtension
from tools import message


class Main(CogExtension):

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(message.codeblock(f'{round(self.bot.latency*1000)} ms'))

    @commands.command()
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(message.codeblock(msg))

    @commands.command()
    async def purge(self, ctx, num: int, mode='-u'):
        if mode == '-m':
            deleted = await ctx.channel.purge(limit=num+1, check=lambda message: message.author == ctx.author)
            await ctx.send(message.codeblock('Delete {} message(s).').format(len(deleted)-1), delete_after=10)
        elif mode == '-u':
            if ctx.author.guild_permissions.manage_messages:
                deleted = await ctx.channel.purge(limit=num+1)
                await ctx.send(message.codeblock('Delete {} message(s).').format(len(deleted)-1), delete_after=10)
            else:
                await ctx.send(message.codeblock('Permission denied.You do not have the permission of managing messages.'))

    @commands.command()
    async def hello(self, ctx):
        embed = discord.Embed(title="Discord bot MitoBot",
                              description="Hi My Name is Mito~~", color=0xfcc9b9,
                              timestamp=dt.datetime.utcnow())
        embed.set_author(name="MitoBot", url="https://github.com/jasonkao402/MitoBot",
                         icon_url="https://pbs.twimg.com/media/E7wn7V7XIAA4cUX?format=png&name=medium")
        embed.set_thumbnail(
            url="https://pbs.twimg.com/media/E7wn7V7XIAA4cUX?format=png&name=medium")
        embed.add_field(
            name="Author", value="Yukimura0119 & Jasonkao402", inline=False)
        embed.add_field(name="Language", value="Python", inline=False)
        embed.add_field(name="Birthday", value="Aug 16, 2021 ", inline=False)
        embed.add_field(name="BloodType", value="A", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def website(self, ctx):
        await ctx.send('Here is my website~\nhttps://github.com/jasonkao402/MitoBot')


def setup(bot):
    bot.add_cog(Main(bot))
