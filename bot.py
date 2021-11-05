import discord
from discord.ext import commands

from pathlib import Path
import json
import os
#from keep_alive import keep_alive
from tools import message

def main():
    parentDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(parentDir)

    with open(f"./data/setting/secret.json", 'r', encoding='utf8') as jdata:
        secret = json.load(jdata)

    bot = commands.Bot(command_prefix='>', case_insensitive=True,
                    intents=discord.Intents.all())

    bot.COG_LIST = {p.stem for p in Path(".").glob("cogs/*.py")}
    bot.LOADED_COG = {}

    @bot.event
    async def on_ready():
        bot.client_id = (await bot.application_info()).id
        # PreLoad
        bot.LOADED_COG = {'event', 'reactionRole', 'react', 'main'}
        for c in bot.LOADED_COG:
            bot.load_extension(f'cogs.{c}')
        print('>> MitoBot is on service <<')


    @bot.event
    async def on_connect():
        print(
            f'MitoBot connected to Discord (latency: {round(bot.latency*1000)} ms).')

    @bot.command()
    @commands.has_any_role('botMaster', '社團幹部')
    async def reload(ctx):
        suc = 0
        for c in bot.LOADED_COG:
            bot.reload_extension(f'cogs.{c}')
            suc += 1
        await ctx.send(f'reload {suc} cogs done')
        print(f'[C] reloaded {suc}')

    @bot.command()
    @commands.has_any_role('botMaster', '社團幹部')
    async def load(ctx, *args):
        suc = 0
        fal = 0
        if (not args) or '-l' in args:
            await ctx.send(f"available cogs : {',  '.join(bot.COG_LIST)}")
            return

        elif '-a' in args:
            for c in bot.COG_LIST:
                suc+=1
                bot.load_extension(f'cogs.{c}')

        else:
            for c in args:
                if c in bot.LOADED_COG:
                    fal+=1
                    print(f"{c} already loaded")
                elif c in bot.COG_LIST:
                    suc+=1
                    bot.LOADED_COG.add(c)
                    bot.load_extension(f'cogs.{c}')
                    print(f"{c} load done")
                else:
                    fal+=1
                    print(f"{c} not exist")
        await ctx.send(f'load {suc} done,  load {fal} failed')
        print('[C] loaded, now : ', bot.LOADED_COG)

    @bot.command()
    @commands.has_any_role('botMaster', '社團幹部')
    async def unload(ctx, *args):
        suc = 0
        fal = 0
        if (not args) or ('-l' in args):
            await ctx.send(f"current loaded : {',  '.join(bot.LOADED_COG)}")
            return

        elif '-a' in args:
            for c in bot.LOADED_COG:
                bot.unload_extension(f'cogs.{c}')
            # reset loaded set
            bot.LOADED_COG = set()
            await ctx.send('full unload completed')
        
        for c in args:
            if c in bot.LOADED_COG:
                suc+=1
                bot.LOADED_COG.remove(c)
                bot.unload_extension(f'cogs.{c}')
                print(f"{c} unload done")
            else:
                fal+=1
                print(f"{c} not exist")
        await ctx.send(f'unload {suc} done,  unload {fal} failed')
        print('[C] unloaded, now : ', bot.LOADED_COG)

    # @bot.command()
    # async def load(ctx, ext):
    #     bot.load_extension(f'cogs.{ext}')
    #     await ctx.send(message.codeblock(f'{ext} loaded successfully.'))


    # @bot.command()
    # async def unload(ctx, ext):
    #     bot.unload_extension(f'cogs.{ext}')
    #     await ctx.send(message.codeblock(f'{ext} unloaded successfully.'))


    # @bot.command()
    # async def reload(ctx, ext):
    #     bot.reload_extension(f'cogs.{ext}')
    #     await ctx.send(message.codeblock(f'{ext} reloaded successfully.'))


    @bot.command()
    @commands.has_any_role('botMaster', '社團幹部')
    async def close(ctx):
        await ctx.send(message.codeblock('Bye bye.'))
        await bot.close()

    print('Done.\nMitoBot starting...')
    bot.run(secret['Authorization'], reconnect=True)

if __name__ == '__main__':
    main()
