from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField

from django.db import models

# Create your models here.
class modbusDataTable(models.Model):
	datetimestamp = models.DateTimeField(unique=True)
	dataset = JSONField()
	def __unicode__(self):
		return unicode(self.datetimestamp)

class humanReadableDataTable(models.Model):
	datetimestamp = models.DateTimeField(unique=True)
	dataset = JSONField()
	def __unicode__(self):
		return unicode(self.datetimestamp)

# NOTE:
# http://stackoverflow.com/questions/9910535/django-coercing-to-unicode-need-string-or-buffer-datetime-date-found
# https://docs.djangoproject.com/en/dev/ref/utils/#module-django.utils.dateparse
