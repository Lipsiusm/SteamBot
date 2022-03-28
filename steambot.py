import requests
import os
import json
import discord
from games import *
from bs4 import BeautifulSoup as bs

#nabbin up them current specials
store_url= 'https://store.steampowered.com/specials/#tab=TopSellers'

test = 'https://en.wikipedia.org/wiki/Python_(programming_language)'

#this is the class i need to grab for the ETA of next sale
#<span class="huge-countdown" id="js-sale-countdown" data-target="1647277200000">05 : 12 : 53 : 46</span>
#figure out how to grab specific headers
def main():
    sales_to_post=current_top_sellers()
    run_bot(sales_to_post)

def run_bot(data):
    # client = discord.Client()
    token = ''
    webhook = ''

    data = {
        "content" : "Hello",

        "username" : "SteamBot"
    }

    result = requests.post(webhook, headers={'Authorization': ''}, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

    # webhook = discord.Webhook.partial(
    #     STATUS_WEBHOOK_ID,
    #     STATUS_WEBHOOK_TOKEN,
    #     adapter=discord.RequestsWebhookAdapter(),
    # )

def current_top_sellers():

    return_games = []
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

    return return_games


#if this application was run directly, run it
if __name__ == "__main__":
    main()