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

def dollarStringToNumber(dollar_string):
	numeric_value = 0.0

	# float conversion doesn't like commas so remove them
	dollar_string = dollar_string.replace(',', '')

	# remove $ and any leading +/- character
	parts = dollar_string.split('$')
	if (len(parts) > 1):
		value_string = parts[1]
		numeric_value = float(value_string)

	return numeric_value