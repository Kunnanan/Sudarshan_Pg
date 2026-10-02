from django.urls import path
from . import views


urlpatterns = [

    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Signup
    path(
        "signup/",
        views.signup,
        name="signup"
    ),

    # User Login
    path(
        "user-login/",
        views.user_login,
        name="user_login"
    ),

    # Login aliases
    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "login",
        views.user_login,
        name="login_no_slash"
    ),

    # User Dashboard
    path(
        "user-dashboard/",
        views.user_dashboard,
        name="user_dashboard"
    ),

    # Pay Rent
    path(
        "pay-rent/",
        views.pay_rent,
        name="pay_rent"
    ),

    # Payment Receipt
    path(
        "payment-receipt/<int:payment_id>/",
        views.payment_receipt,
        name="payment_receipt"
    ),

    # Logout
    path(
        "user-logout/",
        views.user_logout,
        name="user_logout"
    ),

    # Contact
    path(
        "contact/",
        views.contact,
        name="contact"
    ),
]