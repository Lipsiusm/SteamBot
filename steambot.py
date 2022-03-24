import time
import requests
from dotenv import load_dotenv
from games import *
from bs4 import BeautifulSoup as bs

#nabbin up them current specials
store_url= 'https://store.steampowered.com/specials/#tab=TopSellers'

test = 'https://en.wikipedia.org/wiki/Python_(programming_language)'

#this is the class i need to grab for the ETA of next sale
#<span class="huge-countdown" id="js-sale-countdown" data-target="1647277200000">05 : 12 : 53 : 46</span>
#figure out how to grab specific headers
def main():
	current_top_sellers()

def current_top_sellers():

	games = []
	feed = requests.get(store_url)
	soup = bs(feed.text, 'html.parser')
	games = soup.find_all(class_=['tab_item_name', 'discount_pct', 'discount_final_price'])
	continue_looping = True

	#cut tag info off the items in the list
	for i in range (len(games)):
		games[i] = games[i].get_text()
		#print(games[i])

	new_game = Game(games[0], games[1],games[2])
	print(new_game.get_title())
	
	# while continue_looping:
	# 	pct = games.pop(0)
	# 	cost = games.pop(1)
	# 	title = games.pop(2)
	# 	new_game = Game(pct, cost, title)


#send the items from the sale to the discord webhook id
#def post_to_disc():
	#sales = {}


#if this application was run directly, run it
if __name__ == "__main__":
    main()