import io
import os
from decimal import Decimal

import razorpay

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .models import (
    Room,
    Tenant,
    Booking,
    Payment,
    VacateRequest,
    Complaint,
)


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# CONTACT
# ---------------------------------------------------------

def contact(request):
    from .models import PGProperty

    pg_property = PGProperty.objects.first()

    return render(
        request,
        "pg/contact.html",
        {
            "pg_property": pg_property,
        }
    )

# ---------------------------------------------------------
# SIGNUP
# ---------------------------------------------------------

def generate_tenant_id():

    while True:

        tenant_id = (
            f"TNT-{timezone.now().strftime('%y%m%d')}-"
            f"{os.urandom(3).hex().upper()}"
        )

        if not Tenant.objects.filter(
            tenant_id=tenant_id
        ).exists():

            return tenant_id


def signup(request):

    if request.user.is_authenticated:
        return redirect("user_home")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        if not username or not email or not phone or not password:

            messages.error(
                request,
                "Please fill in all required fields."
            )

            return redirect("signup")

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("signup")

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("signup")

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email is already registered."
            )

            return redirect("signup")

        if Tenant.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "A tenant profile already exists with this email."
            )

            return redirect("signup")

        with transaction.atomic():

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            Tenant.objects.create(
                user=user,
                tenant_id=generate_tenant_id(),
                full_name=username,
                email=email,
                phone_number=phone,
                gender="Other"
            )

        messages.success(
            request,
            "Account created successfully. Please sign in."
        )

        return redirect("login")

    return render(
        request,
        "pg/signup.html"
    )


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------

def user_login(request):

    if request.user.is_authenticated:
        return redirect("user_home")

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

            login(
                request,
                user
            )

            return redirect(
                "user_home"
            )

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "pg/login.html"
    )


# ---------------------------------------------------------
# USER DASHBOARD
# ---------------------------------------------------------

@login_required
def user_home(request):

    tenant = getattr(
        request.user,
        "tenant_profile",
        None
    )

    if tenant is None:

        messages.warning(
            request,
            "Your tenant profile has not been created yet."
        )

        return render(
            request,
            "pg/user_home.html",
            {
                "tenant": None,
                "booking": None,
                "payments": [],
                "complaints": [],
                "vacate_requests": [],
            }
        )

    booking = Booking.objects.filter(
        tenant=tenant,
        status__in=[
            "Confirmed",
            "Active",
        ]
    ).select_related(
        "room",
        "room__property"
    ).first()

    payments = Payment.objects.filter(
        tenant=tenant
    ).select_related(
        "booking",
        "booking__room"
    )[:5]

    complaints = Complaint.objects.filter(
        tenant=tenant
    )[:5]

    vacate_requests = VacateRequest.objects.filter(
        tenant=tenant
    ).select_related(
        "room"
    )[:5]

    return render(
        request,
        "pg/user_home.html",
        {
            "tenant": tenant,
            "booking": booking,
            "payments": payments,
            "complaints": complaints,
            "vacate_requests": vacate_requests,
        }
    )


# ---------------------------------------------------------
# VACATE REQUEST
# ---------------------------------------------------------

@login_required
def vacate_request(request):

    tenant = get_object_or_404(
        Tenant,
        user=request.user
    )

    booking = Booking.objects.filter(
        tenant=tenant,
        status__in=[
            "Confirmed",
            "Active",
        ]
    ).select_related(
        "room"
    ).first()

    if booking is None:

        messages.error(
            request,
            "You do not have an active room."
        )

        return redirect(
            "user_home"
        )

    if request.method == "POST":

        vacate_date = request.POST.get(
            "vacate_date"
        )

        reason = request.POST.get(
            "reason",
            ""
        ).strip()

        if not vacate_date:

            messages.error(
                request,
                "Please select your vacate date."
            )

            return redirect(
                "vacate"
            )

        VacateRequest.objects.create(
            tenant=tenant,
            room=booking.room,
            sharing_type=booking.room.sharing_type,
            vacate_date=vacate_date,
            reason=reason
        )

        messages.success(
            request,
            "Your vacate request has been submitted."
        )

        return redirect(
            "user_home"
        )

    return render(
        request,
        "pg/vacate.html",
        {
            "tenant": tenant,
            "booking": booking,
        }
    )


# ---------------------------------------------------------
# COMPLAINT
# ---------------------------------------------------------

@login_required
def complaint(request):

    tenant = get_object_or_404(
        Tenant,
        user=request.user
    )

    if request.method == "POST":

        complaint_type = request.POST.get(
            "complaint_type",
            ""
        ).strip()

        subject = request.POST.get(
            "subject",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        if not complaint_type or not subject or not description:

            messages.error(
                request,
                "Please fill in all complaint fields."
            )

            return redirect(
                "complaint"
            )

        Complaint.objects.create(
            tenant=tenant,
            complaint_type=complaint_type,
            subject=subject,
            description=description
        )

        messages.success(
            request,
            "Your complaint has been submitted successfully."
        )

        return redirect(
            "user_home"
        )

    complaints = Complaint.objects.filter(
        tenant=tenant
    )

    return render(
        request,
        "pg/complaint.html",
        {
            "tenant": tenant,
            "complaints": complaints,
        }
    )


# ---------------------------------------------------------
# RAZORPAY CLIENT
# ---------------------------------------------------------

def get_razorpay_client():

    key_id = getattr(
        settings,
        "RAZORPAY_KEY_ID",
        ""
    )

    key_secret = getattr(
        settings,
        "RAZORPAY_KEY_SECRET",
        ""
    )

    if not key_id or not key_secret:

        return None

    return razorpay.Client(
        auth=(
            key_id,
            key_secret
        )
    )


# ---------------------------------------------------------
# PAY RENT
# ---------------------------------------------------------

@login_required
def pay_rent(request):

    tenant = get_object_or_404(
        Tenant,
        user=request.user
    )

    booking = Booking.objects.filter(
        tenant=tenant,
        status__in=[
            "Confirmed",
            "Active",
        ]
    ).select_related(
        "room",
        "room__property"
    ).first()

    if booking is None:

        messages.error(
            request,
            "No active room booking was found."
        )

        return redirect(
            "user_home"
        )

    today = timezone.localdate()

    existing_payment = Payment.objects.filter(
        tenant=tenant,
        booking=booking,
        payment_status="Paid",
        payment_date__year=today.year,
        payment_date__month=today.month,
    ).first()

    if existing_payment:

        return render(
            request,
            "pg/pay_rent.html",
            {
                "tenant": tenant,
                "booking": booking,
                "already_paid": existing_payment,
                "razorpay_enabled": bool(
                    get_razorpay_client()
                ),
            }
        )

    client = get_razorpay_client()

    if client is None:

        messages.error(
            request,
            "Online payment is not configured yet."
        )

        return redirect(
            "user_home"
        )

    amount = Decimal(
        booking.monthly_rent
    )

    amount_in_paise = int(
        amount * 100
    )

    receipt_reference = (
        f"SPG-{tenant.tenant_id}-"
        f"{today.strftime('%Y%m%d')}"
    )

    order_data = {
        "amount": amount_in_paise,
        "currency": "INR",
        "receipt": receipt_reference,
        "notes": {
            "tenant_id": tenant.tenant_id,
            "room_number": booking.room.room_number,
            "sharing_type": booking.room.sharing_type,
        }
    }

    try:

        order = client.order.create(
            data=order_data
        )

    except Exception as error:

        messages.error(
            request,
            f"Unable to create payment order: {error}"
        )

        return redirect(
            "user_home"
        )

    payment = Payment.objects.create(
        tenant=tenant,
        booking=booking,
        amount=amount,
        payment_date=today,
        payment_method="Razorpay",
        payment_status="Pending",
        gateway_order_id=order["id"],
        description=(
            f"Monthly rent for Room "
            f"{booking.room.room_number}"
        )
    )

    return render(
        request,
        "pg/pay_rent.html",
        {
            "tenant": tenant,
            "booking": booking,
            "payment": payment,
            "razorpay_order": order,
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "razorpay_enabled": True,
        }
    )


# ---------------------------------------------------------
# PAYMENT SUCCESS CALLBACK
# ---------------------------------------------------------

@login_required
def payment_success(request):

    tenant = get_object_or_404(
        Tenant,
        user=request.user
    )

    razorpay_order_id = request.POST.get(
        "razorpay_order_id"
    )

    razorpay_payment_id = request.POST.get(
        "razorpay_payment_id"
    )

    razorpay_signature = request.POST.get(
        "razorpay_signature"
    )

    if not razorpay_order_id:
        messages.error(
            request,
            "Payment order information is missing."
        )

        return redirect(
            "pay_rent"
        )

    payment = get_object_or_404(
        Payment,
        tenant=tenant,
        gateway_order_id=razorpay_order_id
    )

    client = get_razorpay_client()

    if client is None:

        messages.error(
            request,
            "Payment gateway is not configured."
        )

        return redirect(
            "pay_rent"
        )

    try:

        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }
        )

    except Exception:

        payment.payment_status = "Failed"

        payment.save(
            update_fields=[
                "payment_status"
            ]
        )

        messages.error(
            request,
            "Payment verification failed."
        )

        return redirect(
            "pay_rent"
        )

    with transaction.atomic():

        payment.payment_status = "Paid"

        payment.gateway_payment_id = (
            razorpay_payment_id
        )

        payment.gateway_signature = (
            razorpay_signature
        )

        payment.transaction_id = (
            razorpay_payment_id
        )

        payment.payment_date = (
            timezone.localdate()
        )

        payment.save()

    receipt_pdf = generate_receipt_pdf(
        payment
    )

    email_receipt(
        payment,
        receipt_pdf
    )

    return render(
        request,
        "pg/payment_success.html",
        {
            "payment": payment,
        }
    )


# ---------------------------------------------------------
# GENERATE PDF RECEIPT
# ---------------------------------------------------------

def generate_receipt_pdf(payment):

    buffer = io.BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4
    )

    width, height = A4

    pdf.setTitle(
        f"Receipt-{payment.receipt_number}"
    )

    pdf.setFont(
        "Helvetica-Bold",
        24
    )

    pdf.drawString(
        50,
        height - 70,
        "SUDARSHAN PG"
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        height - 92,
        "Monthly Rent Payment Receipt"
    )

    pdf.line(
        50,
        height - 110,
        width - 50,
        height - 110
    )

    y = height - 150

    booking = payment.booking

    details = [
        (
            "Receipt Number",
            payment.receipt_number
        ),
        (
            "Tenant Name",
            payment.tenant.full_name
        ),
        (
            "Email",
            payment.tenant.email
        ),
        (
            "Phone",
            payment.tenant.phone_number
        ),
        (
            "Room Number",
            booking.room.room_number
            if booking else "-"
        ),
        (
            "Sharing Type",
            booking.room.sharing_type
            if booking else "-"
        ),
        (
            "Payment Date",
            payment.payment_date.strftime(
                "%d-%m-%Y"
            )
        ),
        (
            "Payment Method",
            payment.payment_method
        ),
        (
            "Transaction ID",
            payment.transaction_id
        ),
        (
            "Payment Status",
            payment.payment_status
        ),
    ]

    for label, value in details:

        pdf.setFont(
            "Helvetica-Bold",
            11
        )

        pdf.drawString(
            60,
            y,
            f"{label}:"
        )

        pdf.setFont(
            "Helvetica",
            11
        )

        pdf.drawString(
            190,
            y,
            str(value)
        )

        y -= 27

    y -= 10

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        60,
        y,
        "Amount Paid"
    )

    pdf.setFont(
        "Helvetica-Bold",
        20
    )

    pdf.drawString(
        190,
        y,
        f"Rs. {payment.amount}"
    )

    y -= 70

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        60,
        y,
        "Thank you for staying with Sudarshan PG."
    )

    y -= 20

    pdf.drawString(
        60,
        y,
        "This is a computer-generated receipt."
    )

    pdf.showPage()

    pdf.save()

    buffer.seek(0)

    return buffer.getvalue()


# ---------------------------------------------------------
# EMAIL RECEIPT
# ---------------------------------------------------------

def email_receipt(
    payment,
    receipt_pdf
):

    email = payment.tenant.email

    if not email:
        return

    subject = (
        f"Sudarshan PG - Rent Receipt "
        f"{payment.receipt_number}"
    )

    body = f"""
Hello {payment.tenant.full_name},

Your monthly rent payment has been successfully received.

Payment Details
-------------------------
Receipt Number: {payment.receipt_number}
Room Number: {payment.booking.room.room_number}
Sharing Type: {payment.booking.room.sharing_type}
Amount Paid: Rs. {payment.amount}
Payment Date: {payment.payment_date.strftime("%d-%m-%Y")}
Transaction ID: {payment.transaction_id}

Your payment receipt is attached to this email.

Regards,
Sudarshan PG
"""

    message = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )

    message.attach(
        f"{payment.receipt_number}.pdf",
        receipt_pdf,
        "application/pdf"
    )

    try:
        message.send(
            fail_silently=True
        )
    except Exception:
        pass


# ---------------------------------------------------------
# DOWNLOAD RECEIPT
# ---------------------------------------------------------

@login_required
def download_receipt(
    request,
    payment_id
):

    tenant = get_object_or_404(
        Tenant,
        user=request.user
    )

    payment = get_object_or_404(
        Payment,
        id=payment_id,
        tenant=tenant,
        payment_status="Paid"
    )

    receipt_pdf = generate_receipt_pdf(
        payment
    )

    response = HttpResponse(
        receipt_pdf,
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = (
        f'attachment; '
        f'filename="{payment.receipt_number}.pdf"'
    )

    return response


# ---------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------

def user_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect(
        "home"
    )