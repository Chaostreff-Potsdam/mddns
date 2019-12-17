from django.contrib import admin

from .models import *

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):

	def get_readonly_fields(self, request, obj=None):
		if obj is None:
			return []
		else:
			return ["zone"]

	def get_queryset(self, request):
		return self.availableZones(request)

	@classmethod
	def availableZones(cls, request):
		if request.user.is_superuser:
			return Zone.objects.all()
		return Zone.objects.filter(allowed_users__id__exact=request.user.id).order_by('pk')


@admin.register(RecordName)
class RecordNameAdmin(admin.ModelAdmin):

	filter_horizontal = ('owners',)

	def get_readonly_fields(self, request, obj=None):
		if obj is None:
			return []
		else:
			return ["zone", "name"]

	def get_form(self, request, obj=None, **kwargs):
		form = super(RecordNameAdmin, self).get_form(request, obj, **kwargs)
		if obj is None:
			form.base_fields['zone'].initial = ZoneAdmin.availableZones(request).first()
			form.base_fields['owners'].initial = [request.user]
		return form

	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		if db_field.name == "zone":
			kwargs["queryset"] = ZoneAdmin.availableZones(request)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def get_queryset(self, request):
		return self.availableNames(request)

	def save_related(self, request, form, formsets, change):
		super().save_related(request, form, formsets, change)
		if not (change and request.user.is_superuser):
			obj = form.instance
			obj.owners.add(request.user)
			obj.save()

	@classmethod
	def availableNames(self, request):
		if request.user.is_superuser:
			return RecordName.objects.all()
		return RecordName.objects.filter(owners__id__exact=request.user.id)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):

	def get_readonly_fields(self, request, obj=None):
		if obj is None:
			return []
		else:
			return ["name"]

	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		if db_field.name == "name":
			kwargs["queryset"] = RecordNameAdmin.availableNames(request)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)


	def get_queryset(self, request):
		if request.user.is_superuser:
			return Record.objects.all()
		return Record.objects.filter(name__owners__id__exact=request.user.id)
