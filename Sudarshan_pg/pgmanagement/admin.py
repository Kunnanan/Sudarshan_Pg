from django.contrib import admin

from .models import (
    PGProperty,
    Room,
    Tenant,
    Booking,
    Payment,
    Facility,
    Review,
    Complaint,
)


@admin.register(PGProperty)
class PGPropertyAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "city",
        "phone",
        "email",
        "is_active",
    )

    list_filter = (
        "city",
        "is_active",
    )

    search_fields = (
        "name",
        "city",
        "phone",
        "email",
    )

    list_editable = (
        "is_active",
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "room_number",
        "pg",
        "sharing_type",
        "rent",
        "capacity",
        "occupied_beds",
        "vacancy",
        "status",
        "attached_bathroom",
        "is_active",
    )

    list_filter = (
        "pg",
        "sharing_type",
        "status",
        "attached_bathroom",
        "is_active",
    )

    search_fields = (
        "room_number",
        "floor",
    )

    list_editable = (
        "rent",
        "capacity",
        "occupied_beds",
        "vacancy",
        "status",
        "is_active",
    )


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "email",
        "gender",
        "room",
        "joining_date",
        "status",
    )

    list_filter = (
        "gender",
        "status",
        "joining_date",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "id_proof_number",
    )

    list_editable = (
        "status",
    )

    date_hierarchy = "joining_date"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "tenant",
        "room",
        "booking_date",
        "move_in_date",
        "advance_amount",
        "status",
    )

    list_filter = (
        "status",
        "booking_date",
    )

    search_fields = (
        "tenant__name",
        "room__room_number",
    )

    list_editable = (
        "status",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "receipt_number",
        "tenant",
        "room",
        "amount",
        "payment_date",
        "payment_method",
        "status",
        "paid_at",
        "confirmation_email_sent",
    )

    list_filter = (
        "status",
        "payment_method",
        "payment_date",
        "confirmation_email_sent",
    )

    search_fields = (
        "receipt_number",
        "tenant__name",
        "tenant__phone",
        "transaction_id",
    )

    list_editable = (
        "status",
    )

    readonly_fields = (
        "receipt_number",
        "paid_at",
        "confirmation_email_sent",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "payment_date"

    ordering = (
        "-created_at",
    )


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "icon",
        "is_active",
        "display_order",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    list_editable = (
        "is_active",
        "display_order",
    )

    ordering = (
        "display_order",
        "name",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "tenant",
        "rating",
        "status",
        "created_at",
    )

    list_filter = (
        "rating",
        "status",
        "created_at",
    )

    search_fields = (
        "name",
        "review",
        "tenant__name",
    )

    list_editable = (
        "status",
    )

    readonly_fields = (
        "created_at",
    )


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):

    list_display = (
        "subject",
        "tenant",
        "priority",
        "status",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "priority",
        "status",
        "created_at",
    )

    search_fields = (
        "subject",
        "description",
        "tenant__name",
    )

    list_editable = (
        "priority",
        "status",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )