from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.Info().invoke),
    path('pribadi/', views.DataPribadi().invoke),
    path('file/', views.File().invoke),
    path('download/', views.Download().invoke)
]