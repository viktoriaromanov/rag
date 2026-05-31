from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.utils.text import slugify
from taggit.models import Tag 

from .models import Book, Reservation, Reader, Genre, Event
from .forms import BookForm, ReservationForm, ReaderProfileForm, CustomUserCreationForm

def home(request):
    events = Event.objects.all()[:4] 
    
    context = {
        'events': events,
    }
    return render(request, 'catalog/home.html', context)

def event_detail(request, slug):
    from .models import Event # Импорт модели
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'catalog/event_detail.html', {'event': event})

def about(request):
    return render(request, 'catalog/about.html')

def book_list(request):
    query = request.GET.get("q", "").strip()
    genre_id = request.GET.get("genre", "").strip()

    books_qs = Book.objects.filter(is_available=True).select_related('genre')

    # Фильтр по поиску
    if query:
        books_qs = books_qs.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(summary__icontains=query)
        )

    # Фильтр по жанру
    selected_genre = None
    if genre_id:
        try:
            selected_genre = Genre.objects.get(id=genre_id)
            
            # 1. Берем ID выбранного жанра
            genre_ids = [selected_genre.id]
            
            # 2. Находим все поджанры этого жанра
            subgenres = Genre.objects.filter(parent=selected_genre)
            if subgenres.exists():
                # Добавляем ID поджанров в список
                genre_ids.extend(subgenres.values_list('id', flat=True))
            
            # 3. Фильтруем книги по списку ID (книга должна быть в выбранном жанре ИЛИ в поджанре)
            books_qs = books_qs.filter(genre__id__in=genre_ids)
            
        except Genre.DoesNotExist:
            pass
    
    all_genres = Genre.objects.annotate(
        direct_count=Count('books', filter=Q(books__is_available=True))
    )

    root_genres = []
    
    # Перебираем только корневые жанры (у которых нет родителя)
    for root in all_genres.filter(parent__isnull=True).order_by('name'):
        
        # Находим поджанры этого корня
        children = all_genres.filter(parent=root)
        
        # Считаем общее количество книг (свои + поджанры)
        children_count = sum([c.direct_count for c in children])
        root.total_count = root.direct_count + children_count
        
        # Сохраняем список поджанров, у которых есть книги
        root.visible_children = [c for c in children if c.direct_count > 0]
        
        # Добавляем корень в список, если у него есть книги (в нем или в поджанрах)
        if root.total_count > 0:
            root_genres.append(root)

    # Пагинация
    paginator = Paginator(books_qs, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Жанры для сайдбара (считаем только доступные книги)
        # Жанры для сайдбара
    genres = Genre.objects.annotate(
        available_count=Count('books', filter=Q(books__is_available=True))
    ).filter(available_count__gt=0).order_by('name')

    # Теги (ПРАВИЛЬНОЕ ИМЯ СВЯЗИ!)
    tags = Tag.objects.annotate(
        num_times=Count('taggit_taggeditem_items')
    ).filter(num_times__gt=0).order_by('-num_times')[:10]

    context = {
        "page_obj": page_obj,
        "query": query,
        "root_genres": root_genres,
        #"genres": genres,
        "selected_genre": selected_genre,
        "tags": tags,
    }
    return render(request, "catalog/book_list.html", context)

def books_by_tag(request, tag_slug):
    """Отображение книг с определённым тегом"""
    tag = get_object_or_404(Tag, slug=tag_slug)
    
    books_qs = Book.objects.filter(
        tags__slug=tag_slug,
        is_available=True
    ).select_related('genre')
    
    query = request.GET.get("q", "").strip()
    if query:
        books_qs = books_qs.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(summary__icontains=query)
        )
    
    # Пагинация
    paginator = Paginator(books_qs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "books": page_obj,
        "page_obj": page_obj,
        "query": query,
        "tag": tag,
    }
    return render(request, "catalog/books_by_tag.html", context)


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
@login_required
def reader_profile(request):
    """Личный кабинет читателя"""
    from accounts.models import Profile
    from .models import Reservation, Fine
    from django.db.models import Sum
    
    profile, _ = Profile.objects.get_or_create(user=request.user)
    
    # Получаем читателя
    try:
        reader = request.user.reader_profile
    except:
        reader = None
    
    # Получаем активные брони
    active_reservations = Reservation.objects.filter(
        reader__user=request.user,
        status__in=['active', 'pending']
    ).select_related('book')
    
    # Получаем историю
    history = Reservation.objects.filter(
        reader__user=request.user,
        status__in=['completed', 'cancelled', 'overdue']
    ).select_related('book').order_by('-reservation_date')[:10]
    
    if reader:
        fines = Fine.objects.filter(reservation__reader=reader, is_paid=False)
        total_debt = fines.aggregate(total=Sum('amount'))['total'] or 0
    else:
        fines = Fine.objects.none()
        total_debt = 0
    
    context = {
        'profile': profile,
        'active_reservations': active_reservations,
        'history': history,
        'fines': fines,
        'unpaid_fines': fines,
        'total_debt': total_debt,
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
            return redirect("catalog:book_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})