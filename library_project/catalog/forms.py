from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Reservation, Reader

User = get_user_model()

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'genre', 'summary', 'is_available', 'tags']  
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'slug' in self.fields:
            self.fields['slug'].required = False
            self.fields['slug'].widget.attrs['readonly'] = True  

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["notes"]  

class ReaderProfileForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ["phone", "address", "birth_date"]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")