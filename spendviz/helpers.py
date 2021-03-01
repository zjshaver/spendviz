def cleanupFile(file_path):
	with open(file_path,'r') as f:
		with open("data/transactions.csv",'w') as f1:
			next(f) # skip header line
			for line in f:
					f1.write(line)

def getDateParts(date_string):
	year = ''
	month = ''
	day = ''

	date_parts = date_string.split('-')
	if (len(date_parts) > 2):
		year = date_parts[0]
		month = date_parts[1]
		day = date_parts[2]

	return year, month, day