from django.shortcuts import render
from django.http import JsonResponse
from .models import modbusDataTable
import json


# Create your views here.

"""
Description:
	The following function extracts the content of latest entry into database.
"""
def dataConversion(request):
	modelData = modbusDataTable.objects.latest('datetimestamp')
	if request.is_ajax():
		humanData = json.loads(modelData.humanData)
		machineData = json.loads(modelData.machineData)
		datetimestamp = modelData.datetimestamp
		return JsonResponse(humanData, safe=False)
	return render(request, 'option1/interface.html')
