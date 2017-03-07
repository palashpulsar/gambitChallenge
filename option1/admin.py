from django.contrib import admin
from .models import modbusDataTable, humanReadableDataTable

# Register your models here.
admin.site.register(modbusDataTable)
admin.site.register(humanReadableDataTable)