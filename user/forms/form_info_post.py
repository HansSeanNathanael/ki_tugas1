from django import forms
from django.core.validators import RegexValidator

class FormInfoPost(forms.Form):
    key = forms.CharField(
        min_length=8, max_length=64, required=True, 
        error_messages={
            'min_length' : 'Minimum 8 huruf',
            'max_length' : 'Maksimum 32 huruf',
            'required' : 'Key kosong'
        }
    )
    
    nama = forms.CharField(
        max_length=64, required=True, 
        error_messages={
            'max_length' : 'Maksimum 32 huruf',
            'required' : 'Nama kosong'
        }
    )
    
    email = forms.EmailField(
        max_length=64, required=True, 
        error_messages={
            'max_length' : 'Maksimum 254 huruf',
            'required' : 'Email kosong'
        }
    )
    
    tanggal_lahir = forms.DateField(
        required=True, 
        error_messages={
            'required' : 'Tanggal lahir kosong'
        }
    )
    
    alamat = forms.CharField(
        max_length=255, required=True, 
        error_messages={
            'max_length' : 'Maksimum 255 huruf',
            'required' : 'Alamat kosong'
        }
    )
    
    nomor_telepon = forms.CharField(
        max_length=255, required=True,
        validators=[
            RegexValidator(
                regex=r'^\+?62?\d{9,15}$',
                message="Nomor telepon harus dalam format +62812xxxx atau 0812xxxx."
            )
        ],
        error_messages={
            'max_length' : 'Maksimum 255 huruf',
            'required' : 'Alamat kosong'
        }
    )