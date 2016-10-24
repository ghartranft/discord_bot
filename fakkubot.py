import asyncio
import json
import urllib.error
import urllib.request
import re
from bs4 import BeautifulSoup
from discord.ext import commands
import random
from Manga import manga
import password
import requests

# All functions are async so we can interrupt them at any time and resume another

p = re.compile('^(https?:\/\/)', re.IGNORECASE)

bot = commands.Bot(command_prefix='!', description='bot owned by Sindalf')


@bot.event
async def on_member_join(member):
    server = member.server
    if server.id == '222895741918511105':
        fmt = 'Welcome {0.mention} to {1.name}!'
        await bot.send_message(server, fmt.format(member, server))

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


@bot.command(description='How do I shot web?')
async def shotweb():
    await bot.say("How do I shot web? \n https://cdn.drawception.com/images/panels/2012/6-14/GGFpZEHKLY-2.png")


@bot.command(description=':joy: :gun:')
async def joygun():
    await bot.say(":joy: :gun:")

@bot.command(description="checkem")
async def roll(start=0, limit=100):
    num = random.randint(start, limit)
    string = ':' + str(num) + ':'
    await bot.say(string)
    
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


@bot.command(description='Get a random manga from fakku.net')
async def rand():
    data = await get_html('https://www.fakku.net/hentai/newest')
    if data is not None:
        soup = BeautifulSoup(data, 'html.parser')
        item = soup.find('div', class_='links')
        num = item.text[11:]
        n = int(num)
        print(n)
        n = random.randint(1, n-1)
        data = await get_html('https://www.fakku.net/hentai/newest/page/' + str(n))
        if data is not None:
            soup = BeautifulSoup(data, 'html.parser')
            items = soup.findAll('a', class_='content-title')
            n = random.randint(0, len(items)-1)
            print(items[n]['href'][8:])
            link = items[n]['href'][8:]
            data = await get_json('https://api.fakku.net/manga/' + link)
            if data is not None:
                data = data['content']
                m = manga(data)
                m.populate()  # populate the object with manga details, author, tags, etc

                html = await get_html(data['content_url'])
                if html is not None:
                    soup = BeautifulSoup(html, 'html.parser')
                    store_link = await detect_store_link(soup)
                    m.set_store_link(store_link)
                    magazine_text = await detect_magazine_text(soup)
                    m.set_magazine_text(magazine_text)
                r = await manga_string(m, 'Random Manga! \n')
                await bot.say(r)

    if data is None:
        print("Error. Is fakku up?")


async def detect_http(url):
    return re.match(p, url)  # regex search for http or https is at the start of url


async def get_json(url):
    try:
        data = requests.get(url, timeout=10)
        data.encoding = 'utf-8'
        return data.json()
    except:  # For some reason HTTPError wouldnt catch an HTTPError ?
        print('json error in get link')
        return None


async def get_html(url):
    try:
        data = requests.get(url, timeout=10)
        data.encoding = 'utf-8'
        return data.text
    except:  # For some reason HTTPError wouldnt catch an HTTPError ?
        print('http error in get link')
        return None


# Does not return without success
# returns a json object
async def get_fakku_json():
    while True:
        try:
            with urllib.request.urlopen('https://api.fakku.net/index', timeout=10) as response:
                html = response.read().decode('UTF-8')
                return json.loads(html)
        except:  # For some reason HTTPError wouldnt catch an HTTPError ?
            print('http error!')
            await asyncio.sleep(60)  # sleep to not grab a dead link over and over
            
async def detect_store_link(soup):
    if soup is not None:
        a = soup.findAll('a', class_="button green")  # Find green button class

        for x in range(0, len(a)):  # loop through multiple green buttons
            try:
                link = a[x]['href']  # Find green button with a link
                if link.find('store.fakku.net') != -1:  # Make sure that link contains a store link
                    return link  # return store link
            except:
                pass  # 'href' access wont work if it doesn't exist
    return None  # return nothing if store link does not exist


async def detect_magazine_text(soup):
    if soup is not None:
        try:
            a = soup.find('div', class_="left", text='Magazine')  # Find Magazine box
            text = a.next_sibling.next_sibling.text  # if it exists then we get a value, otherwise None
            return text
        except:
            pass
    return None


async def manga_string(m, release=''):
    artists = ", ".join(m.content_artists)
        
    release += 'Name: ' + \
               m.content_name + '\nArtists: ' + artists
    
    if m.magazine_text is not None:
        release += '\nMagazine: ' + m.magazine_text

    tags = ", ".join(m.content_tags)
    
    release += '\nTags: ' + tags + '\n' + m.content_url

    if m.store_link is not None:
        release += '\nBuy it here at: ' + m.store_link
    return release


async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')



async def fakku_script():
    await bot.wait_until_ready()  # will not begin until the bot is logged in
    most_recent = 0  # initialize most_recent
    while True:
        r = await get_fakku_json()
        if most_recent == 0:  # first request
            for s in r['index']:
                try:
                    if most_recent < int(s['content_date']):  # iteration required to prevent stickied releases
                        most_recent = int(s['content_date'])
                        most_recent_x = most_recent
                        print(most_recent)
                except KeyError:  # forum posts will cause this
                    pass
        else:  # all requests after the first
            for s in reversed(r['index']):  # iterate in case multiple releases are released at once.
                try:
                    if int(s['content_date']) > most_recent:  # compare against the last release
                        m = manga(s)  # create manga object
                        m.populate()  # populate the object with manga details, author, tags, etc
                        most_recent_x = int(s['content_date'])  # most most recent value in the loop

                        html = await get_html(s['content_url'])  # gets the manga page
                        if html is not None:
                            soup = BeautifulSoup(html, 'html.parser')  # start up html parser
                            store_link = await detect_store_link(soup)  # see if the store link exists
                            m.set_store_link(store_link)  # set store link
                            magazine_text = await detect_magazine_text(soup)  # see if the magazine link exists
                            m.set_magazine_text(magazine_text)  # set magazine link

                        print("New Release!")
                        release_string = await manga_string(m, 'New Release! \n')
                        await bot.send_message(bot.get_channel('196487186860867584'),
                                               release_string)  # send release details into the channel
                        await bot.send_message(bot.get_channel('202830118324928512'), release_string)
                except KeyError:  # forum posts will cause this
                    pass
        most_recent = most_recent_x
        await asyncio.sleep(60)  # Sleep for 60seconds


bot.loop.set_debug(True)
bot.loop.create_task(fakku_script())
bot.run(password.Token) # Put your own discord token here
