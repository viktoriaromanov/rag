from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager

class Book(models.Model):
    title = models.CharField("Название", max_length=200)
    slug = models.SlugField(
        max_length=200, 
        unique=True, 
        blank=True,
        null=True  # Важно для существующих книг
    )
    author = models.CharField("Автор", max_length=150)
    isbn = models.CharField("ISBN", max_length=17, unique=True, blank=True, null=True)
    genre = models.ForeignKey("Genre", on_delete=models.SET_NULL, null=True, verbose_name="Жанр", related_name="books")
    is_available = models.BooleanField("Доступна", default=True)
    summary = models.TextField("Описание", blank=True)
    added_at = models.DateTimeField("Добавлено", auto_now_add=True)
    
    tags = TaggableManager(blank=True, verbose_name="Теги")

    def save(self, *args, **kwargs):
        # Генерируем slug ТОЛЬКО если его нет
        if not self.slug:
            # Создаём базовый slug из названия (только латиница)
            base_slug = slugify(self.title, allow_unicode=False)
            
            #  Если slugify вернул пустую строку (кириллица), создаём запасной вариант
            if not base_slug:
                # Если книга уже имеет ID (сохранена), используем его
                if self.pk:
                    base_slug = f"book-{self.pk}"
                else:
                    # Если книга новая, используем хеш от названия как временный идентификатор
                    import hashlib
                    base_slug = f"book-{hashlib.md5(self.title.encode('utf-8')).hexdigest()[:8]}"
            
            # Проверяем уникальность и добавляем суффикс при необходимости
            slug = base_slug
            counter = 1
            while Book.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Присваиваем итоговый slug
            self.slug = slug
        
        # Вызываем оригинальный save() для сохранения в БД
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:book_detail', kwargs={'slug': self.slug})
        
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-added_at"]

class Genre(models.Model):
    name = models.CharField("Название жанра", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        
class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="reader_profile")
    phone = models.CharField("Телефон", max_length=20, blank=True)
    address = models.TextField("Адрес", blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    registration_date = models.DateField("Дата регистрации", auto_now_add=True)
    is_active_reader = models.BooleanField("Активный читатель", default=True)

    def active_reservations_count(self):
        return self.reservations.filter(status__in=['active', 'pending']).count()

    def overdue_reservations(self):
        return self.reservations.filter(
            status='active',
            due_date__lt=timezone.now().date()
        )

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('active', 'Активна'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
        ('overdue', 'Просрочена'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reservations", verbose_name="Книга")
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name="reservations", verbose_name="Читатель", null=True,blank=True)
    reservation_date = models.DateTimeField("Дата бронирования", auto_now_add=True)
    start_date = models.DateField("Дата выдачи", null=True, blank=True)
    due_date = models.DateField("Дата возврата", null=True, blank=True)
    return_date = models.DateField("Фактический возврат", null=True, blank=True)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField("Заметки", blank=True)

    def save(self, *args, **kwargs):
        if self.start_date and not self.due_date:
            self.due_date = self.start_date + timedelta(days=14)
        if self.status == 'active' and self.due_date and self.due_date < timezone.now().date():
            self.status = 'overdue'
        super().save(*args, **kwargs)

    def calculate_fine(self):
        if self.return_date and self.return_date > self.due_date:
            days_overdue = (self.return_date - self.due_date).days
            return days_overdue * 10
        return 0

    def __str__(self):
        return f"Бронь #{self.id} - {self.book.title} ({self.reader})"

    class Meta:
        ordering = ['-reservation_date']
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

class Fine(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="fines", verbose_name="Бронирование")
    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    is_paid = models.BooleanField("Оплачен", default=False)
    paid_at = models.DateTimeField("Дата оплаты", null=True, blank=True)

    def mark_as_paid(self):
        self.is_paid = True
        self.paid_at = timezone.now()
        self.save()

    class Meta:
        verbose_name = "Штраф"
        verbose_name_plural = "Штрафы"