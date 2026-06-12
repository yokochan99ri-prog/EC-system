from django import forms
from .models import AccountUser

class UserForm(forms.Form):

    id = forms.CharField(label='ユーザーID', max_length=128)
    password = forms.CharField(label='パスワード', max_length=256, widget=forms.PasswordInput(render_value=False))







