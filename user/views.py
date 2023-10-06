import base64

from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from Crypto.Cipher import AES as AESCHIPHER

from autentikasi.models import User
from ki_tugas1.views import Views
from ki_tugas1.encryptor.aes import AES, StringBlock, StringDecryptBlock
from ki_tugas1.commands.encryption_key import get_key
from .models import File as FileModel
from .forms.form_info_get import FormInfoGet
from .forms.form_info_post import FormInfoPost
from ki_tugas1.commands.encryption_key import get_key

# Create your views here.

class Info(Views):
    
    def get(self, request : HttpRequest, *args, **kwargs):
        form = FormInfoGet(request.GET)
        user : User = request.user
        
        if form.is_valid():
            key = form.cleaned_data['key']
            key_hash = get_key(key.encode(), 32)
            
            try:
                nama_dekripsi : str = self.decrypt(key_hash, base64.b64decode(user.nama.encode()), AESCHIPHER.MODE_CBC).decode()
                email_dekripsi : str = self.decrypt(key_hash, base64.b64decode(user.email.encode()), AESCHIPHER.MODE_CBC).decode()
                tanggal_lahir_dekripsi : str = self.decrypt(key_hash, base64.b64decode(user.tanggal_lahir.encode()), AESCHIPHER.MODE_CBC).decode()
                alamat_dekripsi : str = self.decrypt(key_hash, base64.b64decode(user.alamat.encode()), AESCHIPHER.MODE_CBC).decode()
                nomor_telepon_dekripsi : str = self.decrypt(key_hash, base64.b64decode(user.nomor_telepon.encode()), AESCHIPHER.MODE_CBC).decode()
                # string -> bytes -> bytes (encrypt) -> (b64encode) bytes -> string
                
                return render(request, 'info\index.html', context={
                    'username' : user.username,
                    'nama' : nama_dekripsi,
                    'email' : email_dekripsi,
                    'tanggal_lahir' : tanggal_lahir_dekripsi,
                    'alamat' : alamat_dekripsi,
                    'nomor_telepon' : nomor_telepon_dekripsi,
                })
            except Exception as e:
                pass
            
        return render(request, 'info\index.html', context={
            'username' : user.username,
            'nama' : '<Encrypted>',
            'email' : '<Encrypted>',
            'tanggal_lahir' : '<Encrypted>',
            'alamat' : '<Encrypted>',
            'nomor_telepon' : '<Encrypted>',
        })
            
        
            
    
    def post(self, request : HttpRequest, *args, **kwargs):
        form = FormInfoPost(request.POST)
        if form.is_valid():
            key = form.cleaned_data['key']
            nama = form.cleaned_data['nama']
            email = form.cleaned_data['email']
            tanggal_lahir = form.cleaned_data['tanggal_lahir']
            alamat = form.cleaned_data['alamat']
            nomor_telepon = form.cleaned_data['nomor_telepon']
            
            key_hash = get_key(key.encode(), 32)
            nama_enkripsi : bytes = self.encrypt(key_hash, nama, AESCHIPHER.MODE_CBC)
            email_enkripsi : bytes = self.encrypt(key_hash, email, AESCHIPHER.MODE_CBC)
            tanggal_lahir_enkripsi : bytes = self.encrypt(key_hash, tanggal_lahir.strftime('%Y/%m/%d'), AESCHIPHER.MODE_CBC)
            alamat_enkripsi : bytes = self.encrypt(key_hash, alamat, AESCHIPHER.MODE_CBC)
            nomor_telepon_enkripsi : bytes = self.encrypt(key_hash, nomor_telepon, AESCHIPHER.MODE_CBC)
            
            
            user : User = request.user
            user.nama = base64.b64encode(nama_enkripsi).decode()
            user.email = base64.b64encode(email_enkripsi).decode()
            user.tanggal_lahir = base64.b64encode(tanggal_lahir_enkripsi).decode()
            user.alamat = base64.b64encode(alamat_enkripsi).decode()
            user.nomor_telepon = base64.b64encode(nomor_telepon_enkripsi).decode()
            user.save()
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            
            
    def encrypt(self, key : bytes, data : str, mode : any) -> bytes:
        aes = AES(key, mode)
        data_block = StringBlock(data, 16)
        
        return aes.encrypt(data_block)
        
    def decrypt(self, key : bytes, data : bytes, mode : any) -> bytes:
        aes = AES(key, mode)
        data_block = StringDecryptBlock(data, 16)
        result = bytes()
        while True:
            data = aes.decrypt16(data_block)
            if data is None:
                break
            
            result += data
        
        return result
    
class File(Views):
    
    def get(self, request : HttpRequest, *args, **kwargs):
        user : User = request.user
        daftar_file = FileModel.objects.filter(id_user=user.id)
        
        kumpulan_file = []
        for fi in daftar_file:
            kumpulan_file.append({
                'nama_file' : fi.nama_file,
                'id_file' : fi.id
            })
            
        return render(request, 'file\index.html', context={
            'daftar_file' : kumpulan_file
        })
        
    def post(self, request : HttpRequest, *args, **kwargs):
        user : User = request.user
        daftar_file = FileModel.objects.filter(id_user=user.id)
        pass