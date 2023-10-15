import base64, uuid

from django.conf import settings
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect, HttpResponse
from Crypto.Cipher import AES as AESCHIPHER, DES as DESCIPHER

from autentikasi.models import User
from ki_tugas1.views import Views
from ki_tugas1.encryptor.aes import AES, DES, RC4, StringBlock, StringDecryptBlock
from ki_tugas1.commands.encryption_key import get_key
from .models import File as FileModel, InformasiPribadi
from .forms.form_info_get import FormInfoGet
from .forms.form_info_post import FormInfoPost
from ki_tugas1.commands.encryption_key import get_key

# Create your views here.

default_location_folder = './user/public/files/'

def encryptAES(key : bytes, data : bytes, mode : any) -> bytes:
    aes = AES(key, mode)
    
    data_block = None
    if mode == AESCHIPHER.MODE_CTR:
        data_block = StringBlock(data, None)
    else:
        data_block = StringBlock(data, 16)
    
    return aes.encrypt(data_block)
    
def decryptAES(key : bytes, data : bytes, mode : any) -> bytes:
    aes = AES(key, mode)
    data_block = None
    if mode == AESCHIPHER.MODE_CTR:
        data_block = StringDecryptBlock(data, None)
    else:
        data_block = StringDecryptBlock(data, 16)
        
    result = bytes()
    while True:
        data = aes.decrypt(data_block)
        if data is None:
            break
        
        result += data
    return result

def encryptDES(key : bytes, data : bytes, mode : any) -> bytes:
    des = DES(key, mode)
    data_block = None
    if mode == DESCIPHER.MODE_CTR:
        data_block = StringBlock(data, None)
    else:
        data_block = StringBlock(data, 8)
    
    return des.encrypt(data_block)

def decryptDES(key : bytes, data : bytes, mode : any) -> bytes:
    des = DES(key, mode)
    data_block = None
    if mode == DESCIPHER.MODE_CTR:
        data_block = StringDecryptBlock(data, None)
    else:
        data_block = StringDecryptBlock(data, 8)
        
    result = bytes()
    while True:
        data = des.decrypt(data_block)
        if data is None:
            break
        result += data
    return result

def encryptRC4(key : bytes, data : bytes) -> bytes:
    rc4 = RC4(key)
    return rc4.encrypt(data)

def decryptRC4(key : bytes, data : bytes) -> bytes:
    rc4 = RC4(key)
    return rc4.decrypt(data)

def encrypt(algoritma : str, key : str, data : bytes) -> bytes:
    tipe_enkripsi = algoritma[:3]
    if tipe_enkripsi == "aes":
        mode = algoritma[4:]
        if mode == "cbc":
            return encryptAES(get_key(key.encode(), 16), data, AESCHIPHER.MODE_CBC)
        elif mode == "cfb":
            return encryptAES(get_key(key.encode(), 16), data, AESCHIPHER.MODE_CFB)
        elif mode == "ofb":
            return encryptAES(get_key(key.encode(), 16), data, AESCHIPHER.MODE_OFB)
        elif mode == "ctr":
            return encryptAES(get_key(key.encode(), 16), data, AESCHIPHER.MODE_CTR)
    elif tipe_enkripsi == "des":
        mode = algoritma[4:]
        if mode == "cbc":
            return encryptDES(get_key(key.encode(), 8), data, DESCIPHER.MODE_CBC)
        elif mode == "cfb":
            return encryptDES(get_key(key.encode(), 8), data, DESCIPHER.MODE_CFB)
        elif mode == "ofb":
            return encryptDES(get_key(key.encode(), 8), data, DESCIPHER.MODE_OFB)
        elif mode == "ctr":
            return encryptDES(get_key(key.encode(), 8), data, DESCIPHER.MODE_CTR)
    elif tipe_enkripsi == "rc4":
        return encryptRC4(get_key(key.encode(), 16), data)
    return bytes()

def decrypt(algoritma : str, key : str, data : bytes) -> bytes:
    tipe_enkripsi = algoritma[:3]
    if tipe_enkripsi == "aes":
        mode = algoritma[4:]
        if mode == "cbc":
            return decryptAES(get_key(key.encode(), 16), data, AESCHIPHER.MODE_CBC)
        elif mode == "cfb":
            return decryptAES(get_key(key.encode(), 16), data, AESCHIPHER.MODE_CFB)
        elif mode == "ofb":
            return decryptAES(get_key(key.encode(), 16), data, AESCHIPHER.MODE_OFB)
        elif mode == "ctr":
            print(decryptAES(get_key(key.encode(), 16), data, AESCHIPHER.MODE_CTR))
            return decryptAES(get_key(key.encode(), 16), data, AESCHIPHER.MODE_CTR)
    elif tipe_enkripsi == "des":
        mode = algoritma[4:]
        if mode == "cbc":
            return decryptDES(get_key(key.encode(), 8), data, DESCIPHER.MODE_CBC)
        elif mode == "cfb":
            return decryptDES(get_key(key.encode(), 8), data, DESCIPHER.MODE_CFB)
        elif mode == "ofb":
            return decryptDES(get_key(key.encode(), 8), data, DESCIPHER.MODE_OFB)
        elif mode == "ctr":
            return decryptDES(get_key(key.encode(), 8), data, DESCIPHER.MODE_CTR)
    elif tipe_enkripsi == "rc4":
        return decryptRC4(get_key(key.encode(), 16), data)
    return bytes()

class Info(Views):
    
    def get(self, request : HttpRequest, *args, **kwargs):
        form = FormInfoGet(request.GET)
        user : User = request.user
        
        if form.is_valid():
            key = form.cleaned_data['key']
            enkripsi = request.GET.get('enkripsi')
            
            try:
                nama_dekripsi : str = decrypt(enkripsi, key, base64.b64decode(user.nama.encode())).decode()
                email_dekripsi : str = decrypt(enkripsi, key, base64.b64decode(user.email.encode())).decode()
                tanggal_lahir_dekripsi : str = decrypt(enkripsi, key, base64.b64decode(user.tanggal_lahir.encode())).decode()
                alamat_dekripsi : str = decrypt(enkripsi, key, base64.b64decode(user.alamat.encode())).decode()
                nomor_telepon_dekripsi : str = decrypt(enkripsi, key, base64.b64decode(user.nomor_telepon.encode())).decode()
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
            enkripsi = request.POST.get('enkripsi')
            
            nama_enkripsi : bytes = encrypt(enkripsi, key, nama.encode())
            email_enkripsi : bytes = encrypt(enkripsi, key, email.encode())
            tanggal_lahir_enkripsi : bytes = encrypt(enkripsi, key, tanggal_lahir.strftime('%Y/%m/%d').encode())
            alamat_enkripsi : bytes = encrypt(enkripsi, key, alamat.encode())
            nomor_telepon_enkripsi : bytes = encrypt(enkripsi, key, nomor_telepon.encode())
            
            
            user : User = request.user
            user.nama = base64.b64encode(nama_enkripsi).decode()
            user.email = base64.b64encode(email_enkripsi).decode()
            user.tanggal_lahir = base64.b64encode(tanggal_lahir_enkripsi).decode()
            user.alamat = base64.b64encode(alamat_enkripsi).decode()
            user.nomor_telepon = base64.b64encode(nomor_telepon_enkripsi).decode()
            user.save()
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class DataPribadi(Views):
    
    def get(self, request : HttpRequest, *args, **kwargs):
        id = request.GET.get('id')
        key = request.GET.get('key')
        enkripsi = request.GET.get('enkripsi')
            
        user : User = request.user
        
        daftar_informasi_pribadi = InformasiPribadi.objects.filter(id_user=user.id)
        daftar_data_pribadi = []
        for informasi in daftar_informasi_pribadi:
            data_informasi = {
                'id' : informasi.id,
                'nama_informasi' : decryptRC4(get_key(settings.PUBLIC_KEY.encode(), 32), base64.b64decode(informasi.nama_informasi.encode())).decode()
            }
            
            data = "<Encrypted>"
            if id is not None and id == str(informasi.id):
                try:
                    data = decrypt(enkripsi, key, base64.b64decode(informasi.isi_informasi.encode())).decode()
                except:
                    pass
            data_informasi['isi_informasi'] = data
            daftar_data_pribadi.append(data_informasi)
        
        return render(request, 'data_pribadi\index.html', context={
            'daftar_data_pribadi' : daftar_data_pribadi
        })
        
    
    def post(self, request : HttpRequest, *args, **kwargs):
        key = request.POST.get('key')
        nama_informasi = request.POST.get('nama_informasi')
        isi_informasi = request.POST.get('isi_informasi')
        enkripsi = request.POST.get('enkripsi')
        user : User = request.user
        
        id = uuid.uuid4()
        nama_informasi_enkripsi = base64.b64encode(encryptRC4(get_key(settings.PUBLIC_KEY.encode(), 32), nama_informasi.encode())).decode()
        isi_informasi_enkripsi = base64.b64encode(encrypt(enkripsi, key, isi_informasi.encode())).decode()
        InformasiPribadi.objects.create(
            id = id,
            id_user = user,
            nama_informasi = nama_informasi_enkripsi,
            isi_informasi = isi_informasi_enkripsi
        )
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    
class File(Views):
    
    def get(self, request : HttpRequest, *args, **kwargs):
        user : User = request.user
        daftar_file = FileModel.objects.filter(id_user=user.id)
        
        kumpulan_file = []
        for fi in daftar_file:
            kumpulan_file.append({
                'nama_file' : decryptDES(get_key(settings.PUBLIC_KEY.encode(), 8), base64.b64decode(fi.nama_file.encode()), DESCIPHER.MODE_CBC).decode(),
                'id_file' : fi.id
            })
            
        return render(request, 'file\index.html', context={
            'daftar_file' : kumpulan_file
        })
        
    def post(self, request : HttpRequest, *args, **kwargs):
        user : User = request.user
        key = request.POST['key']
        enkripsi = request.POST['enkripsi']
        uploaded_file = request.FILES['upload_file']
        
        id = uuid.uuid4()
        nama_file = base64.b64encode(encryptDES(get_key(settings.PUBLIC_KEY.encode(), 8), uploaded_file.name.encode(), DESCIPHER.MODE_CBC)).decode()
        nama_file_fisik = uuid.uuid4()
        FileModel.objects.create(id=id, id_user=user, nama_file=nama_file, nama_file_fisik=nama_file_fisik)

        self.handle_uploaded_file(uploaded_file, nama_file_fisik, enkripsi, key)
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    def handle_uploaded_file(self, fi, name, enkripsi : str, key : str):
        with open(default_location_folder + str(name), "wb+") as destination:
            destination.write(encrypt(enkripsi, key, fi.read()))
                
class Download(Views):
    
    def get(self, request : HttpRequest, *args, **kwargs):
        user : User = request.user
        id = request.GET['id']
        key = request.GET['key']
        enkripsi = request.GET['enkripsi']
        
        fi = FileModel.objects.filter(id=id).get()
        
        result = bytes()
        with open(default_location_folder + str(fi.nama_file_fisik), "rb") as destination:
            result = decrypt(enkripsi, key, destination.read())
            
        return HttpResponse(result, content_type='application/octet-stream')