from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import modbusDataTable
import urllib2
import json
from django.utils.dateparse import parse_datetime


# Create your views here.

def modbusDataEntry(request):
	url = "http://tuftuf.gambitlabs.fi/feed.txt"
	[datetimestamp, machineData] = readDataFromURL(url)
	dataEntry = modbusDataTable(datetimestamp=parse_datetime(datetimestamp), dataset=json.dumps(machineData))
	try:
		dataEntry.save()
	except IntegrityError:
		print "Preventing duplicate data to enter our database :)."
	return HttpResponse("Testing")

def modbusDataEntryAutomate():
	url = "http://tuftuf.gambitlabs.fi/feed.txt"
	[datetimestamp, machineData] = readDataFromURL(url)
	dataEntry = modbusDataTable(datetimestamp=parse_datetime(datetimestamp), dataset=json.dumps(machineData))
	try:
		dataEntry.save()
	except IntegrityError:
		print "Preventing duplicate data to enter our database :)."
	return

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
			# machineData['date'] = line.split(' ')[0]
			# machineData['time'] = line.split(' ')[1].split('\n')[0]
			datetimestamp = line.split('\n')[0]
		else:
			machineData[int(line.split(':')[0])] = int(line.split(':')[1])
	# print datetimestamp
	# print "modbus data:\n", machineData
	return [datetimestamp, machineData]