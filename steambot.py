import requests
import json
import math
from games import *
from bs4 import BeautifulSoup as bs

#this is the class i need to grab for the ETA of next sale
#<span class="huge-countdown" id="js-sale-countdown" data-target="1647277200000">05 : 12 : 53 : 46</span>
#figure out how to grab specific headers

def main():
    cdn_data = cdn_top_sellers()
    usd_data = usd_top_sellers()
    run_bot(cdn_data, usd_data)


def run_bot(cdn_data, usd_data):
    
    with open("../bot_info.json", "r") as webhook_file:
        webhooks  = json.load(webhook_file)

    DIG_webhook = webhooks['DIG_webhook']
    SMP_webhook = webhooks['SMP_webhook']
    
    cdn_sales = ''
    usd_sales = ''

    for sale in cdn_data:
        cdn_sales = cdn_sales + f'{sale}\n'

    for sale in usd_data:
        usd_sales = usd_sales + f'{sale}\n'

    #embed the sales for a good looking output
    DIG_data = {
        "username": "SteamBot",
        "embeds": [
            {
                "title": "Steam Sales ",
                "description": cdn_sales,
                "color": "16704809",
            }
        ],
    }

    SMP_data = {
        "username": "SteamBot",
        "embeds": [
            {
                "title": "Steam Sales ",
                "description": usd_sales,
                "color": "16704809",
            }
        ],
    }

    DIG_result = requests.post(DIG_webhook, data = json.dumps(DIG_data), headers={'Content-Type':'application/json'})
    SMP_result = requests.post(SMP_webhook, data = json.dumps(SMP_data), headers={'Content-Type':'application/json'})

def usd_top_sellers():

    proxy = {
    'https' : '20.81.62.32:3128'
    }

    #nabbin up them current specials
    store_url= 'https://store.steampowered.com/specials/#tab=TopSellers'
    return_games = []
    return_list = []
    feed = requests.get(store_url,proxies=proxy)
    soup = bs(feed.text, 'html.parser')
    games = soup.find_all(class_=['tab_item_name', 'discount_pct', 'discount_final_price'])
    
    #cut tag info off the items in the list
    for i in range (len(games)):
        games[i] = games[i].get_text()

    for i in games:

        pct = games.pop(0)
        cost = games.pop(0)
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

def cdn_top_sellers():

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

        #stripping the CDN dollar characters and white space to save character spaces
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


#if this application was run directly, run it
if __name__ == "__main__":
    main()