import requests
import os
import json
import discord
import math
from games import *
from bs4 import BeautifulSoup as bs

#this is the class i need to grab for the ETA of next sale
#<span class="huge-countdown" id="js-sale-countdown" data-target="1647277200000">05 : 12 : 53 : 46</span>
#figure out how to grab specific headers

def main():
    #sales_to_post=current_top_sellers()
    #run_bot(sales_to_post)
    convert_to_usd()

def convert_to_usd(cdn_cost):

    #grab the current CAD to USD conversion rate
    url = 'https://www.google.com/finance/quote/CAD-USD'
    feed = requests.get(url)
    soup = bs(feed.text, 'html.parser')
    grab_rate = soup.find_all(class_='YMlKec fxKbKc')
    
    #convert the value and return it
    conversion_rate = grab_rate[0].get_text()
    conversion_rate = float(conversion_rate)
    usd_amount = conversion_rate * cdn_cost
    usd_amount = round(conversion_rate, 2)
    return usd_amount

def run_bot(data):
    

    # DIG_webhook=''
    # SMP_webhook=''
    sales = ''

    for game in data:
        sales = sales + f'{game}\n'
        
    #embed the sales for a good looking output
    data_to_send = {
        "username": "SteamBot",
        "embeds": [
            {
                "title": "Steam Sales",
                "description": sales,
                "color": "16704809",
            }
        ],
    }

    result = requests.post(DIG_webhook, data = json.dumps(data_to_send), headers={'Content-Type':'application/json'})


def current_top_sellers():

    #nabbin up them current specials
    store_url= 'https://store.steampowered.com/specials/#tab=TopSellers'
    return_games = []
    return_list = []
    feed = requests.get(store_url)
    soup = bs(feed.text, 'html.parser')
    games = soup.find_all(class_=['tab_item_name', 'discount_pct', 'discount_final_price'])
    continue_looping = True
    
    #cut tag info off the items in the list
    for i in range (len(games)):
        games[i] = games[i].get_text()

    while continue_looping:
        pct = games.pop(0)
        cost = games.pop(0)
        #stripping the CDN dollar characters and white space to save character spaces
        cost = cost.strip('CDN')
        title = games.pop(0)

        #checking to see if title is a random untitled tag with ascii values
        #48 -> 57 are numbers, as theres numbers in certain titles
        #97 -> 122 is a - z
        
        if ord(title[0].lower()) < 97 and ord(title[0].lower()) < 48 or ord(title[0].lower()) > 122 and ord(title[0].lower()) > 57:
            continue_looping = False
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