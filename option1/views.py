from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import modbusDataTable

from dataProcessing import readDataFromURL, variableNames, convert2HumanData2
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from django.db import IntegrityError
import json


# Create your views here.
def dataConversion(request):
	# modelData = modbusDataTable.objects.all()[2]
	modelData = modbusDataTable.objects.latest('datetimestamp')
	print "Human Data: \n", type(modelData.humanData)
	print "Machine Data: \n", type(json.loads(modelData.machineData))
	print "Date stamp: \n", type(modelData.datetimestamp)
	if request.is_ajax():
		print "AJAX activated."
		humanData = json.loads(modelData.humanData)
		machineData = json.loads(modelData.machineData)
		datetimestamp = modelData.datetimestamp
		print humanData
		return JsonResponse(humanData, safe=False)
	return render(request, 'option1/interface.html')

def test(request):
	modelData = modbusDataTable.objects.latest('datetimestamp')
	data = json.loads(modelData.machineData)
	print data
	return JsonResponse(data, safe=False)


def redesignDatacollection(request):

	# url = "http://tuftuf.gambitlabs.fi/feed.txt"
	# [datetimestamp, machineData] = readDataFromURL(url)
	# parse_datetimestamp = parse_datetime(datetimestamp)

	modelData = modbusDataTable.objects.all()[0]
	print "timestamp is: ", modelData.datetimestamp
	machineData = modelData.machineData
	print "machineData: ", json.loads(machineData)
	dictVar = variableNames()
	humanData = convert2HumanData2(machineData, dictVar)
	print "humanData: ", humanData

	# for key in humanData:
	# 	if key == 'reynolds number':
	# 		print humanData[key]
	# 		for data_key in humanData[key]:
	# 			print type(data_key), ":", humanData[key][data_key]

	# if not is_aware(parse_datetimestamp):
	# 	parse_datetimestamp = make_aware(parse_datetimestamp)
	# dataEntry = modbusDataTable(datetimestamp = parse_datetimestamp,
	# 							machineData = json.dumps(humanData))
	# try:
	# 	dataEntry.save()
	# except IntegrityError:
	# 	print "Preventing duplicate data to enter our database :)."
	# else:
	# 	print "New data entered to the server."
	return HttpResponse("Some data collection occuring in background")