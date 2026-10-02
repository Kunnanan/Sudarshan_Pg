from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Payment


@receiver(post_save, sender=Payment)
def send_payment_confirmation_email(sender, instance, created, **kwargs):

    # Only send email when payment is Paid
    if instance.status != "Paid":
        return

    # Don't send the same confirmation again
    if instance.confirmation_email_sent:
        return

    # -----------------------------------------
    # Get tenant email
    # -----------------------------------------

    email = instance.tenant.email

    if not email and instance.tenant.user:
        email = instance.tenant.user.email

    # No email available
    if not email:
        print("Payment email not sent: tenant has no email address.")
        return

    # -----------------------------------------
    # Room
    # -----------------------------------------

    room_number = "Not Assigned"

    if instance.room:
        room_number = instance.room.room_number

    # -----------------------------------------
    # PG name
    # -----------------------------------------

    pg_name = "Sudarshan PG"

    if instance.tenant.pg:
        pg_name = instance.tenant.pg.name

    # -----------------------------------------
    # Email subject
    # -----------------------------------------

    subject = "Payment Successful - Sudarshan PG"

    # -----------------------------------------
    # Email message
    # -----------------------------------------

    message = f"""
Dear {instance.tenant.name},

Your rent payment has been successfully verified by Sudarshan PG.

========================================
          PAYMENT RECEIPT
========================================

Receipt Number : {instance.receipt_number}

Tenant Name    : {instance.tenant.name}

PG Name        : {pg_name}

Room Number    : {room_number}

Payment For    : {instance.payment_for}

Amount Paid    : ₹{instance.amount}

Payment Method : {instance.payment_method}

Transaction ID : {instance.transaction_id or "Not provided"}

Payment Date   : {instance.payment_date}

Status         : {instance.status}

========================================

Your payment has been successfully completed.

You can login to your Sudarshan PG account to view your payment receipt.

Thank you for staying with Sudarshan PG.

Regards,
Sudarshan PG Management

This is an automatically generated email.
"""

    # -----------------------------------------
    # Send email
    # -----------------------------------------

    try:

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        # Mark email as sent
        Payment.objects.filter(
            pk=instance.pk
        ).update(
            confirmation_email_sent=True
        )

        print(
            f"Payment confirmation email sent successfully to {email}"
        )

    except Exception as e:

        print(
            "Payment confirmation email failed:"
        )

        print(e)