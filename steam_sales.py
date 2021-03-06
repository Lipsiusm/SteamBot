import requests
import json
from games import *
from bs4 import BeautifulSoup as bs

def send_info(data):
    
    with open("../bot_info.json", "r") as webhook_file:
        bot_info  = json.load(webhook_file)

    DIG_webhook = bot_info['DIG_WEBHOOK']
    
    sales = ''

    for sale in data:
        sales = sales + f'{sale}\n'

    #embed the sales for a good looking output
    DIG_data = {
        "username": "SteamBot",
        "embeds": [
            {
                "title": "Steam Sales ",
                "description": sales,
                "color": "16704809",
            }
        ],
    }

    DIG_result = requests.post(DIG_webhook, data = json.dumps(DIG_data), headers={'Content-Type':'application/json'})

def top_sellers():

    #nabbin up them current specials
    store_url= 'https://store.steampowered.com/specials/#tab=TopSellers'
    return_games = []
    return_list = []
    feed = requests.get(store_url)
    soup = bs(feed.text, 'html.parser')
    games = soup.find_all(class_=['tab_item_name', 'discount_pct', 'discount_final_price'])
    
    #cut tag info off the items in the list
    for i in range (len(games)):
        games[i] = games[i].get_text()

    for i in games:

        pct = games.pop(0)
        cost = games.pop(0)

        #stripping the CDN dollar characters to save character spaces
        cost = cost.strip('CDN')
        title = games.pop(0)


        #checking to see if title is a random untitled tag with ascii values
        #48 -> 57 are numbers, as theres numbers in certain titles
        #97 -> 122 is a - z
        if ord(title[0].lower()) < 97 and ord(title[0].lower()) < 48 or ord(title[0].lower()) > 122 and ord(title[0].lower()) > 57:
            break

        new_game = Game(pct, cost, title)
        
        if new_game not in return_games:
            return_games.append(new_game)

    for i in return_games:
        return_list.append(f'{i.get_title()} - {i.get_cost()} ({i.get_discount()} off)')

    return return_list
    