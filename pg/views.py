from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .models import Room

def home(request):

    all_rooms = Room.objects.filter(
        status="Available",
        available_beds__gt=0
    ).select_related(
        "property"
    ).prefetch_related(
        "facilities"
    )

    sharing_types = [
        "2 Sharing",
        "3 Sharing",
        "4 Sharing",
    ]

    rooms = []

    for sharing_type in sharing_types:

        room = all_rooms.filter(
            sharing_type=sharing_type
        ).first()

        if room:
            rooms.append(room)

    return render(
        request,
        "pg/home.html",
        {
            "rooms": rooms,
        }
    )
def contact(request):
    return render(request, "pg/contact.html")


def signup(request):

    if request.user.is_authenticated:
        return redirect("user_home")

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check required fields
        if not username or not email or not password:
            messages.error(request, "Please fill in all required fields.")
            return redirect("signup")

        # Check password
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        # Check username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        # Check email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("signup")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Account created successfully. Please sign in."
        )

        return redirect("login")

    return render(request, "pg/signup.html")


def user_login(request):

    if request.user.is_authenticated:
        return redirect("user_home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("user_home")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "pg/login.html")


@login_required
def user_home(request):
    return render(request, "pg/user_home.html")


def user_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("home")