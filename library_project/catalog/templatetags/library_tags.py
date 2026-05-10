# catalog/templatetags/library_tags.py
from django import template
from ..models import Book

register = template.Library()

@register.simple_tag
def total_books():
    """Возвращает общее количество доступных книг"""
    return Book.objects.filter(is_available=True).count()

@register.inclusion_tag('catalog/latest_books.html')
def show_latest_books(count=3):
    """Возвращает последние N книг"""
    latest_books = Book.objects.filter(is_available=True).order_by('-added_at')[:count]
    return {'latest_books': latest_books}

@register.inclusion_tag('catalog/tag_cloud.html')
def show_tag_cloud():
    """Возвращает популярные теги (пример упрощенный)"""
    # Для django-taggit это сложнее, упростим для учебного проекта:
    # Просто покажем уникальные теги из первых 20 книг
    books = Book.objects.filter(is_available=True).prefetch_related('tags')[:20]
    tags = set()
    for book in books:
        for tag in book.tags.all():
            tags.add(tag)
    return {'tags': list(tags)}