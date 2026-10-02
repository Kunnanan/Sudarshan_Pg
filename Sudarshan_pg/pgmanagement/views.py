from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models, transaction

from .models import (
    Facility,
    Room,
    Tenant,
    Payment,
)


# ============================================================
# HOME
# ============================================================

def home(request):

    facilities = Facility.objects.filter(
        is_active=True
    )

    rooms = Room.objects.filter(
        is_active=True
    ).order_by(
        "sharing_type",
        "room_number"
    )

    available_rooms = rooms.filter(
        vacancy__gt=0
    )

    context = {
        "facilities": facilities,
        "rooms": rooms,
        "available_rooms": available_rooms,
    }

    return render(
        request,
        "pgmanagement/home.html",
        context
    )


# ============================================================
# CONTACT
# ============================================================

def contact(request):

    return render(
        request,
        "pgmanagement/contact.html"
    )


# ============================================================
# SIGNUP
# ============================================================

def signup(request):

    if request.user.is_authenticated:

        return redirect(
            "user_dashboard"
        )


    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password"
        )

        confirm_password = request.POST.get(
            "confirm_password"
        )


        # ------------------------------------
        # Validation
        # ------------------------------------

        if not all([
            name,
            email,
            phone,
            username,
            password,
            confirm_password
        ]):

            messages.error(
                request,
                "Please fill in all fields."
            )

            return redirect(
                "signup"
            )


        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect(
                "signup"
            )


        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect(
                "signup"
            )


        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email is already registered."
            )

            return redirect(
                "signup"
            )


        # ------------------------------------
        # Create user + tenant
        # ------------------------------------

        with transaction.atomic():

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=name
            )


            Tenant.objects.create(
                user=user,
                name=name,
                email=email,
                phone=phone
            )


        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect(
            "user_login"
        )


    return render(
        request,
        "pgmanagement/signup.html"
    )


# ============================================================
# USER LOGIN
# ============================================================

def user_login(request):

    if request.user.is_authenticated:

        return redirect(
            "user_dashboard"
        )


    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            # Prevent admin from using user login

            if user.is_staff or user.is_superuser:

                messages.error(
                    request,
                    "Admin accounts must use Admin Login."
                )

                return redirect(
                    "user_login"
                )


            login(
                request,
                user
            )

            return redirect(
                "user_dashboard"
            )


        messages.error(
            request,
            "Invalid username or password."
        )


    return render(
        request,
        "pgmanagement/user_login.html"
    )


# ============================================================
# USER DASHBOARD
# ============================================================
@login_required(login_url="/user-login/")
def payment_receipt(request, payment_id):

    tenant = Tenant.objects.filter(
        user=request.user
    ).first()

    if not tenant:
        messages.error(
            request,
            "Tenant profile not found."
        )

        return redirect("user_dashboard")


    payment = get_object_or_404(
        Payment.objects.select_related(
            "tenant",
            "room"
        ),
        id=payment_id,
        tenant=tenant
    )


    # Receipt should only be available for successful payments
    if payment.status != "Paid":

        messages.error(
            request,
            "Receipt is available only after the payment is marked as Paid."
        )

        return redirect("user_dashboard")


    context = {
        "payment": payment,
    }


    return render(
        request,
        "pgmanagement/payment_receipt.html",
        context
    )
@login_required(login_url="/user-login/")
def user_dashboard(request):

    try:

        tenant = Tenant.objects.select_related(
            "room",
            "user"
        ).get(
            user=request.user
        )

    except Tenant.DoesNotExist:

        messages.error(
            request,
            "Tenant profile not found."
        )

        return redirect(
            "home"
        )


    payments = Payment.objects.filter(
        tenant=tenant
    ).order_by(
        "-payment_date",
        "-created_at"
    )


    # Get complaints safely

    try:

        complaints = tenant.complaints.all().order_by(
            "-created_at"
        )

    except AttributeError:

        complaints = []


    context = {

        "tenant": tenant,

        "payments": payments,

        "complaints": complaints,

    }


    return render(
        request,
        "pgmanagement/user_dashboard.html",
        context
    )


# ============================================================
# PAY RENT
# ============================================================

@login_required(login_url="/user-login/")
def pay_rent(request):

    try:

        tenant = Tenant.objects.select_related(
            "room"
        ).get(
            user=request.user
        )

    except Tenant.DoesNotExist:

        messages.error(
            request,
            "Tenant profile not found."
        )

        return redirect(
            "user_dashboard"
        )


    # ------------------------------------
    # Get monthly rent
    # ------------------------------------

    monthly_rent = 0

    if tenant.room:

        monthly_rent = tenant.room.rent


    # ------------------------------------
    # Submit payment
    # ------------------------------------

    if request.method == "POST":

        amount = request.POST.get(
            "amount"
        )

        payment_method = request.POST.get(
            "payment_method"
        )

        transaction_id = request.POST.get(
            "transaction_id",
            ""
        ).strip()


        if not amount:

            messages.error(
                request,
                "Please enter the payment amount."
            )

            return redirect(
                "pay_rent"
            )


        if not payment_method:

            messages.error(
                request,
                "Please select a payment method."
            )

            return redirect(
                "pay_rent"
            )


        Payment.objects.create(

            tenant=tenant,

            room=tenant.room
            if tenant.room
            else None,

            amount=amount,

            payment_date=date.today(),

            payment_for="Monthly Rent",

            payment_method=payment_method,

            status="Pending",

            transaction_id=transaction_id,

        )


        messages.success(
            request,
            "Rent payment submitted successfully. It is waiting for admin verification."
        )


        return redirect(
            "user_dashboard"
        )


    context = {

        "tenant": tenant,

        "monthly_rent": monthly_rent,

    }


    return render(
        request,
        "pgmanagement/pay_rent.html",
        context
    )


# ============================================================
# USER LOGOUT
# ============================================================

def user_logout(request):

    logout(request)

    return redirect(
        "home"
    )

    # ============================================================
# PAYMENT RECEIPT
# ============================================================

@login_required(login_url="/user-login/")
def payment_receipt(request, payment_id):

    try:

        tenant = Tenant.objects.get(
            user=request.user
        )

        payment = Payment.objects.select_related(
            "tenant",
            "room",
            "tenant__pg"
        ).get(
            id=payment_id,
            tenant=tenant
        )

    except Tenant.DoesNotExist:

        messages.error(
            request,
            "Tenant profile not found."
        )

        return redirect("home")

    except Payment.DoesNotExist:

        messages.error(
            request,
            "Payment receipt not found."
        )

        return redirect("user_dashboard")


    # Only show receipt for successful payments

    if payment.status != "Paid":

        messages.error(
            request,
            "Receipt is available only after payment is verified."
        )

        return redirect("user_dashboard")


    return render(
        request,
        "pgmanagement/payment_receipt.html",
        {
            "payment": payment,
            "tenant": tenant,
        }
    )