# -*- coding: utf-8 -*-
import datetime
import numpy as np 
from matplotlib import pyplot as plt 
from . import helpers
from .CreditCard import CreditCard
from .Transaction import Transaction

import xml.etree.ElementTree as ET

def initAccounts(info_file):
	credit_cards = []
	bank_accounts = []
	tree = ET.parse(info_file)
	root = tree.getroot()

	for card in root.findall('./creditcards/card'):
		cc = CreditCard(card[0].text,card[1].text)
		credit_cards.append(cc)
		#print(cc.getName(), cc.getStatementDate())

	for account in root.findall('./account'):
		bank_accounts.append(account[0].text)
		#print(account[0].text)

	return credit_cards, bank_accounts

def validTransaction(transaction, bank_accounts, credit_cards, current_date):
	# defaults
	status = False
	current_year = '2021'
	current_month = '01'

	current_year, current_month, current_day = helpers.getDateParts(current_date)
	trans_year, trans_month, trans_day = helpers.getDateParts(transaction.getDate())
		
	if transaction.getAccount() in bank_accounts:
		if trans_month == current_month:
			status = True
	else:
		#print('trans: ',transaction.getAccount())
		for card in credit_cards:
			#print(card.getName())
			if transaction.getAccount() == card.getName():
				start_year = int(current_year)
				end_year = int(current_year)
				start_month = int(current_month) - 1
				end_month = int(current_month)
				start_day = int(card.getStatementDate()) + 1
				end_day = int(card.getStatementDate())
				if (current_month == '01'):
					start_year = int(current_year) - 1
					start_month = 12
				
				statement_start = datetime.datetime(start_year, start_month, start_day)
				print("\n",statement_start)
				statement_end = datetime.datetime(end_year, end_month, end_day)
				print(statement_end)
				trans_date = datetime.datetime(int(trans_year), int(trans_month), int(trans_day))
				print(trans_date)
				if statement_start <= trans_date <= statement_end:
					print("VALID!!!")
					status = True

	return status

def processTransactions(df, bank_accounts, credit_cards, current_date):
	# ignore certain transaction type (income, transfers, etc.)
	filter_ = (df['Category'] != 'Transfers') & \
		(df['Category'] != 'Education') & \
		(df['Category'] != 'Paychecks/Salary') & \
		(df['Category'] != 'Other Income') & \
		(df['Category'] != 'Interest') & \
		(df['Category'] != 'Deposits') & \
		(df['Category'] != 'Securities Trades') & \
		(df['Category'] != 'Investment Income') & \
		(df['Category'] != 'Retirement Contributions') & \
		(df['Category'] != 'Uncategorized') & \
		(df['Category'] != 'Credit Card Payments')
	df_filtered = df[filter_]
	#print(df[filter_])
	transactions = []
	# Dictionary of category:total_amount key:value pairs.
	categories = {}
	for row_label, row in df_filtered.iterrows():
		numeric_dollar_amount = helpers.dollarStringToNumber(row['Amount'])
		t = Transaction(row['Date'], row['Description'], row['Category'], row['Account Name'], numeric_dollar_amount)
		# Determine if transaction is valid for this months finances.
		# For credit card charges that means on the statement being
		# paid this month. For bank accounts that means simply within
		# the dates of this month.
		if validTransaction(t, bank_accounts, credit_cards, current_date):
			transactions.append(t)
			current_category = t.getCategory()
			if current_category not in categories.keys():
				categories[current_category] = t.getAmount()
			else:
				current_sum = categories[current_category]
				categories[current_category] = round((current_sum + t.getAmount()), 2)
		#print(row_label, row, sep='\n', end='\n\n')
	#print(categories)
	print(len(transactions))

	return categories

def visualizeData(category_data):
	s = sorted(category_data.items(),key=lambda x: (x[1],len(x[0])),reverse=True)
	#print(s)
	sorted_data = {}
	for k,v in s:
		sorted_data[k] = v
	print(sorted_data)

	# Creating autocpt arguments 
	def func(pct, allvalues): 
		absolute = int(pct / 100.*np.sum(allvalues)) 
		return "{:.1f}%\n(${:d})".format(pct, absolute) 
 
	fig1, ax1 = plt.subplots()
	ax1.pie(sorted_data.values(),
		labels=sorted_data.keys(),
		autopct=lambda pct: func(pct, list(sorted_data.values())),
		startangle=180,
		pctdistance=0.85)
		
	#draw circle
	centre_circle = plt.Circle((0,0),0.7,fc='white')
	fig = plt.gcf()
	fig.gca().add_artist(centre_circle)# Equal aspect ratio ensures that pie is drawn as a circle
	ax1.axis('equal')  
	plt.tight_layout()

	# show plot 
	plt.show() 

	

        