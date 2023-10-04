from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register().invoke),
    path('login/', views.Login().invoke)
]