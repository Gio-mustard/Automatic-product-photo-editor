from django.urls import path
from . import views

urlpatterns = [
    path('make/stack/',views.make_stack,name='make-stack'),
]
