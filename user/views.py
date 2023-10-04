from django.shortcuts import render
from django.http.request import HttpRequest

from ki_tugas1.views import Views
from .forms.form_info_get import FormInfoGet
from .forms.form_info_post import FormInfoPost
from ki_tugas1.commands.encryption_key import get_key

# Create your views here.

class Info(Views):
    
    def get(self, request : HttpRequest, *args, **kwargs):
        pass
    
    def post(self, request : HttpRequest, *args, **kwargs):
        form = FormInfoPost(request.POST)
        
        if form.is_valid:
            key = form.cleaned_data['key']
            nama = form.cleaned_data['nama']
            email = form.cleaned_data['email']
            tanggal_lahir = form.cleaned_data['tanggal_lahir']
            alamat = form.cleaned_data['alamat']
            nomor_telepon = form.cleaned_data['nomor_telepon']
            
            