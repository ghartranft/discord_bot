import asyncio
import json
import urllib.error
import urllib.request
import re
from bs4 import BeautifulSoup
from discord.ext import commands
import random
import password
import requests
import os.path
import pickle
from Manga import manga
import sys
from datetime import datetime
import bisect

# All functions are async so we can interrupt them at any time and resume another

p = re.compile('^(https?:\/\/)', re.IGNORECASE)

bot = commands.Bot(command_prefix='!', description='bot owned by Sindalf')


@bot.event
async def on_member_join(member):
    server = member.server
    if server.id == '222895741918511105':
        fmt = 'Welcome {0.mention} to {1.name}!'
        await bot.send_message(server, fmt.format(member, server))
'''
@bot.command(description='Get a random post from r/blackpeopletwitter')
async def bpt(limit=100):
    data = await get_json('https://www.reddit.com/r/blackpeopletwitter.json?limit=' + str(limit))
    if data is not None:
        data = data['data']['children']
        num = random.randint(1, len(data)-1)
        url = data[num]['data']['url']
        await bot.say(url)
    else:
        await bot.say('Could not receive reddit json')
'''
'''
@bot.command(description='Get a random post from r/woof_irl')
async def bork(limit=50):
    data = await get_json('https://www.reddit.com/r/woof_irl.json?limit=' + str(limit))
    if data is not None:
        data = data['data']['children']
        num = random.randint(1, len(data)-1)
        url = data[num]['data']['url']
        await bot.say(url)
    else:
        await bot.say('Could not receive reddit json')
'''
@bot.command(description='How do I shot web?')
async def shotweb():
    await bot.say("How do I shot web? \n https://cdn.drawception.com/images/panels/2012/6-14/GGFpZEHKLY-2.png")


@bot.command(description=':joy: :gun:')
async def joygun():
    await bot.say(":joy: :gun:")

@bot.command(description=":clap:")
async def clap(*message):
    a = " :clap: ".join(message)
    await bot.say(a)


@bot.command(description="charge me daddy")
async def charge():
    await bot.say(":regional_indicator_c: :regional_indicator_h: :regional_indicator_a: :regional_indicator_r: :regional_indicator_g: :regional_indicator_e:  :regional_indicator_m: :regional_indicator_e:  :regional_indicator_d: :regional_indicator_a: :regional_indicator_d: :regional_indicator_d: :regional_indicator_y:!")

@bot.command(description="checkem")
async def roll(start=0, limit=100):
    num = random.randint(start, limit)
    string = ':' + str(num) + ':'
    await bot.say(string)
'''
@bot.command(description='Check if a website is online. Default=https://www.fakku.net/')
async def up(url="https://www.fakku.net/"):
    if await detect_http(url) is None:  # detects if the front of the url contains http:// or https://
        url = 'http://' + url  # add http since most http sites redirect to https
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            if response.getcode() == 200:
                await bot.say(url + " looks up from here! (USA East Coast)")
            else:
                await bot.say(url + " looks down from here! (USA East Coast)")
    except urllib.error.URLError:  # redundant command
        await bot.say(url + " is an invalid url or not up!")
    except urllib.error.HTTPError:  # This may never happen but just in case
        await bot.say(url + " looks down from here! (USA East Coast)")
'''

"""
@bot.command(description=":regional_indicator_")
async def text(*message : str):
    string = ""
    for x in message:
        for i in x.lower():
            append = ":regional_indicator_" + i + ":"
            string +=  append
        string += "   "
    await bot.say(string)
"""

@bot.command(description="its that time")
async def itsthattime():
    await bot.say('https://www.youtube.com/watch?v=shCYA2J-De8')

async def detect_http(url):
    return re.match(p, url)  # regex search for http or https is at the start of url


@bot.command(description="Heads or Tails")
async def coinflip():
    a = random.randint(0,1)
    str = "Tails"
    if a:
        str = "Heads"
    await bot.say(str)
    
@bot.command(description="Create a strawpoll!")
async def strawpoll(*message : str):
    a = " ".join(message)
    print(a)
    a = a.split(",")
    print(a)
    a = list(map(str.strip, a))
    print(a)
    multi = ["true", "false"]
    dupe = ["normal", "permissive", "disabled"]
    data = {"multi": "false", "dupcheck": "normal"}
    options = list()

    data['title'] = a[0]
    option_offset = 1
    '''
    if len(a) > 4:
        if a[1].lower() in multi:
            data['multi'] = a[1].lower()
        if a[2].lower() in dupe:
            data['dupcheck'] = a[2].lower()
        option_offset = 3
    '''
    for question in a[option_offset:]:
        options.append(question)

    data['options'] = options

    headers = {'Content-type': "application/json"}
    r = await post_request('https://strawpoll.me/api/v2/polls', json.dumps(data), headers)
    if r.status_code == 200:
        result = r.json()
        await bot.say("https://www.strawpoll.me/" + str(result['id']))
    else:
        await bot.say(r.json())



async def get_json(url,cookies=None):
    try:
        headers = {
        'User-Agent': 'discordbot'  # This is another valid field
        }
        data = requests.get(url, timeout=10,cookies=cookies, headers=headers)
        data.encoding = 'utf-8'
        return data.json()
    except:  # For some reason HTTPError wouldnt catch an HTTPError ?
        print('json error in get link')
        return None


async def get_html(url,cookies=None):
    try:
        data = requests.get(url, timeout=10,cookies=cookies)
        data.encoding = 'utf-8'
        return data.text
    except:  # For some reason HTTPError wouldnt catch an HTTPError ?
        print('http error in get link')
        return None

#Must be successful
async def must_get_request(url,cookies=None):
    while True:
        try:
            data = requests.get(url, timeout=10,cookies=cookies)
            data.encoding = 'utf-8'
            return data
        except:
            print('http error!')
            await asyncio.sleep(60)  # sleep to not grab a dead link over and over



async def post_request(url, data=None, headers=None):
    r = requests.post(url, data=data, headers=headers)
    return r


async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_member_join(member):
    server = member.server
    if server.id == '222895741918511105':
        fmt = 'Welcome {0.mention} to {1.name}!'
        await bot.send_message(server, fmt.format(member, server))

    if server.id in join_messages:
        msgs = join_messages[server.id]
        for k,v in msgs.items():
            if type(k) == int:
                await bot.send_message(member, v)

@bot.command(pass_context=True, no_pm=True)
async def add_join_message(ctx):

    permission = False
    for x in ctx.message.author.roles:
        if x.permissions.manage_channels:
            permission = True

    if permission:
        await bot.say("Command accepted")
        msgs = join_messages.get(ctx.message.author.server.id, {})
        if not msgs:
            msgs['max'] = 0
            join_messages[ctx.message.author.server.id] = msgs
        num = msgs['max']
        num += 1
        msgs['max'] = num
        msgs[num] = ctx.message.content[18:]
        join_messages['change'] = True
    else:
        await bot.say("You don't have permission to use this command")

@bot.command(pass_context=True, no_pm=True)
async def check_join_messages(ctx):
    permission = False
    for x in ctx.message.author.roles:
        if x.permissions.manage_channels:
            permission = True
    if permission:
        msgs = join_messages.get(ctx.message.author.server.id, {})
        for k,v in msgs.items():
            if type(k) == int:
                await bot.say("Displaying message " + str(k))
                await bot.say(v)
        await bot.say("Finished displaying messages")
    else:
        await bot.say("You don't have permission to use this command")

@bot.command(pass_context=True, no_pm=True)
async def delete_join_message(ctx, number : int):
    permission = False
    for x in ctx.message.author.roles:
        if x.permissions.manage_channels:
            permission = True
    if permission:
        msgs = join_messages.get(ctx.message.author.server.id, {})
        try:
            del msgs[number]
            await bot.say("The command " + str(number) + " has been deleted.")
            join_messages['change'] = True
        except KeyError:
            await bot.say("The command " + str(number) + " does not exist.")
    else:
        await bot.say("You don't have permission to use this command")

async def save_join_messages_forver(path="D:\stuff\BotData"):
    while True:
        if join_messages['change']:
            join_messages['change'] = False
            await save_data(join_messages, path)
            print("join_messages Saved!")
        await asyncio.sleep(60)

async def save_data_forever(data, path, time):
    while True:
        await asyncio.sleep(time)
        await save_data(data, path)
        
        
async def save_data(data, path):
        f = open(path, "wb+")
        pickle.dump(data, f)
        f.close()
        print(path + " Saved!")
        
@bot.command(pass_context=True)
async def backup(ctx):
    if ctx.message.author.id == '48163936855392256':
        await save_data(join_messages, "D:\stuff\BotData")
        await save_data(join_messages, "D:\stuff\BotEndBackUp")
        await save_data(exp_users, "D:\stuff\BotExpUsers")
        await save_data(exp_users, "D:\stuff\BotExpUsersBackUp")
    else:
        print("Someone is trying to use the backup command")

@bot.command(pass_context=True)
async def done(ctx):
    if ctx.message.author.id == '48163936855392256':
        await save_data(join_messages, "D:\stuff\BotData")
        await save_data(join_messages, "D:\stuff\BotEndBackUp")
        await save_data(exp_users, "D:\stuff\BotExpUsers")
        await save_data(exp_users, "D:\stuff\BotExpUsersBackUp")
        sys.exit()
    else:
        print("Someone is trying to use the done command")

def get_data_from_file(path, default):
    a = os.path.exists(path)
    if a:
        f = open(path, "rb+")
        data = pickle.load(f)
        f.close()
    else:
        data = default
    return data

'''
breakpoints = [300, 600, 1200, 5000, 10000]
exp_curve = [60, 60, 60, 380, 500, 500]
level_chart = [60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, 780, 840, 900, 960, 1020, 1080, 1140, 1200, 1260, 1640, 2020, 2400, 2780, 3160, 3540, 3920, 4300, 4680, 5000, 5560, 6060, 6560, 7060, 7560, 8060, 8560, 9060, 9560, 10000, 10560, 11060, 11560, 12060, 12560, 13060, 13560, 14060, 14560, 15060]
'''
breakpoints = [300, 600, 3000, 6000, 11000, 15860]
exp_curve = [60, 60, 240, 300, 500, 600, 1414]
level_chart = [60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 900, 1140, 1380, 1620, 1860, 2100, 2340, 2580, 2820, 3060, 3360, 3660, 3960, 4260, 4560, 4860, 5160, 5460, 5760, 6060, 6560, 7060, 7560, 8060, 8560, 9060, 9560, 10060, 10560, 11060, 11660, 12260, 12860, 13460, 14060, 14660, 15260, 15860, 17274, 18688, 20102, 21516, 22930, 24344, 25758, 27172, 28586, 30000]
exp_gain = 15
ranks = ['Normie', 'Kogal', 'Office Lady', "High Schooler", "Loli", "Succubus", 'Tentacle Beast']


class user_exp():
    def __init__(self):
        self.exp = 0
        self.time = datetime.now()
    
@bot.event
async def on_message(message):
    if message.server is not None:
        id = exp_users.get(message.author.id, user_exp())
        delta = datetime.now() - id.time
        if delta.seconds > 30:
            id.exp += exp_gain
            id.time = datetime.now()
        
        exp_users[message.author.id] = id 
    
    await bot.process_commands(message)

@bot.command(pass_context=True, no_pm=True)
async def rank(ctx):
    id = exp_users.get(ctx.message.author.id, None)
    if id is not None:
        i = bisect.bisect_left(breakpoints, id.exp)
        rank = ranks[i]
        level = bisect.bisect_left(level_chart, id.exp) + 1
        name = ctx.message.author.name
        fmt = "{0}: You are level {1} with {2.exp} exp. You have achieved the rank of {3}"
        await bot.say(fmt.format(name, level, id, rank))


bot.loop.set_debug(True)
join_messages = get_data_from_file("D:\stuff\BotData", {"change": False})
exp_users = get_data_from_file("D:\stuff\BotExpUsers", dict())
bot.loop.create_task(save_join_messages_forver())
bot.loop.create_task(save_data_forever(exp_users, "D:\stuff\BotExpUsers", 60*5))
bot.run(password.Token) # Put your own discord token here
