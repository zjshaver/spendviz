import datetime
import pandas as pd
from .helpers import cleanupFile
from .core import initAccounts
from .core import processTransactions
from .core import visualizeData

credit_cards = []
bank_accounts = []
bucket_results = {}

# Assume processing data for the current month
#dt = datetime.datetime.now()
dt = datetime.datetime(2021, 2, 28)
current_date = dt.strftime("%Y-%m-%d")
print(current_date)

cleanupFile('data/Transactions_For_All_Accounts_From_Nov_2020_to_Feb_2021.CSV')
credit_cards, bank_accounts = initAccounts('data/accounts.xml')
df = pd.read_csv ('data/transactions.csv',usecols=['Date', 'Description', 'Category', 'Account Name', 'Amount'])
bucket_results = processTransactions(df, bank_accounts, credit_cards, current_date)
visualizeData(bucket_results)