from django import forms
from .models import Book, Reservation

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "isbn", "genre", "summary", "is_available"]

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["text"]  