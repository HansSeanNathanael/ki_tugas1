from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.Info().invoke),
    path('file/', views.File().invoke)
]