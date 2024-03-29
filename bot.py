import discord
from discord.ext import commands
import requests
import json
import time
import random
import string
import os
import asyncio
import sys

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='/', intents=intents)

bbgen_cooldown_rate = 1
bbgen_cooldown_seconds = 60

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def nitro_gen():
    url = 'https://api.discord.gx.games/v1/direct-fulfillment'
    headers = {
        'authority': 'api.discord.gx.games',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.opera.com',
        'referer': 'https://www.opera.com/',
        'sec-ch-ua': '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0'
    }

    data = {
        'partnerUserId': generate_random_string(64)
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            token = response.json()['token']
            return f"https://discord.com/billing/partner-promotions/1180231712274387115/", token
        elif response.status_code == 429:
            return "Rate limit exceeded! Please try again later."
        elif response.status_code == 504:
            return "Server timed out! Please try again later."
        else:
            return f"Request failed with status code {response.status_code}. Error message: {response.text}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
@commands.cooldown(bbgen_cooldown_rate, bbgen_cooldown_seconds, commands.BucketType.user)
async def bbgen(ctx):
    try:
        link_prefix, token = await bot.loop.run_in_executor(None, nitro_gen)
        await ctx.author.send(f"{link_prefix}[][][][][][]{token}\n**(HVIS LINKET IK VIRKER, FJERN [][][][][][])**\n\n**IMAGINE AT VÆRE SÅ HJÆLPELØS!**")

        msg = await ctx.send(f"{ctx.author.mention}, Dit link er blevet sendt til dig!")

        await asyncio.sleep(5)
        await ctx.message.delete()
        await msg.delete()

    except commands.CommandOnCooldown as e:
        cooldown_retry_after = round(e.retry_after, 2)
        await ctx.send(f'SLAP AF DIN GRIS. Vent {cooldown_retry_after} sekunder.')
    except Exception as e:
        print(f"An error occurred: {e}")


@bot.command()
async def restart(ctx):
    if ctx.author.id == INDSÆT DIT ID:  # BRUG DIT EGET ID
        await ctx.send("Restarting bot...")
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        await ctx.send("You do not have permission to restart the bot.")

@bot.command()
async def clear(ctx, amount: int):
    if ctx.author.id == INDSÆT DIT ID:  # BRUG DIT EGET ID
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"{amount} messages cleared by {ctx.author.mention}.", delete_after=5)
    else:
        await ctx.send("You do not have the required permissions to use this command.")

@bot.command()
async def test(ctx):
	await ctx.send(f"```Generate dit Promo Link:\n\n/bbgen```")




bot.run('DIN EGEN TOKEN')
