from django.urls import path

from . import views, update

urlpatterns = [
    path('', views.index, name='index'),
    path('update', update.index, name='index'),
]

