from django.core.exceptions import ValidationError
from django.db import models, transaction


# ============================================================
# PG
# ============================================================

class PG(models.Model):

    name = models.CharField(
        max_length=200
    )

    tagline = models.CharField(
        max_length=300,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    address = models.TextField()

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True
    )

    location_map_url = models.URLField(
        blank=True
    )

    main_image = models.ImageField(
        upload_to="pg/main/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


# ============================================================
# ROOM
# ============================================================

class Room(models.Model):

    SHARING_CHOICES = [
        ("Single", "Single Sharing"),
        ("Triple", "Triple Sharing"),
        ("Four", "Four Sharing"),
    ]

    pg = models.ForeignKey(
        PG,
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    room_type = models.CharField(
        max_length=50,
        choices=SHARING_CHOICES
    )

    rent = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_beds = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    available_beds = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="pg/rooms/",
        blank=True,
        null=True
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def update_availability(self):

        # ----------------------------------------------------
        # If total beds are not known,
        # availability cannot be calculated.
        # ----------------------------------------------------

        if self.total_beds is None:
            return

        # ----------------------------------------------------
        # Count only active residents.
        # Vacated residents are not counted.
        # ----------------------------------------------------

        occupied_beds = self.residents.filter(
            status="Active"
        ).count()

        # ----------------------------------------------------
        # Calculate available beds.
        # ----------------------------------------------------

        self.available_beds = max(
            self.total_beds - occupied_beds,
            0
        )

        # ----------------------------------------------------
        # Room is available only when at least
        # one bed is available.
        # ----------------------------------------------------

        self.is_available = (
            self.available_beds > 0
        )

        # ----------------------------------------------------
        # Update database directly.
        # This avoids calling save() again.
        # ----------------------------------------------------

        Room.objects.filter(
            pk=self.pk
        ).update(
            available_beds=self.available_beds,
            is_available=self.is_available
        )

    def __str__(self):
        return f"{self.pg.name} - {self.room_type}"


# ============================================================
# RESIDENT
# ============================================================

class Resident(models.Model):

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Vacated", "Vacated"),
    ]

    pg = models.ForeignKey(
        PG,
        on_delete=models.CASCADE,
        related_name="residents"
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="residents"
    )

    name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True
    )

    move_in_date = models.DateField()

    vacated_date = models.DateField(
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

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # ========================================================
    # VALIDATION
    # ========================================================

    def clean(self):

        # ----------------------------------------------------
        # ROOM MUST BELONG TO SAME PG
        # ----------------------------------------------------

        if self.room:

            if self.room.pg_id != self.pg_id:

                raise ValidationError(
                    "The selected room does not belong to the selected PG."
                )

        # ----------------------------------------------------
        # ACTIVE RESIDENT VALIDATION
        # ----------------------------------------------------

        if self.status == "Active":

            if self.vacated_date:

                raise ValidationError(
                    "An active resident cannot have a vacated date."
                )

            # ------------------------------------------------
            # CHECK ROOM CAPACITY
            # ------------------------------------------------

            if (
                self.room_id
                and self.room.total_beds is not None
            ):

                active_residents = Resident.objects.filter(
                    room=self.room,
                    status="Active"
                ).exclude(
                    pk=self.pk
                ).count()

                if active_residents >= self.room.total_beds:

                    raise ValidationError(
                        "This room is already full."
                    )

        # ----------------------------------------------------
        # VACATED RESIDENT VALIDATION
        # ----------------------------------------------------

        elif self.status == "Vacated":

            if not self.vacated_date:

                raise ValidationError(
                    "Please enter the vacated date for a vacated resident."
                )

    # ========================================================
    # SAVE
    # ========================================================

    def save(self, *args, **kwargs):

        old_room_id = None

        # ----------------------------------------------------
        # Get previous room before updating the resident.
        # ----------------------------------------------------

        if self.pk:

            old_resident = Resident.objects.filter(
                pk=self.pk
            ).first()

            if old_resident:

                old_room_id = old_resident.room_id

        # ----------------------------------------------------
        # Validate resident data.
        # ----------------------------------------------------

        self.full_clean()

        # ----------------------------------------------------
        # Save resident and update room availability
        # in the same transaction.
        # ----------------------------------------------------

        with transaction.atomic():

            super().save(
                *args,
                **kwargs
            )

            # ------------------------------------------------
            # UPDATE CURRENT ROOM
            # ------------------------------------------------

            if self.room_id:

                current_room = Room.objects.get(
                    pk=self.room_id
                )

                current_room.update_availability()

            # ------------------------------------------------
            # UPDATE PREVIOUS ROOM
            #
            # This is useful if a resident is moved
            # from one room to another.
            # ------------------------------------------------

            if (
                old_room_id
                and old_room_id != self.room_id
            ):

                old_room = Room.objects.get(
                    pk=old_room_id
                )

                old_room.update_availability()

    # ========================================================
    # DELETE
    # ========================================================

    def delete(self, *args, **kwargs):

        room_id = self.room_id

        with transaction.atomic():

            result = super().delete(
                *args,
                **kwargs
            )

            # ------------------------------------------------
            # Recalculate room availability after
            # deleting the resident.
            # ------------------------------------------------

            if room_id:

                room = Room.objects.filter(
                    pk=room_id
                ).first()

                if room:

                    room.update_availability()

            return result

    # ========================================================
    # DISPLAY NAME
    # ========================================================

    def __str__(self):
        return f"{self.name} - {self.room.room_type}"


# ============================================================
# FACILITY
# ============================================================

class Facility(models.Model):

    pg = models.ForeignKey(
        PG,
        on_delete=models.CASCADE,
        related_name="facilities"
    )

    name = models.CharField(
        max_length=100
    )

    icon = models.CharField(
        max_length=20,
        blank=True
    )

    description = models.CharField(
        max_length=300,
        blank=True
    )

    def __str__(self):
        return self.name


# ============================================================
# GALLERY IMAGE
# ============================================================

class GalleryImage(models.Model):

    pg = models.ForeignKey(
        PG,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    image = models.ImageField(
        upload_to="pg/gallery/"
    )

    caption = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.pg.name} - {self.caption}"


# ============================================================
# ENQUIRY
# ============================================================

class Enquiry(models.Model):

    ROOM_CHOICES = [
        ("Single", "Single Sharing"),
        ("Triple", "Triple Sharing"),
        ("Four", "Four Sharing"),
    ]

    pg = models.ForeignKey(
        PG,
        on_delete=models.CASCADE,
        related_name="enquiries"
    )

    name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True
    )

    room_type = models.CharField(
        max_length=50,
        choices=ROOM_CHOICES,
        blank=True
    )

    move_in_date = models.DateField(
        null=True,
        blank=True
    )

    message = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_contacted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.name} - {self.pg.name}"