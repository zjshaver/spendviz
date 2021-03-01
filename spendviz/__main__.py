import datetime
import pandas as pd
from .helpers import cleanupFile
from .core import initAccounts
from .core import processTransactions

credit_cards = []
bank_accounts = []

# Assume processing data for the current month
dt = datetime.datetime.now()
current_date = dt.strftime("%Y-%m-%d")
current_month = dt.strftime("%m")
print(current_date)
#print(current_date.strftime("%x"))

cleanupFile('data/Transactions_For_All_Accounts_From_Nov_2020_to_Feb_2021.CSV')
credit_cards, bank_accounts = initAccounts('data/accounts.xml')
df = pd.read_csv ('data/transactions.csv',usecols=['Date', 'Description', 'Category', 'Account Name', 'Amount'])
processTransactions(df, bank_accounts, credit_cards, current_date)