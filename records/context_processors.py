from mddns import settings

def admin_context(request):
	return {'ADMIN_NAME': settings.ADMIN_NAME}
