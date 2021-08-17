import discord
from discord.ext import commands

from extension.cog import CogExtension

KEYWORD = "**[KEYWORD]**找我領取身分組"

class React(CogExtension):
    __slots__ = ('bot')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @commands.command(name = 'lrole')
    @commands.has_role('botMaster')
    async def _listRole(self, ctx):
        print(", ".join([str(r.id) for r in ctx.guild.roles]))
        print(", ".join([str(r) for r in ctx.guild.roles]))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if KEYWORD not in reaction.message.content:
            return
        if reaction.emoji == "❔":
            Role = discord.utils.get(user.guild.roles, name="A")
            await user.add_roles(Role)
        elif reaction.emoji == "⚡":
            Role = discord.utils.get(user.guild.roles, name="B")
            await user.add_roles(Role)


def setup(bot):
    bot.add_cog(React(bot))
