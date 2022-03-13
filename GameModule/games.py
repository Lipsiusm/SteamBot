#class represents an object on sale at the steam store

class Game:

	discount_percent=''
	sale_price=''
	title=''

	def __init__(self, discount_percent, sale_price, title):
		self.discount_percent = discount_percent
		self.sale_price = sale_price
		self.title = title

	def get_title():
		return self.title

	def get_discount_percent():
		return self.discount_percent

	def get_orig_price():
		return self.sale_price
