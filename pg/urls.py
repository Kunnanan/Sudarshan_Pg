from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "signup/",
        views.signup,
        name="signup"
    ),

    path(
        "user-home/",
        views.user_home,
        name="user_home"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),

    path(
        "vacate/",
        views.vacate_request,
        name="vacate"
    ),

    path(
        "complaint/",
        views.complaint,
        name="complaint"
    ),

    path(
        "pay-rent/",
        views.pay_rent,
        name="pay_rent"
    ),

    path(
        "payment-success/",
        views.payment_success,
        name="payment_success"
    ),

    path(
        "receipt/<int:payment_id>/",
        views.download_receipt,
        name="download_receipt"
    ),
]