from django.db import models
from django.contrib.auth.models import User

# Сначала определяем модель Book
class Book(models.Model):
    title = models.CharField("Название", max_length=200)
    author = models.CharField("Автор", max_length=150)
    isbn = models.CharField("ISBN", max_length=17, unique=True, blank=True, null=True)
    genre = models.CharField("Жанр", max_length=100, default="Не указан")
    is_available = models.BooleanField("Доступна", default=True)
    summary = models.TextField("Описание", blank=True)
    added_at = models.DateTimeField("Добавлено", auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} — {self.author}"

# Потом модель Reservation
class Reservation(models.Model):
    book = models.ForeignKey(
        Book,  # ← Теперь Book уже определена!
        on_delete=models.CASCADE, 
        related_name="reservations",
        verbose_name="Книга"
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Пользователь"
    )
    text = models.TextField("Заметка")
    created_at = models.DateTimeField("Дата заявки", auto_now_add=True)
    
    def __str__(self):
        return f"Бронь от {self.author.username if self.author else 'Аноним'} на {self.book.title}"