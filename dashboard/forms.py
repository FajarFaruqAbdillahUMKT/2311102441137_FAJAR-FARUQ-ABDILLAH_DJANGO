from django import forms
from .models import Mahasiswa


from django.contrib.auth import get_user_model


class MahasiswaForm(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = [
            'nim',
            'nama',
            # 'prodi',
            # 'email',
        ]


class CustomUserCreationForm(forms.Form):
    user_email = forms.EmailField(label='Email', max_length=254, required=True)
    user_password = forms.CharField(label='Kata Sandi', widget=forms.PasswordInput)
    user_password_confirm = forms.CharField(label='Konfirmasi Kata Sandi', widget=forms.PasswordInput)
    username = forms.CharField(label='Username', max_length=150, required=True)
    check = forms.BooleanField(label='Saya setuju dengan Syarat & Ketentuan', required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('user_password')
        password_confirm = cleaned_data.get('user_password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Kata sandi tidak cocok.")
        return cleaned_data

    def clean_user_email(self):
        email = self.cleaned_data.get('user_email')
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email ini sudah terdaftar.")
        return email

    def save(self):
        User = get_user_model()
        user = User.objects.create_user(
            email=self.cleaned_data['user_email'],
            username=self.cleaned_data['username'],
            password=self.cleaned_data['user_password']
        )
        return user