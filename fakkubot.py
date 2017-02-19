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
    
    
@bot.command(descriptoin="charge me daddy")
async def charge():
    await bot.say(":regional_indicator_c: :regional_indicator_h: :regional_indicator_a: :regional_indicator_r: :regional_indicator_g: :regional_indicator_e:  :regional_indicator_m: :regional_indicator_e:  :regional_indicator_d: :regional_indicator_a: :regional_indicator_d: :regional_indicator_d: :regional_indicator_y:!")
    
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

@bot.command(description=":regional_indicator_")
async def text(*message : str):
    string = ""
    for x in message:
        for i in x.lower():
            append = ":regional_indicator_" + i + ":"
            string +=  append
        string += "   "
    await bot.say(string)
    
@bot.command(description="its that time")
async def itsthattime():
    await bot.say('https://www.youtube.com/watch?v=shCYA2J-De8')

async def detect_http(url):
    return re.match(p, url)  # regex search for http or https is at the start of url



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
    if a[1].lower() in multi:
        data['multi'] = a[1].lower()    
    if a[2].lower() in dupe:
        data['dupcheck'] = a[2].lower()
        
    for question in a[3:]:
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
        
    release += 'Name: ' + \
               m.content_name
    
    if m.content_artists is not None:
        artists = ", ".join(m.content_artists)
        release += '\nArtists: ' + artists
        
    if m.magazine_text is not None:
        release += '\nMagazine: ' + m.magazine_text

    if m.content_tags is not None:
        tags = ", ".join(m.content_tags)
        release += '\nTags: ' + tags

    release += '\n' + m.content_url

    if m.store_link is not None:
        release += '\nBuy it here at: ' + m.store_link
    return release


async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


'''
I want this to crash if it fails
'''
async def login(username, password):
    r = requests.post('https://www.fakku.net/login/submit', data = {'username':username,'password':password})
    return r
    
async def get_front_page_links(soup):
    items = soup.findAll('a', class_='content-title')
    links = set()
    for manga in items:
        link = manga['href'][8:]
        links.add(link)
    return links
            
async def fakku_script():
    await bot.wait_until_ready()  # will not begin until the bot is logged in.
    manga_set = set()
    first = True
    r  = await login(password.username, password.password)
    cookies = r.cookies  
    while True:
        r = await must_get_request('https://fakku.net', cookies=cookies)
        soup = BeautifulSoup(r.text, 'html.parser')
        links = await get_front_page_links(soup)
        if first == True:
            manga_set = links
            first = False
        else:
            links.difference_update(manga_set)
            for book in links:
                data = await must_get_request("https://api.fakku.net/manga/"+book, cookies=cookies)
                book_json = data.json()['content']
                m = manga(book_json)
                m.populate()
                
                html = await get_html(book_json['content_url'])  # gets the manga page
                if html is not None:
                    soup = BeautifulSoup(html, 'html.parser')  # start up html parser
                    store_link = await detect_store_link(soup)  # see if the store link exists
                    m.set_store_link(store_link)  # set store link
                    magazine_text = await detect_magazine_text(soup)  # see if the magazine link exists
                    m.set_magazine_text(magazine_text)  # set magazine link

                print("New Release!")
                release_string = await manga_string(m, 'New Release! \n')
                await bot.send_message(bot.get_channel('196487186860867584'), release_string)  # send release details into the channel
                await bot.send_message(bot.get_channel('202830118324928512'), release_string)
                
            manga_set.update(links)
        await asyncio.sleep(60)

    
bot.loop.set_debug(True)
bot.loop.create_task(fakku_script())
bot.run(password.Token) # Put your own discord token here
