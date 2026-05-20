from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('about/', views.about, name='about'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('books/<slug:slug>/edit/', views.book_edit, name='book_edit'),
    path('books/<slug:slug>/delete/', views.book_delete, name='book_delete'),
    path('tag/<str:tag_slug>/', views.books_by_tag, name='books_by_tag'),
    path('profile/', views.reader_profile, name='reader_profile'),
    path('accounts/signup/', views.signup, name='signup'),
    path('event/<slug:slug>/', views.event_detail, name='event_detail'),
]