from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PGProperty(models.Model):
    name = models.CharField(max_length=150)
    address = models.TextField()
    city = models.CharField(max_length=100, default="Bengaluru")
    description = models.TextField(blank=True)

    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)

    total_rooms = models.PositiveIntegerField(default=0)
    total_beds = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "PG Property"
        verbose_name_plural = "PG Properties"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Facility(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: fa-solid fa-wifi"
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Room(models.Model):

    SHARING_CHOICES = [
        ("2 Sharing", "2 Sharing"),
        ("3 Sharing", "3 Sharing"),
        ("4 Sharing", "4 Sharing"),
    ]

    ROOM_STATUS_CHOICES = [
        ("Available", "Available"),
        ("Full", "Full"),
        ("Maintenance", "Maintenance"),
    ]

    property = models.ForeignKey(
        PGProperty,
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    room_number = models.CharField(max_length=30)

    sharing_type = models.CharField(
        max_length=20,
        choices=SHARING_CHOICES
    )

    monthly_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    security_deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    total_beds = models.PositiveIntegerField(default=1)
    available_beds = models.PositiveIntegerField(default=1)

    floor = models.PositiveIntegerField(default=1)

    attached_bathroom = models.BooleanField(default=True)
    balcony = models.BooleanField(default=False)
    is_furnished = models.BooleanField(default=True)

    status = models.CharField(
        max_length=20,
        choices=ROOM_STATUS_CHOICES,
        default="Available"
    )

    facilities = models.ManyToManyField(
        Facility,
        blank=True,
        related_name="rooms"
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ["property", "room_number"]

    def __str__(self):
        return f"{self.property.name} - Room {self.room_number}"


class Tenant(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    tenant_id = models.CharField(
        max_length=20,
        unique=True
    )

    full_name = models.CharField(max_length=150)

    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=15)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    address = models.TextField(blank=True)

    emergency_contact_name = models.CharField(
        max_length=150,
        blank=True
    )

    emergency_contact_number = models.CharField(
        max_length=15,
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

    is_active = models.BooleanField(default=True)

    joined_date = models.DateField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.tenant_id})"


class Booking(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Active", "Active"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
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

    move_out_date = models.DateField(
        null=True,
        blank=True
    )

    monthly_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    security_deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.tenant.full_name} - Room {self.room.room_number}"


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Bank Transfer", "Bank Transfer"),
        ("Card", "Card"),
        ("Other", "Other"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
        ("Refunded", "Refunded"),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    payment_date = models.DateField()

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="Pending"
    )

    transaction_id = models.CharField(
        max_length=150,
        blank=True
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"{self.tenant.full_name} - ₹{self.amount}"


class Review(models.Model):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    property = models.ForeignKey(
        PGProperty,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    title = models.CharField(
        max_length=150,
        blank=True
    )

    comment = models.TextField()

    is_approved = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.tenant.full_name} - {self.rating}/5"