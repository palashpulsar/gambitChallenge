from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import modbusDataTable, humanReadableDataTable
import urllib2
import json
from django.utils.dateparse import parse_datetime
from dataProcessing import variableNames, convert2HumanData, readDataFromURL


# Create your views here.

def modbusDataEntry(request):
	url = "http://tuftuf.gambitlabs.fi/feed.txt"
	[datetimestamp, machineData] = readDataFromURL(url)
	dataEntry = modbusDataTable(datetimestamp=parse_datetime(datetimestamp), dataset=json.dumps(machineData))
	try:
		dataEntry.save()
	except IntegrityError:
		print "Preventing duplicate data to enter our database :)."
	else:
		dictVar = variableNames()
		humanData = convert2HumanData(machineData, dictVar)
		humanDataEntry = humanReadableDataTable(datetimestamp=parse_datetime(datetimestamp), dataset=json.dumps(humanData))
		humanDataEntry.save()
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