from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    PGProperty,
    Room,
    Tenant,
    Booking,
    Payment,
    Facility,
    Review,
)


@admin.register(PGProperty)
class PGPropertyAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "city",
        "total_rooms",
        "total_beds",
        "is_active",
        "created_at",
    )

    list_filter = (
        "city",
        "is_active",
    )

    search_fields = (
        "name",
        "city",
        "address",
        "contact_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "room_number",
        "property",
        "sharing_type",
        "monthly_rent",
        "total_beds",
        "available_beds",
        "status",
        "attached_bathroom",
    )

    list_filter = (
        "sharing_type",
        "status",
        "attached_bathroom",
        "is_furnished",
        "property",
    )

    search_fields = (
        "room_number",
        "property__name",
    )

    filter_horizontal = (
        "facilities",
    )

    list_editable = (
        "monthly_rent",
        "available_beds",
        "status",
    )


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):

    list_display = (
        "tenant_id",
        "full_name",
        "email",
        "phone_number",
        "gender",
        "is_active",
        "joined_date",
    )

    list_filter = (
        "gender",
        "is_active",
    )

    search_fields = (
        "tenant_id",
        "full_name",
        "email",
        "phone_number",
    )

    readonly_fields = (
        "joined_date",
        "created_at",
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "tenant",
        "room",
        "booking_date",
        "move_in_date",
        "monthly_rent",
        "status",
    )

    list_filter = (
        "status",
        "booking_date",
        "move_in_date",
    )

    search_fields = (
        "tenant__full_name",
        "tenant__tenant_id",
        "room__room_number",
        "room__property__name",
    )

    list_editable = (
        "status",
    )

    readonly_fields = (
        "created_at",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "tenant",
        "amount",
        "payment_date",
        "payment_method",
        "payment_status",
        "transaction_id",
    )

    list_filter = (
        "payment_method",
        "payment_status",
        "payment_date",
    )

    search_fields = (
        "tenant__full_name",
        "tenant__tenant_id",
        "transaction_id",
    )

    list_editable = (
        "payment_status",
    )

    readonly_fields = (
        "created_at",
    )


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "icon",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "tenant",
        "property",
        "rating",
        "title",
        "is_approved",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_approved",
        "created_at",
    )

    search_fields = (
        "tenant__full_name",
        "property__name",
        "title",
        "comment",
    )

    list_editable = (
        "is_approved",
    )

    readonly_fields = (
        "created_at",
    )