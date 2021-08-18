import discord
from discord.ext import commands

from pathlib import Path
import json
#from keep_alive import keep_alive
from tools import message


with open('data/setting/secret.json', 'r', encoding='utf8') as jdata:
    secret = json.load(jdata)

bot = commands.Bot(command_prefix='>', case_insensitive=True,
                   intents=discord.Intents.all())


@bot.event
async def on_ready():
    bot.client_id = (await bot.application_info()).id
    print('>> MitoBot is on service <<')


@bot.event
async def on_connect():
    print(
        f'MitoBot connected to Discord (latency: {round(bot.latency*1000)} ms).')


@bot.command()
async def load(ctx, ext):
    bot.load_extension(f'cogs.{ext}')
    await ctx.send(message.codeblock(f'{ext} loaded successfully.'))


@bot.command()
async def unload(ctx, ext):
    bot.unload_extension(f'cogs.{ext}')
    await ctx.send(message.codeblock(f'{ext} unloaded successfully.'))


@bot.command()
async def reload(ctx, ext):
    bot.reload_extension(f'cogs.{ext}')
    await ctx.send(message.codeblock(f'{ext} reloaded successfully.'))


@bot.command()
@commands.has_role('botMaster')
async def close(ctx):
    await ctx.send(message.codeblock('Bye bye.'))
    await bot.close()

for cog in [p.stem for p in Path(".").glob("./cogs/*.py")]:
    bot.load_extension(f'cogs.{cog}')
    print(f'Loaded {cog}.')
print('Done.')

# keep_alive()
print('MitoBot starting...')
bot.run(secret['Authorization'], reconnect=True)
