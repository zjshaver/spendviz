class Transaction:
	def __init__(self, date, desc, category, account, amount):
		self.date = date
		self.description = desc
		self.category = category
		self.account = account
		self.amount = amount

	def getAccount(self):
		return self.account

	def getDate(self):
		return self.date

	def getCategory(self):
		return self.category

	def getAmount(self):
		return self.amount