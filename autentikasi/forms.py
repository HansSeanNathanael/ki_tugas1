from django import forms

class FormLogin(forms.Form):
    username = forms.CharField(
        min_length=8, max_length=32, required=True, 
        error_messages={
            'min_length' : 'Minimum 8 huruf',
            'max_length' : 'Maksimum 32 huruf',
            'required' : 'Username kosong'
        }
    )
    
    password = forms.CharField(
        min_length=8, max_length=32, required=True, 
        error_messages={
            'min_length' : 'Minimum 8 huruf',
            'max_length' : 'Maksimum 32 huruf',
            'required' : 'Password kosong'
        }
    )
    
class FormRegister(forms.Form):
    username = forms.CharField(
        min_length=8, max_length=32, required=True, 
        error_messages={
            'min_length' : 'Minimum 8 huruf',
            'max_length' : 'Maksimum 32 huruf',
            'required' : 'Username kosong'
        }
    )
    
    password = forms.CharField(
        min_length=8, max_length=32, required=True, 
        error_messages={
            'min_length' : 'Minimum 8 huruf',
            'max_length' : 'Maksimum 32 huruf',
            'required' : 'Password kosong'
        }
    )