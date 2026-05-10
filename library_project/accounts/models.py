from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="profile",
        verbose_name="Пользователь"
    )
    phone = models.CharField("Телефон", max_length=20, blank=True)
    address = models.TextField("Адрес", blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    bio = models.TextField("О себе", blank=True)
    avatar = models.ImageField(
        "Аватар", 
        upload_to="avatars/", 
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)
    
    def __str__(self):
        return f"Профиль пользователя {self.user.username}"
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

# Автоматическое создание профиля при регистрации
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)