import discord
from discord.ext import commands
from extension.cog import CogExtension
from tools import message

#KEYWORD = "找我領取身分組"
roleDict = {"<:nsysu_isc:877159351272493058>": "資安社",
            "<:nsysu_cc:877159351582871552>": "程式研習社"}


class RoleManager(CogExtension):
    __slots__ = ('bot')
    _message_id = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # @commands.command(name='lrole')
    # @commands.has_any_role('botMaster', '社團幹部')
    # async def _listRole(self, ctx):
    #     print(", ".join([str(r.id) for r in ctx.guild.roles]))
    #     print(", ".join([str(r) for r in ctx.guild.roles]))

    @commands.command(name='reactionRole')
    @commands.has_any_role('botMaster', '社團幹部')
    async def _reactionRole(self, ctx):
        await ctx.message.delete()
        msg = await ctx.send('找我領取身分組OwO')
        self._message_id = msg.id
        for k in roleDict:
            try:
                await msg.add_reaction(k)
            except:
                pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != self._message_id:
            return
        if str(payload.emoji) == '<:nsysu_isc:877159351272493058>':
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(876466020649431110)
            await payload.member.add_roles(role)
            await payload.member.send(f'您取得了{role}身分組!\n歡迎加入資安社')
        elif str(payload.emoji) == '<:nsysu_cc:877159351582871552>':
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(876465833315028992)
            await payload.member.add_roles(role)
            await payload.member.send(f'您取得了{role}身分組!\n歡迎加入程式研習社')

    # remove無法取得member參數
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id != self._message_id:
            return
        if str(payload.emoji) == '<:nsysu_isc:877159351272493058>':
            guild = self.bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            role = guild.get_role(876466020649431110)
            await user.remove_roles(role)
        elif str(payload.emoji) == '<:nsysu_cc:877159351582871552>':
            guild = self.bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            role = guild.get_role(876465833315028992)
            await user.remove_roles(role)


def setup(bot):
    bot.add_cog(RoleManager(bot))
