from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Ohai. I've got no API.")
