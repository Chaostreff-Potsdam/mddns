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

	def get_form(self, request, obj=None, **kwargs):
		form = super(RecordNameAdmin, self).get_form(request, obj, **kwargs)
		if obj is None:
			form.base_fields['zone'].initial = self.availableZones(request).first()
		return form

	def availableZones(self, request):
		return Zone.objects.filter().order_by('pk')

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):

	def get_readonly_fields(self, request, obj=None):
		if obj is None:
			return []
		else:
			return ["name"]
