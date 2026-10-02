from django.db import models
from django.contrib.auth.models import User


# ============================================================
# PG PROPERTY
# ============================================================

class PGProperty(models.Model):

    name = models.CharField(max_length=150)

    address = models.TextField()

    city = models.CharField(max_length=100)

    phone = models.CharField(max_length=20)

    email = models.EmailField(blank=True)

    description = models.TextField(blank=True)

    rules = models.TextField(
        blank=True,
        help_text="Enter PG rules and regulations."
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "PG Property"
        verbose_name_plural = "PG Properties"

    def __str__(self):
        return self.name


# ============================================================
# ROOM
# ============================================================

class Room(models.Model):

    SHARING_CHOICES = [
        ("2 Sharing", "2 Sharing"),
        ("3 Sharing", "3 Sharing"),
        ("4 Sharing", "4 Sharing"),
        ("5 Sharing", "5 Sharing"),
        ("Single", "Single"),
    ]

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Partially Occupied", "Partially Occupied"),
        ("Full", "Full"),
        ("Maintenance", "Maintenance"),
    ]

    pg = models.ForeignKey(
        PGProperty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rooms"
    )

    room_number = models.CharField(max_length=20)

    floor = models.CharField(
        max_length=50,
        blank=True
    )

    sharing_type = models.CharField(
        max_length=30,
        choices=SHARING_CHOICES,
        default="2 Sharing"
    )

    rent = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    capacity = models.PositiveIntegerField(
        default=1
    )

    occupied_beds = models.PositiveIntegerField(
        default=0
    )

    vacancy = models.PositiveIntegerField(
        default=0
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Available"
    )

    attached_bathroom = models.BooleanField(
        default=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if self.capacity < 1:
            self.capacity = 1

        if self.occupied_beds < 0:
            self.occupied_beds = 0

        if self.occupied_beds > self.capacity:
            self.occupied_beds = self.capacity

        if self.vacancy > self.capacity:
            self.vacancy = self.capacity

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Room {self.room_number} - {self.sharing_type}"


# ============================================================
# TENANT
# ============================================================

class Tenant(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Left", "Left"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tenant_profile"
    )

    pg = models.ForeignKey(
        PGProperty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tenants"
    )

    name = models.CharField(
        max_length=150
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    emergency_contact_name = models.CharField(
        max_length=150,
        blank=True
    )

    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True
    )

    id_proof_type = models.CharField(
        max_length=50,
        blank=True
    )

    id_proof_number = models.CharField(
        max_length=100,
        blank=True
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tenants"
    )

    joining_date = models.DateField(
        null=True,
        blank=True
    )

    leaving_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# ============================================================
# BOOKING
# ============================================================

class Booking(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
        ("Completed", "Completed"),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    booking_date = models.DateField()

    move_in_date = models.DateField()

    expected_move_out_date = models.DateField(
        null=True,
        blank=True
    )

    advance_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.tenant.name} - Room {self.room.room_number}"


# ============================================================
# PAYMENT
# ============================================================

class Payment(models.Model):

    PAYMENT_METHODS = [
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Bank Transfer", "Bank Transfer"),
        ("Card", "Card"),
        ("Other", "Other"),
    ]

    PAYMENT_STATUS = [
        ("Paid", "Paid"),
        ("Pending", "Pending"),
        ("Partial", "Partial"),
        ("Failed", "Failed"),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField()

    payment_for = models.CharField(
        max_length=100,
        default="Monthly Rent"
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHODS,
        default="UPI"
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    transaction_id = models.CharField(
        max_length=150,
        blank=True
    )

    receipt_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    confirmation_email_sent = models.BooleanField(
        default=False
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        import uuid

        if not self.receipt_number:

            self.receipt_number = (
                "SPG-" +
                uuid.uuid4().hex[:10].upper()
            )

        if self.status == "Paid" and not self.paid_at:

            from django.utils import timezone

            self.paid_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.tenant.name} - "
            f"₹{self.amount} - "
            f"{self.status}"
        )


# ============================================================
# FACILITY
# ============================================================

class Facility(models.Model):

    name = models.CharField(
        max_length=100
    )

    icon = models.CharField(
        max_length=100,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.name


# ============================================================
# REVIEW
# ============================================================

class Review(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    name = models.CharField(
        max_length=100
    )

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    rating = models.PositiveIntegerField(
        default=5
    )

    review = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.rating}/5"


# ============================================================
# COMPLAINT
# ============================================================

class Complaint(models.Model):

    STATUS_CHOICES = [
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
        ("Closed", "Closed"),
    ]

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Urgent", "Urgent"),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="complaints"
    )

    subject = models.CharField(
        max_length=200
    )

    description = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Open"
    )

    admin_reply = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.subject