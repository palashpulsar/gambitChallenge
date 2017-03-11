from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from option1.models import modbusDataTable
import json

# Create your views here.

def test(request):
	return render(request, 'option2/test.html')

def visualization(request):
	print "Am I here?"
	return render(request, 'option2/visualization.html')

def varType_Modbus(request):
	varList = [];
	modelData = modbusDataTable.objects.latest('datetimestamp')
	for key in json.loads(modelData.machineData):
		varList.append(key)
	print varList
	return JsonResponse(varList, safe=False)

def varType_Human(request):
	varList = [];
	modelData = modbusDataTable.objects.latest('datetimestamp')
	for key in json.loads(modelData.humanData):
		varList.append(key)
	print varList
	return JsonResponse(varList, safe=False)


def callForModbusData(request, numElement=5, regNum = 1):
	print "callForModbusData is selected."

	# Defining what are the keys (the first 100 registers) from the latest entry
	modelData = modbusDataTable.objects.latest('datetimestamp')
	modbusData = dict.fromkeys((str(key) for key in json.loads(modelData.machineData)), [])
	modbusData['datetimestamp'] = []
	
	# Element limit ?? (ie, number of data for an element that we want to show. Lets start with 5.)
	numElement = 1
	
	allEntry = modbusDataTable.objects.all().order_by('-datetimestamp')[:numElement]
	allEntry = reversed(allEntry)
	for obj in allEntry:
		dataDict = json.loads(obj.machineData)

		# for key in modbusData:
		# 	if key == 'datetimestamp':
		# 		modbusData['datetimestamp'].append(obj.datetimestamp)
		# 	else:
		# 		print "key: ", key
		# 		print "modbusData[key]: ", modbusData[key]
		# 		print "dataDict[key]: ", dataDict[key]
		# 		modbusData[key].append(dataDict[key])
		# 		print "modbusData[key]: ", modbusData[key]
		# 		print "\n"

		for key in dataDict:
			print "key: ", key
			print "dataDict[key]: ", dataDict[key]
			print "\n"
		modbusData['datetimestamp'].append(obj.datetimestamp)
	print modbusData['datetimestamp']
	print modbusData
	return HttpResponse("Testing")

def callForHumanData(request):
	print "callForHumanData is selected."
	return HttpResponse("Testing")


