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
import mysql.connector

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

    cursor = await get_join_messages(server.id)
    for id, Message in cursor:
        await bot.send_message(member, Message)
    cursor.close()
    
@bot.command(pass_context=True, no_pm=True)
async def add_join_message(ctx):
 ##  msgs[num] = ctx.message.content[18:]
    permission = False
    for x in ctx.message.author.roles:
        if x.permissions.manage_channels:
            permission = True
       
        
    if permission:
        try:
            msg = ctx.message.content[18:]
            cursor = cnx.cursor(buffered=True)
            statement = "Insert into joinMessages(Message, ServerID) VALUES(%s,%s)"
            values = (msg, ctx.message.author.server.id)
            cursor.execute(statement, values)
            cursor.execute('commit')
            cursor.close()
            await bot.say("Command accepted")
        except Exception:
            await bot.say("Something went wrong! Try again or alert Sindalf")
    else:
        await bot.say("You don't have permission to use this command")

@bot.command(pass_context=True, no_pm=True)
async def check_join_messages(ctx):
    permission = False
    for x in ctx.message.author.roles:
        if x.permissions.manage_channels:
            permission = True
            
    if permission:
        try:
            cursor = await get_join_messages(ctx.message.author.server.id)
            
            for id, Message in cursor:
                await bot.say("Message id: " + str(id))
                await bot.say(Message)
                
            cursor.close()
            await bot.say("Finished displaying messages")
        except Exception:
            await bot.say("Something went wrong! Try again or alert Sindalf")
    else:
        await bot.say("You don't have permission to use this command")

@bot.command(pass_context=True, no_pm=True)
async def delete_join_message(ctx, number : int):
    permission = False
    for x in ctx.message.author.roles:
        if x.permissions.manage_channels:
            permission = True
            
    if permission:
        try:
            await delete_db_join_message(number, ctx.message.author.server.id)
            await bot.say("Message deleted")
        except Exception:
            await bot.say("Something went wrong! Try again or alert Sindalf")
    else:
        await bot.say("You don't have permission to use this command")
        

@bot.command(pass_context=True, no_pm=True)
async def done(ctx):
    if ctx.message.author.id == '48163936855392256':
        cnx.close()
        sys.exit()
    else:
        print("Someone is trying to use the done command")

'''
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
breakpoints = [300, 600, 3000, 6000, 11000, 15860]
exp_curve = [60, 60, 240, 300, 500, 600, 1414]
level_chart = [60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 900, 1140, 1380, 1620, 1860, 2100, 2340, 2580, 2820, 3060, 3360, 3660, 3960, 4260, 4560, 4860, 5160, 5460, 5760, 6060, 6560, 7060, 7560, 8060, 8560, 9060, 9560, 10060, 10560, 11060, 11660, 12260, 12860, 13460, 14060, 14660, 15260, 15860, 17274, 18688, 20102, 21516, 22930, 24344, 25758, 27172, 28586, 30000]
exp_gain = 7
ranks = ['Normie', 'Kogal', 'Office Lady', "High Schooler", "Loli", "Succubus", 'Tentacle Beast']


class user_exp():
    def __init__(self):
        self.time = datetime.now()
    
@bot.event
async def on_message(message):
    if message.server is not None:
        id = message.author.id
        user_time = exp_users.get(id, None)
        if user_time is None:
            await Increment(id) ## adds to database if DNE
            user_time = user_exp()
        else:
            date = datetime.now() 
            delta = date - user_time.time
            if delta.seconds > 30:
                user_time.time = date
                await Increment(id)
                
        exp_users[id] = user_time 
    
    await bot.process_commands(message)

async def delete_db_join_message(id, server_id):
    query = ("Delete from joinMessages where id = %s and ServerID = %s")
    values = (id, server_id)
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query, values)
    cursor.execute("commit")
    cursor.close()
    
async def get_join_messages(server_id):
    cursor = cnx.cursor(buffered=True)
    query = ("Select id, Message from joinMessages where ServerID = %s")
    cursor.execute(query, (server_id,))
    cursor.execute(query, (server_id,))
    return cursor
    
async def Increment(id):
    cursor = cnx.cursor(buffered=True)
    args = (id,)
    cursor.callproc('Increment', args)
    cursor.execute('commit')
    cursor.close()
    
async def getEXP(id):
    cursor = cnx.cursor(buffered=True)
    args = (id,0)
    result = cursor.callproc('getEXP', args)
    cursor.close()
    return result[1]
    
@bot.command(pass_context=True, no_pm=True)
async def rank(ctx):
    id = ctx.message.author.id
    exp = await getEXP(id)
    if exp is not None:
        i = bisect.bisect_left(breakpoints, exp)
        rank = ranks[i]
        level = bisect.bisect_left(level_chart, exp) + 1
        name = ctx.message.author.name
        fmt = "{0}: You are level {1} with {2} exp. You have achieved the rank of {3}"
        await bot.say(fmt.format(name, level, exp, rank))


async def get_self_assigned_roles(server_id):
    cursor = cnx.cursor(buffered=True)
    query = ("Select ServerID, roleID, name from self_assigned_roles where ServerID = %s")
    cursor.execute(query, (server_id,))
    roles = list()
    for serverID,roleID,name in cursor:
        a = {"serverID":serverID, "roleID":str(roleID),"name":name}
        roles.append(a)
    cursor.close()
    return roles

async def add_self_assigned_role(serverID, roleID, name):
    cursor = cnx.cursor(buffered=True)
    statement = "Insert into self_assigned_roles(ServerID, roleID, name) VALUES(%s,%s, %s)"
    values = (serverID, roleID, name)
    cursor.execute(statement, values)
    cursor.execute("commit")
    cursor.close()

async def delete_role_from_db(serverID, name):
    query = ("Delete from self_assigned_roles where serverID = %s and name = %s")
    values = (serverID, name)
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query, values)
    cursor.execute("commit")
    cursor.close()
    
    
@bot.command(pass_context=True, no_pm=True)
async def remove_role(ctx, name):
    permission = False
    for x in ctx.message.author.roles:
        if x.permissions.manage_roles:
            permission = True
            
    if permission:
        await delete_role_from_db(ctx.message.server.id, name)
        await bot.say("Roles deleted. Probably. Do !get_roles to check the list.")
    else:
        await bot.say("You don't have permission to use this function.")
    
@bot.command(pass_context=True, no_pm=True)
async def get_roles(ctx):
    roles = await get_self_assigned_roles(ctx.message.server.id)
    await bot.say("List of roles you are allowed to add on this server.")
    a = list()
    for x in roles:
        a.append(x["name"])
    if len(a) == 0:
        await bot.say("There are no roles you can add")
    else:
        await bot.say(a)
    
@bot.command(pass_context=True, no_pm=True)
async def add_role(ctx, name):
    permission = False
    for x in ctx.message.author.roles:
        if x.permissions.manage_roles:
            permission = True
            
    if permission:
        result = discord.utils.get(ctx.message.server.roles, name=name)
        if result is None:
            await bot.say("Error. Role does not exist")
        else:
            await add_self_assigned_role(ctx.message.server.id, result.id, result.name)
            await bot.say("Role added")
    else:
        await bot.say("You don't have permission to use this function.")
            
@bot.command(pass_context=True, no_pm=True)
async def set_role(ctx, ds=None):
    try:
        result = discord.utils.get(ctx.message.server.roles, name=ds)
        if result is not None:
            roles = await get_self_assigned_roles(ctx.message.server.id)
            print(roles)
            print(result.id)
            for x in roles:
                if result.id in x["roleID"]:
                    if result in ctx.message.author.roles:
                        await bot.remove_roles(ctx.message.author, result)
                        fmt = "{0}: You no longer have the role of {1}."
                        await bot.say(fmt.format(ctx.message.author.name, result.name))
                    else:
                        await bot.add_roles(ctx.message.author, result)
                        fmt = "{0}: You now have the role of {1}."
                        await bot.say(fmt.format(ctx.message.author.name, result.name))
        else:
            await bot.say("Not a role you can add.")
    except discord.Forbidden:
        await bot.say("You do not have permissions to add roles")
    except discord.HTTPException:
        await bot.say("Adding role failed. Blame discord. Try again.")
        
print("Connecting to database")
cnx = mysql.connector.connect(user=password.MySQL_User, password=password.MySQL_Pass, host=password.MySQL_Host, database=password.MySQL_DB)
exp_users = dict()
bot.loop.set_debug(True)
bot.run(password.Token) # Put your own discord token here
