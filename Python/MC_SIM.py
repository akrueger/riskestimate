""" 
Monte Carlo analysis of stock market gain based on historical probability distributions.
"""

# Import XML Parser
import xml.etree.ElementTree as ET

# Parse XML directly from the file path
tree = ET.parse('I:/Python/retirement_source.xml')

# Create iterable item list
items = tree.findall('item')

# Create class for historic variables
class DataPoint:
	def __init__(self, low, high, freq):
		self.low = low
		self.high = high
		self.freq = freq
		
# Create Master Dictionary and variable list for historic variables
masterDictionary = {}

# Loop to assign variables as dictionary keys and associate their values with them
for item in items:
	thisKey = item.find('variable').text
	thisList = []
	masterDictionary[thisKey] = thisList
	
for item in items:
	thisKey = item.find('variable').text
	newDataPoint = DataPoint(float(item.find('low').text), float(item.find('high').text), float(item.find('freq').text))
	masterDictionary[thisKey].append(newDataPoint)
	

# Prompt user on number of iterations to run
starting_principal = int(raw_input('Starting principal: '))
yearly_investment = int(raw_input('Yearly investment: '))
max_years = int(raw_input('Number of years: '))
max_iterations = int(raw_input('Number of iterations: '))

iterations = 1

# List of all final lifetime worth scenarios
lifetime_worth = []

# Log list
logList = []


# Outer loop (total iterations)
while iterations <= max_iterations:

	principal_list = [starting_principal]
	
	# CPI Index
	CPI = [100]
	
	# Always start at zero years
	years = 1
	
	# Create the dice dictionary with list inside for each key so that values can be appended
	diceDictionary = {}
	for thisKey in masterDictionary.keys():
		thisList = []
		diceDictionary[thisKey] = thisList
	
	# Years loop
	while years <= max_years:
		
		# Dice roll for historic variables
		for thisKey in masterDictionary.keys():
			diceList = []
			diceList = masterDictionary[thisKey]
			import random #Import pseudo-random number generator
			randomValue = random.random()
			for i in range(len(diceList)):
				if randomValue <= sum(i.freq for i in diceList[0:i+1]):			
					diceRoll = random.uniform(diceList[i].low, diceList[i].high)
					diceDictionary[thisKey].append(diceRoll)
					break
					
	
		# Take the ending principal, then add interest, then add yearly investment
		principal_list.append(round(principal_list[years - 1],2) * diceDictionary['stock'][years - 1] + round(principal_list[years - 1],2) + yearly_investment)
		
		# Track the CPI inflation index each year
		CPI.append(CPI[years - 1] + diceDictionary['inflation'][years - 1] * CPI[years - 1])
	
		
		# Create list of lists for log file
		logListRow = []
		logListRow.append(iterations)
		logListRow.append(years)
		logListRow.append(round(principal_list[years - 1],2))
		logListRow.append(yearly_investment)
		logListRow.append(diceDictionary['stock'][years - 1])
		logListRow.append(diceDictionary['inflation'][years - 1])
		logListRow.append(CPI[years])
		logListRow.append(round(principal_list[years],2))
		logListRow.append(round(principal_list[years] * CPI[0] / CPI[years],2))
		logList.append(logListRow)

		#Test log file output
		#print iterations, 'iteration;', years, 'year;', round(principal_list[years - 1],2), 'beginning principal', yearly_investment, 'invested;', diceDictionary['stock'][years - 1], 'interest;', diceDictionary['inflation'][years - 1], 'inflation;', CPI[years], 'CPI;', round(principal_list[years],2), 'end principal;', round(principal_list[years] * CPI[0] / CPI[years],2), 'real end principal'
		
		# Extract the final year's principal
		final_end_principal = round(principal_list[-1],2)
	
		# Adjust for inflation--takes final CPI index and adjusts final end principal back to first year's $ value
		if years == max_years:
			final_end_principal = round(principal_list[-1] * CPI[0] / CPI[-1],2)
		
		# Recursion on inner loop
		years = years + 1
		
	
	# Append each iterations final principal to list to create distribution
	lifetime_worth.append(final_end_principal)
	
	# Recursion on outer loop
	iterations = iterations + 1
	

# Write final lifetime worth for every iteration
final_principal_file = open('I:/Python/test8.csv', 'wb')

for item in lifetime_worth:
  final_principal_file.write("%s\n" % item)

final_principal_file.close()

# Import CSV module
import csv

# Write log events
log_file = csv.writer(open('I:/Python/log.csv', 'wb'))
log_file.writerows(logList)