import time

from django.conf import settings
from django.test import TestCase, Client

from autentikasi.models import User

default_location_folder = './user/public/files/'

# Create your tests here.
class TestInformasi(TestCase):
    def setUp(self) -> None:
        client = Client()
        response = client.post("/auth/register/", data={
            "username" : "percobaan",
            "password" : "percobaan"
        })
        
        self.assertEqual(response.status_code, 302)
        
        self.data = {
            "key" : settings.PUBLIC_KEY,
            "nama" : "nama percobaan",
            "email" : "percobaan@mail.com",
            "tanggal_lahir" : "2023-10-16",
            "alamat" : "alamat percobaan",
            "nomor_telepon" : "081234341212"
        }
    
    def tearDown(self) -> None:
        User.objects.filter(username="percobaan").first().delete()
    
    def test_aes_cbc(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(200):
            data = self.data
            data["enkripsi"] = "aes-cbc"
            
            client.post("/info/user/", data=data)
            response = client.get("/info/user/", data={
                "enkripsi" : "aes-cbc",
                "key" : settings.PUBLIC_KEY
            })
            
            for value in self.data.values():
                halaman : str = response.content.decode()
                if not halaman.find(value):
                    self.assertEqual(True, False)
        waktu_selesai = time.time_ns()
        
        print("Total waktu aes cbc: " + str(waktu_selesai-waktu_mulai) + " ns")
    
    def test_aes_cfb(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(200):
            data = self.data
            data["enkripsi"] = "aes-cfb"
            
            client.post("/info/user/", data=data)
            response = client.get("/info/user/", data={
                "enkripsi" : "aes-cfb",
                "key" : settings.PUBLIC_KEY
            })
            
            for value in self.data.values():
                halaman : str = response.content.decode()
                if not halaman.find(value):
                    self.assertEqual(True, False)
        waktu_selesai = time.time_ns()
        
        print("Total waktu aes cfb: " + str(waktu_selesai-waktu_mulai) + " ns")
    
    def test_aes_ofb(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(200):
            data = self.data
            data["enkripsi"] = "aes-ofb"
            
            client.post("/info/user/", data=data)
            response = client.get("/info/user/", data={
                "enkripsi" : "aes-ofb",
                "key" : settings.PUBLIC_KEY
            })
            
            for value in self.data.values():
                halaman : str = response.content.decode()
                if not halaman.find(value):
                    self.assertEqual(True, False)
        waktu_selesai = time.time_ns()
        
        print("Total waktu aes ofb: " + str(waktu_selesai-waktu_mulai) + " ns")
    
    def test_aes_ctr(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(200):
            data = self.data
            data["enkripsi"] = "aes-ctr"
            
            client.post("/info/user/", data=data)
            response = client.get("/info/user/", data={
                "enkripsi" : "aes-ctr",
                "key" : settings.PUBLIC_KEY
            })
            
            for value in self.data.values():
                halaman : str = response.content.decode()
                if not halaman.find(value):
                    self.assertEqual(True, False)
        waktu_selesai = time.time_ns()
        
        print("Total waktu aes ctr: " + str(waktu_selesai-waktu_mulai) + " ns")
    
    def test_des_cbc(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(200):
            data = self.data
            data["enkripsi"] = "des-cbc"
            
            client.post("/info/user/", data=data)
            response = client.get("/info/user/", data={
                "enkripsi" : "des-cbc",
                "key" : settings.PUBLIC_KEY
            })
            
            for value in self.data.values():
                halaman : str = response.content.decode()
                if not halaman.find(value):
                    self.assertEqual(True, False)
        waktu_selesai = time.time_ns()
        
        print("Total waktu des cbc: " + str(waktu_selesai-waktu_mulai) + " ns")
    
    def test_des_cfb(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(200):
            data = self.data
            data["enkripsi"] = "des-cfb"
            
            client.post("/info/user/", data=data)
            response = client.get("/info/user/", data={
                "enkripsi" : "des-cfb",
                "key" : settings.PUBLIC_KEY
            })
            
            for value in self.data.values():
                halaman : str = response.content.decode()
                if not halaman.find(value):
                    self.assertEqual(True, False)
        waktu_selesai = time.time_ns()
        
        print("Total waktu des cfb: " + str(waktu_selesai-waktu_mulai) + " ns")
    
    def test_des_ofb(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(200):
            data = self.data
            data["enkripsi"] = "des-ofb"
            
            client.post("/info/user/", data=data)
            response = client.get("/info/user/", data={
                "enkripsi" : "des-ofb",
                "key" : settings.PUBLIC_KEY
            })
            
            for value in self.data.values():
                halaman : str = response.content.decode()
                if not halaman.find(value):
                    self.assertEqual(True, False)
        waktu_selesai = time.time_ns()
        
        print("Total waktu des ofb: " + str(waktu_selesai-waktu_mulai) + " ns")
    
    def test_des_ctr(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(200):
            data = self.data
            data["enkripsi"] = "des-ctr"
            
            client.post("/info/user/", data=data)
            response = client.get("/info/user/", data={
                "enkripsi" : "des-ctr",
                "key" : settings.PUBLIC_KEY
            })
            
            for value in self.data.values():
                halaman : str = response.content.decode()
                if not halaman.find(value):
                    self.assertEqual(True, False)
        waktu_selesai = time.time_ns()
        
        print("Total waktu des ctr: " + str(waktu_selesai-waktu_mulai) + " ns")
        
    def test_rc4(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(200):
            data = self.data
            data["enkripsi"] = "rc4"
            
            client.post("/info/user/", data=data)
            response = client.get("/info/user/", data={
                "enkripsi" : "rc4",
                "key" : settings.PUBLIC_KEY
            })
            
            for value in self.data.values():
                halaman : str = response.content.decode()
                if not halaman.find(value):
                    self.assertEqual(True, False)
        waktu_selesai = time.time_ns()
        
        print("Total waktu rc4: " + str(waktu_selesai-waktu_mulai) + " ns")
        
        
class TestFile(TestCase):
    def setUp(self) -> None:
        client = Client()
        response = client.post("/auth/register/", data={
            "username" : "percobaan",
            "password" : "percobaan"
        })
        
        self.assertEqual(response.status_code, 302)
        
        self.data = {
            "key" : settings.PUBLIC_KEY,
            "upload_file" : open(default_location_folder + "BBS Example.xlsx", "rb")
        }
    
    def tearDown(self) -> None:
        User.objects.filter(username="percobaan").first().delete()
    
    def test_aes_cbc(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(10):
            data = self.data
            data["enkripsi"] = "aes-cbc"
            
            client.post("/info/file/", data=data)
        waktu_selesai = time.time_ns()
        
        print("Total waktu FILE aes cbc: " + str(waktu_selesai-waktu_mulai) + " ns")
    
    def test_aes_cfb(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(10):
            data = self.data
            data["enkripsi"] = "aes-cfb"
            
            client.post("/info/file/", data=data)
        waktu_selesai = time.time_ns()
        
        print("Total waktu FILE aes cfb: " + str(waktu_selesai-waktu_mulai) + " ns")
    
    def test_aes_ofb(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(10):
            data = self.data
            data["enkripsi"] = "aes-ofb"
            
            client.post("/info/file/", data=data)
        waktu_selesai = time.time_ns()
        
        print("Total waktu FILE aes ofb: " + str(waktu_selesai-waktu_mulai) + " ns")
    
    def test_aes_ctr(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(10):
            data = self.data
            data["enkripsi"] = "aes-ctr"
            
            client.post("/info/file/", data=data)
        waktu_selesai = time.time_ns()
        
        print("Total waktu FILE aes ctr: " + str(waktu_selesai-waktu_mulai) + " ns")
    
    def test_des_cbc(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(10):
            data = self.data
            data["enkripsi"] = "des-cbc"
            
            client.post("/info/file/", data=data)
        waktu_selesai = time.time_ns()
        
        print("Total waktu FILE des cbc: " + str(waktu_selesai-waktu_mulai) + " ns")
    
    def test_des_cfb(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(10):
            data = self.data
            data["enkripsi"] = "des-cfb"
            
            client.post("/info/file/", data=data)
        waktu_selesai = time.time_ns()
        
        print("Total waktu FILE des cfb: " + str(waktu_selesai-waktu_mulai) + " ns")
    
    def test_des_ofb(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(10):
            data = self.data
            data["enkripsi"] = "des-ofb"
            
            client.post("/info/file/", data=data)
        waktu_selesai = time.time_ns()
        
        print("Total waktu FILE des ofb: " + str(waktu_selesai-waktu_mulai) + " ns")
    
    def test_des_ctr(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(10):
            data = self.data
            data["enkripsi"] = "des-ctr"
            
            client.post("/info/file/", data=data)
        waktu_selesai = time.time_ns()
        
        print("Total waktu FILE des ctr: " + str(waktu_selesai-waktu_mulai) + " ns")
        
    def test_rc4(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')
        
        waktu_mulai = time.time_ns()
        for _ in range(10):
            data = self.data
            data["enkripsi"] = "rc4"
            
            client.post("/info/file/", data=data)
        waktu_selesai = time.time_ns()
        
        print("Total waktu FILE rc4: " + str(waktu_selesai-waktu_mulai) + " ns")