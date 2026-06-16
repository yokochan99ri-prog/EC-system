from django import forms
from .models import AccountUser

class UserForm(forms.Form):

    id = forms.CharField(label='ユーザーID', max_length=128)
    password = forms.CharField(label='パスワード', max_length=256, widget=forms.PasswordInput(render_value=False))

class UserCreateForm(forms.Form):
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    user_id = forms.CharField(label="会員ID", max_length=128)
    password = forms.CharField(label="パスワード", max_length=256, widget=forms.PasswordInput(render_value=False))
    password_check = forms.CharField(label="パスワード(確認)", max_length=256)
    name = forms.CharField(label="お名前", max_length=256)
    address = forms.CharField(label="ご住所", max_length=256)

    def clean_user_id(self):
        value = self.cleaned_data["user_id"]
        if AccountUser.objects.filter(user_id=value).exists():
            raise forms.ValidationError("このIDは使用されています")
        return value
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')
        if password != password_check:
            raise forms.ValidationError('パスワードが一致しません')
        return cleaned_data


class UserUpdateForm(forms.ModelForm):

    password = forms.CharField(label="パスワード", max_length=256, widget=forms.PasswordInput(render_value=False), required=False)
    password_check = forms.CharField(label="パスワード(確認)", max_length=256, widget=forms.PasswordInput(render_value=False), required=False)

    class Meta:
        model = AccountUser
        fields = ['user_id', 'name', 'address']

    def clean_user_id(self):
        value = self.cleaned_data["user_id"]
        queryset = AccountUser.objects.filter(user_id=value)

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError("このIDは使用されています")

        return value
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')

        if password or password_check:
            if password != password_check:
                raise forms.ValidationError('パスワードが一致しません')

        return cleaned_data