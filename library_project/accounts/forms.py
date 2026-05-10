from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile  # ← Импортируем модель из models.py

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="Имя", max_length=30)
    last_name = forms.CharField(required=True, label="Фамилия", max_length=30)
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email")
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

class ProfileUpdateForm(forms.ModelForm):  # ← Правильное имя формы!
    class Meta:
        model = Profile  # ← Используем модель из models.py
        fields = ("phone", "address", "birth_date", "bio", "avatar")
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }