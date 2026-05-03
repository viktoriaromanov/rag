from django.contrib import admin
from .models import Book, Reservation

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "genre", "is_available", "added_at")
    list_filter = ("is_available", "genre", "added_at")
    search_fields = ("title", "author", "isbn")

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("author", "book", "created_at")  # ← Уберите reader_name!
    list_filter = ("created_at",)
    search_fields = ("author__username", "text")