import time
import requests
from dotenv import load_dotenv
import games
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
	soup = soup.find_all('tabarea')
	games = soup.find_all(class_=['tab_item_name', 'discount_pct', 'discount_final_price'])

	#cut tag info off the items in the list
	for i in range (len(games)):
		games[i] = games[i].get_text()
		print (games[i])
	"""
	this is where im going to start storing game objects
	class tab_item_name
	class discount_pct
	class discount_original_price
	class discount_final_price
	anchor tag href
	"""

#send the items from the sale to the discord webhook id
#def post_to_disc():
	#sales = {}


#if this application was run directly, run it
if __name__ == "__main__":
    main()