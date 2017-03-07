import urllib2

def readDataFromURL(targetURL):
	"""
	Description:
	This function reads the text obtained from 'targetURL'.
	It parses the text into individual register reading, date as well as time.
	It returns a dictionary with keys as register number, and values as the corresponding value.
	The dictionary also includes the date and time.
	
	Input:
	targetURL: The url string from where text file is generated.
	
	Output:
	machineData: A dictionary that comprises the content of registers, as well as date and time.
	"""
	txt = urllib2.urlopen(targetURL)
	machineData = {}
	for line in txt:
		if '-' in line: # That is, this is the date and time field
			machineData['date'] = line.split(' ')[0]
			machineData['time'] = line.split(' ')[1].split('\n')[0]
		else:
			machineData[int(line.split(':')[0])] = int(line.split(':')[1])
	return machineData

def variableNames():
	"""
	Description:
	This function map the register number to the variable name.
	
	Input:
	None
	
	Output:
	dictVar: A dictionary that comprises of the register number as key, and the corresponding
	variable name as value. 
	"""
	dictVar =  {1: 'flow rate',
				3: 'energy flow rate',
				5: 'velocity',
				7: 'fluid sound speed',
				9: 'positive accumulator',
				11: 'positive decimal fraction',
				13: 'negative accumulator',
				15: 'negative decimal fraction',
				17: 'positive energy accumulator',
				19: 'positive energy decimal accumulator',
				21: 'negative energy accumulator',
				23: 'negative energy decimal accumulator',
				25: 'net accumulator',
				27: 'net decimal fraction',
				29: 'net energy accumulator',
				31: 'net energy decimal fraction',
				33: 'temperature inlet',
				35: 'temperature outlet',
				37: 'analog input AI3',
				39: 'analog input AI4',
				41: 'analog input AI5',
				43: 'current input at AI3',
				45: 'current input at AI3',
				47: 'current input at AI3',
				49: 'system passowrd',
				51: 'password for hardware',
				53: 'calendar',
				56: 'day+hour for auto-save',
				59: 'key to input',
				60: 'go to window',
				61: 'LCD back-lit lights for number of seconds',
				62: 'times for the beeper',
				72: 'error code',
				77: 'PT100 resistance of inlet',
				79: 'PT100 resistance of outlet',
				81: 'total travel time',
				83: 'delta travel time',
				85: 'upstream travel time',
				87: 'downstream travel time',
				89: 'output current',
				92: 'working step and signal quality',
				93: 'upstream strength',
				94: 'downstream strength',
				96: 'language used',
				97: 'rate of measured travel time ',
				99: 'reynolds number'}
	return dictVar

def convert2HumanData(machineData, dictVar):
	humanData = {}
	for key in machineData:
		if key in [1, 3, 5, 7, 11, 15, 19, 23, 27, 31, 33, 35, 37, 39, 41, 43]:
			regA = machineData[key]
			regB = machineData[key+1]
			humanData[dictVar[key]] = real4Conversion(regA, regB)
			print "(regA, regB): (%r, %r), %s: %r" %(regA, regB, 
														dictVar[key], humanData[dictVar[key]])
		elif key in [9, 13, 17, 21, 25, 29]:
			regA = machineData[key]
			regB = machineData[key+1]
			humanData[dictVar[key]] = longConversion(regA, regB)
			print "(regA, regB): (%r, %r), %s: %r" %(regA, regB, 
														dictVar[key], humanData[dictVar[key]])
	return humanData

def real4Conversion(regA, regB):
	"""
	Description:
	This function converts REAL4 formatted data to human readable.

	Input:
	regA and regB: The two register values for a particular variable.

	Output:
	value: The human readable equivalent of the binary(regB)+binary(regA)

	NOTES:
	http://stackoverflow.com/questions/16926130/python-convert-to-binary-and-keep-leading-zeros
	"""
	bin_form = format(regB, '016b') + format(regA, '016b')
	bin_form = bin_form[::-1]
	sign_value = 0.0
	exponent_value = 0.0
	fraction_value = 1.0

	for i in range(len(bin_form)):
		if i < 23:
			if int(bin_form[i]) == 1:
				fraction_value += int(bin_form[i]) *2**(i-23)
		elif i >= 23 and i <= 30:
			exponent_value += int(bin_form[i]) *2**(i-23)
		else:
			sign_value = (-1)**int(bin_form[i])

	value = sign_value * fraction_value * 2**(exponent_value-127)
	return value

def longConversion(regA, regB):
	regABin = format(regA, '016b')
	regBBin = format(regB, '016b')
	bin_form = regBBin + regABin
	if bin_form[0] == '1':
		bin_form_Compliment = twoCompliment(bin_form)
		return -int(bin_form_Compliment, 2)
	else:
		return int(bin_form, 2) 

def twoCompliment(bin_form):
	result = [0]*len(bin_form)
	carryBit = 1
	for i in range(len(bin_form)):
		if bin_form[i] == '0':
			result[i] = '1'
		else:
			result[i] = '0'

	# Adding 1 at the end
	if result[-1] == '0':
		result[-1] = '1'
	else:
		resultLength = len(result)
		for i in range(resultLength):
			if carryBit == 0:
				break
			if result[resultLength-i-1] == '1':
				result[resultLength-i-1] = '0'
				carryBit = 1
			else:
				result[resultLength-i-1] = '1'
				carryBit = 0
	return ''.join(result)

targetURL = "http://tuftuf.gambitlabs.fi/feed.txt"
machineData = readDataFromURL(targetURL)
print machineData
dictVar = variableNames()
convert2HumanData(machineData, dictVar)
"""
Tasks:

1. Parses the data
2. Converts it to human readable data like integers, decimals and strings.
3. Present it in a nice way
"""

