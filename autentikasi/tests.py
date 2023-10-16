from django.test import TestCase, Client

from .models import User

# Create your tests here.
class TestAutentikasi(TestCase):
    
    def setUp(self) -> None:
        self.user : User|None = None
        
    def tearDown(self) -> None:
        if self.user is not None:
            self.user.delete()
    
    def test_register(self) -> None:
        client = Client()
        response = client.post("/auth/register/", data={
            "username" : "percobaan",
            "password" : "percobaan"
        })
        self.assertEqual(response.status_code, 302)
        self.user = User.objects.filter(username="percobaan").first()
    
    
    def test_login(self) -> None:
        client = Client()
        client.login(username='percobaan', password='percobaan')