from django.contrib import admin

from .models import *

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
	def get_readonly_fields(self, request, obj=None):
		if obj is None:
			return []
		else:
			return ["zone"]


@admin.register(RecordName)
class RecordNameAdmin(admin.ModelAdmin):
	def get_readonly_fields(self, request, obj=None):
		if obj is None:
			return []
		else:
			return ["zone", "name"]


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
	def get_readonly_fields(self, request, obj=None):
		if obj is None:
			return []
		else:
			return ["name"]
