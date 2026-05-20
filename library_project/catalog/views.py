from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.utils.text import slugify

from .models import Book, Reservation, Reader, Genre
from .forms import BookForm, ReservationForm, ReaderProfileForm, CustomUserCreationForm

def home(request):
    return render(request, 'catalog/home.html')

def about(request):
    return render(request, 'catalog/about.html')

def book_list(request):
    query = request.GET.get("q", "").strip()
    books_qs = Book.objects.filter(is_available=True).select_related('genre')

    if query:
        books_qs = books_qs.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(summary__icontains=query)
        )

    paginator = Paginator(books_qs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "books": page_obj,
        "page_obj": page_obj,
        "query": query,
    }
    return render(request, "catalog/book_list.html", context)

def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug, is_available=True)
    reservations = book.reservations.filter(status__in=['active', 'pending']).order_by('-reservation_date')

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request, 'Для бронирования необходимо войти в систему.')
            return redirect('login')

        try:
            reader = request.user.reader_profile
        except Reader.DoesNotExist:
            reader = Reader.objects.create(user=request.user)

        if reader.active_reservations_count() >= 3:
            messages.error(request, 'У вас уже 3 активные брони. Максимум достигнут.')
            return redirect('catalog:book_detail', slug=book.slug)

        existing = reader.reservations.filter(
            book=book,
            status__in=['active', 'pending']
        ).exists()

        if existing:
            messages.warning(request, 'У вас уже есть бронь на эту книгу.')
            return redirect('catalog:book_detail', slug=book.slug)

        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.book = book
            reservation.reader = reader
            reservation.status = 'pending'
            reservation.save()
            messages.success(request, '✓ Заявка на бронирование успешно отправлена!')
            return redirect('catalog:book_detail', slug=book.slug)
    else:
        form = ReservationForm()

    context = {
        "book": book,
        "reservations": reservations,
        "form": form,
    }
    return render(request, "catalog/book_detail.html", context)

@login_required
def reader_profile(request):
    """Личный кабинет читателя"""
    # Получаем профиль текущего пользователя
    from accounts.models import Profile
    profile, _ = Profile.objects.get_or_create(user=request.user)
    
    # Получаем активные брони
    from .models import Reservation
    active_reservations = Reservation.objects.filter(
        reader__user=request.user,
        status__in=['active', 'pending']
    ).select_related('book')
    
    # Получаем историю бронирований
    history = Reservation.objects.filter(
        reader__user=request.user,
        status__in=['completed', 'cancelled', 'overdue']
    ).select_related('book').order_by('-reservation_date')[:10]
    
    context = {
        'profile': profile,
        'active_reservations': active_reservations,
        'history': history,
    }
    return render(request, 'catalog/reader_profile.html', context)

@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            
            if not book.slug:
                base_slug = slugify(book.title, allow_unicode=False)
                
                if not base_slug:
                    book.save()
                    base_slug = f"book-{book.pk}"
                
                slug = base_slug
                counter = 1
                while Book.objects.filter(slug=slug).exclude(pk=book.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                book.slug = slug
            
            book.save()  
            messages.success(request, f'Книга "{book.title}" успешно добавлена!')
            return redirect("catalog:book_detail", slug=book.slug)
    else:
        form = BookForm()
    return render(request, "catalog/book_form.html", {"form": form})

@login_required
def book_edit(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Книга "{book.title}" обновлена!')
            return redirect("catalog:book_detail", slug=book.slug)
    else:
        form = BookForm(instance=book)
    return render(request, "catalog/book_form.html", {"form": form, "is_edit": True, "book": book})

@login_required
def book_delete(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if request.method == "POST":
        title = book.title
        book.delete()
        messages.success(request, f'Книга "{title}" удалена.')
        return redirect("book_list")
    return render(request, "catalog/book_confirm_delete.html", {"book": book})

@login_required
def reader_profile(request):
    reader, created = Reader.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ReaderProfileForm(request.POST, instance=reader)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён!')
            return redirect('reader_profile')
    else:
        form = ReaderProfileForm(instance=reader)

    active_reservations = reader.reservations.filter(status__in=['active', 'pending']).select_related('book')
    history = reader.reservations.filter(status__in=['completed', 'cancelled', 'overdue']).select_related('book').order_by('-reservation_date')[:10]

    context = {
        'reader': reader,
        'form': form,
        'active_reservations': active_reservations,
        'history': history,
    }
    return render(request, 'catalog/reader_profile.html', context)

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Reader.objects.get_or_create(user=user)
            messages.success(request, 'Регистрация успешна! Добро пожаловать.')
            return redirect("book_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})