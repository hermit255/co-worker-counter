from django.urls import path
from chatwork import views

urlpatterns = [
    path('show', views.show),
]
