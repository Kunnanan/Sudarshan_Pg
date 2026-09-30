from django.urls import path
from . import views


urlpatterns = [

    path("", views.home, name="home"),

    path("login/", views.user_login, name="login"),

    path("signup/", views.signup, name="signup"),

    path("user-home/", views.user_home, name="user_home"),

    path("logout/", views.user_logout, name="logout"),

    path("contact/", views.contact, name="contact"),

]