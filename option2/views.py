from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

# Create your views here.

def test(request):
	return HttpResponse("Testing")

