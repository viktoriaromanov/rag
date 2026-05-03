from django.shortcuts import render,redirect, get_object_or_404
from .models import Book
from .forms import BookForm
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import ReservationForm
from .models import Reservation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("book_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

def home(request): 
    return render(request, 'catalog/home.html')
def book_list(request):
    query = request.GET.get("q", "").strip()
    books_qs = Book.objects.filter(is_available=True)

    if query:
        books_qs = books_qs.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(summary__icontains=query)
        )

    paginator = Paginator(books_qs, 5)  # 5 книг на страницу
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "books": page_obj,
        "page_obj": page_obj,
        "query": query,
    }
    return render(request, "catalog/book_list.html", context)
def about(request): 
    return render(request, 'catalog/about.html')
@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, is_available=True)
    reservations = book.reservations.all().order_by("-created_at")

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.book = book
            reservation.author = request.user 
            reservation.save()
            return redirect("book_detail", pk=book.pk)
    else:
        form = ReservationForm()

    context = {
        "book": book,
        "reservations": reservations,
        "form": form,
    }
    return render(request, "catalog/book_detail.html", context)

@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect("book_detail", pk=book.pk)
    else:
        form = BookForm()
    return render(request, "catalog/book_form.html", {"form": form})


@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_detail", pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, "catalog/book_form.html", {"form": form, "is_edit": True, "book": book})

@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "catalog/book_confirm_delete.html", {"book": book})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("book_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})