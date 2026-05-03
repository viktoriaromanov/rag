from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Book, Reader, Reservation, Genre
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class BookModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Тестовый жанр")
        self.book = Book.objects.create(
            title="Тестовая книга",
            author="Тестовый автор",
            isbn="1234567890",
            genre=self.genre
        )
    
    def test_book_creation(self):
        self.assertEqual(self.book.title, "Тестовая книга")
        self.assertTrue(self.book.is_available)
    
    def test_str_method(self):
        self.assertEqual(str(self.book), "Тестовая книга — Тестовый автор")

class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.reader = Reader.objects.create(user=self.user)
        self.book = Book.objects.create(title="Test Book", author="Test Author")
    
    def test_reservation_creation(self):
        reservation = Reservation.objects.create(
            book=self.book,
            reader=self.reader,
            status='active'
        )
        self.assertEqual(reservation.status, 'active')
        self.assertIsNotNone(reservation.due_date)
    
    def test_max_reservations_logic(self):
        # Создаём 3 брони
        for i in range(3):
            Reservation.objects.create(
                book=Book.objects.create(title=f"Book {i}", author="Author"),
                reader=self.reader,
                status='active'
            )
        self.assertEqual(self.reader.active_reservations_count(), 3)

class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(title="Test", author="Author", is_available=True)
    
    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")
    
    def test_reservation_requires_login(self):
        response = self.client.post(reverse('book_detail', kwargs={'pk': self.book.pk}))
        self.assertRedirects(response, f'/accounts/login/?next=/books/{self.book.pk}/')