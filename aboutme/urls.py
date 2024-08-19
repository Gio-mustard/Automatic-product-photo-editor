from django.urls import path
from . import views
from project import rutes_constants as rutes
urlpatterns = [
    path("",views.main_page,name=rutes.ABOUT_ME),
]
