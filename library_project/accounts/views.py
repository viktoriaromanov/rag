from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

def signup(request):
    """Регистрация нового пользователя"""
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("catalog:book_list")
    else:
        form = SignUpForm()
    
    return render(request, "catalog/registration/signup.html", {"form": form})


@login_required
def profile_view(request):
    """Просмотр профиля текущего пользователя"""
    profile, _ = Profile.objects.get_or_create(user=request.user)
    context = {
        "profile": profile,
    }
    return render(request, "accounts/profile.html", context)

@login_required
def profile_edit(request):
    """Редактирование профиля"""
    profile, _ = Profile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=profile
        )
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("accounts:profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    
    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request, "accounts/profile_edit.html", context)