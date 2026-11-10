from django.contrib import admin

from .models import (
    PG,
    Room,
    Resident,
    Facility,
    GalleryImage,
    Enquiry,
)


# ============================================================
# PG ADMIN
# ============================================================

@admin.register(PG)
class PGAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "email",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "address",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# ============================================================
# ROOM ADMIN
# ============================================================

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "room_type",
        "pg",
        "rent",
        "total_beds",
        "available_beds",
        "is_available",
    )

    list_filter = (
        "room_type",
        "is_available",
        "pg",
    )

    search_fields = (
        "room_type",
        "pg__name",
    )

    readonly_fields = (
        "available_beds",
    )

    ordering = (
        "room_type",
    )

    def save_model(
        self,
        request,
        obj,
        form,
        change
    ):

        # Save the room first
        super().save_model(
            request,
            obj,
            form,
            change
        )

        # Automatically calculate available beds
        obj.update_availability()


# ============================================================
# RESIDENT ADMIN
# ============================================================

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "room",
        "pg",
        "move_in_date",
        "vacated_date",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "room__room_type",
        "pg",
        "move_in_date",
        "vacated_date",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "room__room_type",
        "pg__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (

        (
            "Resident Information",
            {
                "fields": (
                    "pg",
                    "room",
                    "name",
                    "phone",
                    "email",
                )
            },
        ),

        (
            "Stay Details",
            {
                "fields": (
                    "move_in_date",
                    "vacated_date",
                    "status",
                )
            },
        ),

        (
            "Additional Information",
            {
                "fields": (
                    "notes",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),

    )

    def delete_queryset(
        self,
        request,
        queryset
    ):

        # Store the rooms affected by the residents
        room_ids = set(
            queryset.values_list(
                "room_id",
                flat=True
            )
        )

        # Delete selected residents
        super().delete_queryset(
            request,
            queryset
        )

        # Recalculate availability for affected rooms
        for room_id in room_ids:

            room = Room.objects.filter(
                pk=room_id
            ).first()

            if room:
                room.update_availability()


# ============================================================
# FACILITY ADMIN
# ============================================================

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "pg",
        "icon",
    )

    list_filter = (
        "pg",
    )

    search_fields = (
        "name",
        "description",
        "pg__name",
    )


# ============================================================
# GALLERY IMAGE ADMIN
# ============================================================

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):

    list_display = (
        "caption",
        "pg",
        "created_at",
    )

    list_filter = (
        "pg",
        "created_at",
    )

    search_fields = (
        "caption",
        "pg__name",
    )


# ============================================================
# ENQUIRY ADMIN
# ============================================================

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "email",
        "room_type",
        "move_in_date",
        "is_contacted",
        "created_at",
    )

    list_filter = (
        "room_type",
        "is_contacted",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "pg__name",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )