import urllib2
from django.db import IntegrityError
from .models import modbusDataTable
import json
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware


def readDataFromURL(targetURL):
	txt = urllib2.urlopen(targetURL)
	machineData = {}
	for line in txt:
		if '-' in line: # That is, this is the date and time field
			datetimestamp = line.split('\n')[0]
		else:
			machineData[int(line.split(':')[0])] = int(line.split(':')[1])
	return [datetimestamp, machineData]


def modbusDataEntryAutomate():
	url = "http://tuftuf.gambitlabs.fi/feed.txt"
	[datetimestamp, machineData] = readDataFromURL(url)
	parse_datetimestamp = parse_datetime(datetimestamp)
	dictVar = variableNames()
	humanData = convert2HumanData2(machineData, dictVar)
	print humanData
	if not is_aware(parse_datetimestamp):
		parse_datetimestamp = make_aware(parse_datetimestamp)
	dataEntry = modbusDataTable(datetimestamp = parse_datetimestamp,
								machineData = json.dumps(machineData),
								humanData = json.dumps(humanData))
	try:
		dataEntry.save()
	except IntegrityError:
		print "Preventing duplicate data to enter our database :)."
	else:
		print "New data entered to the server."
	return 

def OldmodbusDataEntryAutomate():
	url = "http://tuftuf.gambitlabs.fi/feed.txt"
	[datetimestamp, machineData] = readDataFromURL(url)
	parse_datetimestamp = parse_datetime(datetimestamp)
	dictVar = variableNames()
	humanData = convert2HumanData(machineData, dictVar)
	if not is_aware(parse_datetimestamp):
		parse_datetimestamp = make_aware(parse_datetimestamp)
	dataEntry = modbusDataTable(datetimestamp = parse_datetimestamp,
								machineData = json.dumps(machineData),
								humanData = json.dumps(humanData))
	try:
		dataEntry.save()
	except IntegrityError:
		print "Preventing duplicate data to enter our database :)."
	else:
		print "New data entered to the server."
	return
	# NOTE: http://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime


def variableNames():
	
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

def convert2HumanData2(machineData, dictVar):
	humanData = {}
	for key in machineData:
		if key in [1, 3, 5, 7, 11, 15, 19, 23, 27, 31, 33, 35, 37, 39, 41, 43,
					45, 47, 77, 79, 81, 83, 85, 87, 89, 97, 99]:
			regA = machineData[key]
			regB = machineData[key+1]
			humanData[dictVar[key]] = {"A": machineData[key], "B": machineData[key+1], 
										"human": real4Conversion(regA, regB)}
		elif key in [9, 13, 17, 21, 25, 29]:
			regA = machineData[key]
			regB = machineData[key+1]
			humanData[dictVar[key]] = {"A": machineData[key], "B": machineData[key+1], 
										"C": None, "human": real4Conversion(regA, regB)}
		elif key in [49, 51, 53, 56]:
			if key == 53:
				humanData[dictVar[key]] = {"A": machineData[key], "B": machineData[key+1], 
											"C": machineData[key+2], "human": [machineData[key], 
															machineData[key+1], machineData[key+2]]}

			elif key == 49:
				humanData[dictVar[key]] = {"A": machineData[key], "B": machineData[key+1], "C": None,
											"human": [machineData[key], machineData[key+1]]}

			else:
				humanData[dictVar[key]] = {"A": machineData[key], "B": None,
											"C": None, "human": machineData[key]}
		elif key in [59, 60, 61, 62, 92, 93, 94, 96]:
			regA = machineData[key]
			humanData[dictVar[key]] = {"A": machineData[key], "B": None,
										"C": None, "human": integerConversion(regA, key)}
		elif key == 72:
			humanData[dictVar[key]] = {"A": machineData[key], "B": None, 
										"C": None, "human": machineData[key]}
	return humanData


def convert2HumanData(machineData, dictVar):
	humanData = {}
	for key in machineData:
		if key in [1, 3, 5, 7, 11, 15, 19, 23, 27, 31, 33, 35, 37, 39, 41, 43,
					45, 47, 77, 79, 81, 83, 85, 87, 89, 97, 99]:
			regA = machineData[key]
			regB = machineData[key+1]
			humanData[dictVar[key]] = real4Conversion(regA, regB)
		elif key in [9, 13, 17, 21, 25, 29]:
			regA = machineData[key]
			regB = machineData[key+1]
			humanData[dictVar[key]] = longConversion(regA, regB)
		elif key in [49, 51, 53, 56]:
			if key == 53:
				humanData[dictVar[key]] = [machineData[key], 
											machineData[key+1], machineData[key+2]]
			elif key == 49:
				humanData[dictVar[key]] = [machineData[key], machineData[key+1]]
			else:
				humanData[dictVar[key]] = machineData[key]
		elif key in [59, 60, 61, 62, 92, 93, 94, 96]:
			regA = machineData[key]
			humanData[dictVar[key]] = integerConversion(regA, key)		
		elif key == 72:
			humanData[dictVar[key]] = machineData[key]
	return humanData

def integerConversion(regA, key):
	if key == 96:
		if regA == 0:
			return 'English'
		elif regA == 1:
			return 'Chinese'
		else:
			return 'Other language'

	elif key == 92:
		bin_form = format(regA, '016b')
		workingStepBin = bin_form[0:8]
		signalQualityBin = bin_form[8:16]
		return [int(workingStepBin, 2), int(signalQualityBin, 2)]
	else:
		return regA

def real4Conversion(regA, regB):
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

"""
	Description:
	This function map the register number to the variable name.
	
	Input:
	None
	
	Output:
	dictVar: A dictionary that comprises of the register number as key, and the corresponding
	variable name as value. 
	"""

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
