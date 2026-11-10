from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # Validation
        if not username or not email or not password or not confirm_password:
            messages.error(request, "Please fill all required fields.")
            return render(request, "accounts/register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/register.html")

        if len(password) < 6:
            messages.error(request, "Password must contain at least 6 characters.")
            return render(request, "accounts/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "accounts/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "accounts/register.html")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Registration successful. Please login."
        )

        return redirect("accounts:login")

    return render(request, "accounts/register.html")


def user_login(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            # Staff/Admin users → Django/Jazzmin admin
            if user.is_staff:
                return redirect("/admin/")

            # Normal users → Profile
            return redirect("accounts:profile")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "accounts/login.html")


@login_required
def profile(request):
    return render(
        request,
        "accounts/profile.html",
        {
            "user": request.user
        }
    )


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("accounts:login")