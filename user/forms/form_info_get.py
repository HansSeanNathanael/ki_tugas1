from django import forms

class FormInfoGet(forms.Form):
    key = forms.CharField(
        min_length=8, max_length=64, required=True, 
        error_messages={
            'min_length' : 'Minimum 8 huruf',
            'max_length' : 'Maksimum 32 huruf',
            'required' : 'Key kosong'
        }
    )