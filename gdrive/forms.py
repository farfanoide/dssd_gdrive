from django import forms

class GdriveShareForm(forms.Form):

    user_email = forms.EmailField()
