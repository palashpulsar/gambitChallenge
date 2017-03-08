from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import modbusDataTable, humanReadableDataTable
import urllib2
import json
from django.utils.dateparse import parse_datetime
from dataProcessing import variableNames, convert2HumanData, readDataFromURL
from django.utils.timezone import is_aware, make_aware


# Create your views here.

def modbusDataEntry(request):
	url = "http://tuftuf.gambitlabs.fi/feed.txt"
	[datetimestamp, machineData] = readDataFromURL(url)
	parse_datetimestamp = parse_datetime(datetimestamp)
	if not is_aware(parse_datetimestamp):
		print "I am here."
		parse_datetimestamp = make_aware(parse_datetimestamp)
	dataEntry = modbusDataTable(datetimestamp=parse_datetimestamp, dataset=json.dumps(machineData))
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
	# NOTE: http://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime

def modbusDataEntryAutomate():
	url = "http://tuftuf.gambitlabs.fi/feed.txt"
	[datetimestamp, machineData] = readDataFromURL(url)
	dataEntry = modbusDataTable(datetimestamp=parse_datetime(datetimestamp), dataset=json.dumps(machineData))
	try:
		dataEntry.save()
	except IntegrityError:
		print "Preventing duplicate data to enter our database :)."
	return