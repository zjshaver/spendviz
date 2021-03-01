class CreditCard:
	def __init__(self, name, day):
		self.name = name
		self.statement_day = day

	def getName(self):
		return self.name

	def getStatementDate(self):
		return self.statement_day
