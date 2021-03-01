# -*- coding: utf-8 -*-
import datetime
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
	current_day = '01'

	current_year, current_month, current_day = helpers.getDateParts(current_date)
	trans_year, trans_month, trans_day = helpers.getDateParts(transaction.getDate())
		
	if transaction.getAccount() in bank_accounts:
		if trans_month == current_month:
			status = True
	else:
		print('trans: ',transaction.getAccount())
		for card in credit_cards:
			print(card.getName())
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
				print(statement_start)
				statement_end = datetime.datetime(end_year, end_month, end_day)
				print(statement_end)
				trans_date = datetime.datetime(int(trans_year), int(trans_month), int(trans_day))
				print(trans_date)

	return status

def processTransactions(df, bank_accounts, credit_cards, current_date):
	# ignore certain transaction type (income, transfers, etc.)
	filter_ = (df['Category'] != 'Transfers') & \
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
	for row_label, row in df_filtered.iterrows():
		t = Transaction(row['Date'], row['Description'], row['Category'], row['Account Name'], row['Amount'])
		# Determine if transaction is valid for this months finances.
		# For credit card charges that means on the statement being
		# paid this month. For bank accounts that means simply within
		# the dates of this month.
		if validTransaction(t, bank_accounts, credit_cards, current_date):
			transactions.append(t)
		#print(row_label, row, sep='\n', end='\n\n')
	print(len(transactions))

	

        