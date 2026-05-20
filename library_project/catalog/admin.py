from django.contrib import admin
from .models import Book, Reservation, Reader, Genre, Fine, Event

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'is_available', 'added_at')
    list_filter = ('is_available', 'genre', 'added_at')
    search_fields = ('title', 'author', 'isbn')
    prepopulated_fields = {'slug': ('title',)} 
    readonly_fields = ('added_at',)

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'registration_date', 'is_active_reader')
    list_filter = ('is_active_reader', 'registration_date')
    search_fields = ('user__username', 'user__email', 'phone')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('book', 'reader', 'status', 'reservation_date', 'due_date')
    list_filter = ('status', 'reservation_date')
    search_fields = ('book__title', 'reader__user__username')
    readonly_fields = ('reservation_date',)

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'amount', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location')
    prepopulated_fields = {'slug': ('title',)}