from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse


# Create your views here.
def visualization(request):
	return render(request, 'option2/interface.html')