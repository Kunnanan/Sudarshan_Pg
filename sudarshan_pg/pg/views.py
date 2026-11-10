
from datetime import datetime
from urllib.parse import quote

from django.contrib import messages
from django.shortcuts import redirect, render
from django.db.models import Case, When, IntegerField
from django.http import HttpResponse

from .models import (
    PG,
    Room,
    Facility,
    GalleryImage,
    Enquiry,
)


# ============================================================
# HOME
# ============================================================

def home(request):
    pg = PG.objects.filter(is_active=True).first()

    if pg:
        rooms = (
            Room.objects.filter(pg=pg)
            .annotate(
                room_order=Case(
                    When(room_type="Single", then=1),
                    When(room_type="Triple", then=2),
                    When(room_type="Four", then=3),
                    default=99,
                    output_field=IntegerField()
                )
            )
            .order_by("room_order")
        )

        facilities = Facility.objects.filter(pg=pg).order_by("name")
        gallery = GalleryImage.objects.filter(pg=pg).order_by("-created_at")

    else:
        rooms = Room.objects.none()
        facilities = Facility.objects.none()
        gallery = GalleryImage.objects.none()

    context = {
        "pg": pg,
        "rooms": rooms,
        "facilities": facilities,
        "gallery": gallery,
    }

    return render(request, "pg/home.html", context)


# ============================================================
# ABOUT
# ============================================================

def about(request):
    pg = PG.objects.filter(is_active=True).first()

    facilities = (
        Facility.objects.filter(pg=pg).order_by("name")
        if pg
        else Facility.objects.none()
    )

    context = {
        "pg": pg,
        "facilities": facilities,
    }

    return render(request, "pg/about.html", context)


# ============================================================
# ROOMS
# ============================================================

def rooms(request):
    pg = PG.objects.filter(is_active=True).first()

    if pg:
        room_list = (
            Room.objects.filter(pg=pg)
            .annotate(
                room_order=Case(
                    When(room_type="Single", then=1),
                    When(room_type="Triple", then=2),
                    When(room_type="Four", then=3),
                    default=99,
                    output_field=IntegerField()
                )
            )
            .order_by("room_order")
        )
    else:
        room_list = Room.objects.none()

    context = {
        "pg": pg,
        "rooms": room_list,
    }

    return render(request, "pg/rooms.html", context)


# ============================================================
# GALLERY
# ============================================================

def gallery(request):
    pg = PG.objects.filter(is_active=True).first()

    gallery_images = (
        GalleryImage.objects.filter(pg=pg).order_by("-created_at")
        if pg
        else GalleryImage.objects.none()
    )

    context = {
        "pg": pg,
        "gallery": gallery_images,
    }

    return render(request, "pg/gallery.html", context)


# ============================================================
# FACILITIES
# ============================================================

def facilities(request):
    pg = PG.objects.filter(is_active=True).first()

    facility_list = (
        Facility.objects.filter(pg=pg).order_by("name")
        if pg
        else Facility.objects.none()
    )

    context = {
        "pg": pg,
        "facilities": facility_list,
    }

    return render(request, "pg/facilities.html", context)


# ============================================================
# RULES & POLICIES
# ============================================================

def rules(request):
    pg = PG.objects.filter(is_active=True).first()

    context = {
        "pg": pg,
    }

    return render(request, "pg/rules.html", context)


# ============================================================
# CONTACT
# ============================================================

def contact(request):
    pg = PG.objects.filter(is_active=True).first()

    context = {
        "pg": pg,
    }

    return render(request, "pg/contact.html", context)


# ============================================================
# ENQUIRY
# ============================================================

def enquiry(request):
    pg = PG.objects.filter(is_active=True).first()

    if not pg:
        messages.error(
            request,
            "PG details are not available."
        )
        return redirect("home")

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        room_type = request.POST.get("room_type", "").strip()
        move_in_date = request.POST.get("move_in_date", "").strip()
        enquiry_message = request.POST.get("message", "").strip()

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not name:
            messages.error(request, "Please enter your name.")
            return redirect("enquiry")

        if not phone:
            messages.error(request, "Please enter your phone number.")
            return redirect("enquiry")

        # ----------------------------------------------------
        # DATE CONVERSION
        # ----------------------------------------------------

        parsed_move_in_date = None

        if move_in_date:
            try:
                parsed_move_in_date = datetime.strptime(
                    move_in_date,
                    "%Y-%m-%d"
                ).date()

            except ValueError:
                messages.error(
                    request,
                    "Please enter a valid move-in date."
                )
                return redirect("enquiry")

        # ----------------------------------------------------
        # CREATE ENQUIRY
        # ----------------------------------------------------

        Enquiry.objects.create(
            pg=pg,
            name=name,
            phone=phone,
            email=email,
            room_type=room_type,
            move_in_date=parsed_move_in_date,
            message=enquiry_message,
        )

        # ----------------------------------------------------
        # FREE WHATSAPP INTEGRATION
        # ----------------------------------------------------

        owner_number = "919538901339"

        whatsapp_message = (
            "New PG Enquiry - Sudarshan PG\n\n"
            f"Name: {name}\n"
            f"Phone: {phone}\n"
            f"Email: {email or 'Not provided'}\n"
            f"Room Type: {room_type or 'Not specified'}\n"
            f"Move-in Date: {move_in_date or 'Not specified'}\n"
            f"Message: {enquiry_message or 'No message'}"
        )

        whatsapp_url = (
            f"https://wa.me/{owner_number}"
            f"?text={quote(whatsapp_message)}"
        )

        # Store the link temporarily for the success page.
        request.session["whatsapp_url"] = whatsapp_url

        messages.success(
            request,
            "Your enquiry has been submitted successfully."
        )

        return redirect("enquiry_success")

    # --------------------------------------------------------
    # GET REQUEST
    # --------------------------------------------------------

    context = {
        "pg": pg,
    }

    return render(request, "pg/enquiry.html", context)


# ============================================================
# ENQUIRY SUCCESS
# ============================================================

def enquiry_success(request):
    pg = PG.objects.filter(is_active=True).first()

    # Retrieve and remove the WhatsApp URL from the session.
    whatsapp_url = request.session.pop("whatsapp_url", None)

    context = {
        "pg": pg,
        "whatsapp_url": whatsapp_url,
    }

    return render(
        request,
        "pg/enquiry_success.html",
        context
    )
def robots_txt(request):
    content = """User-agent: *
Allow: /

Sitemap: https://YOUR-DOMAIN.com/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")
