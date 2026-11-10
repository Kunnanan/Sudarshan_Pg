
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from pg import views
from pg.sitemaps import StaticViewSitemap


# SITEMAP CONFIGURATION
sitemaps = {
    "static": StaticViewSitemap,
}


urlpatterns = [

    # HOME
    path(
        "",
        views.home,
        name="home"
    ),

    # ABOUT
    path(
        "about/",
        views.about,
        name="about"
    ),

    # ROOMS
    path(
        "rooms/",
        views.rooms,
        name="rooms"
    ),

    # FACILITIES
    path(
        "facilities/",
        views.facilities,
        name="facilities"
    ),

    # GALLERY
    path(
        "gallery/",
        views.gallery,
        name="gallery"
    ),

    # RULES
    path(
        "rules/",
        views.rules,
        name="rules"
    ),

    # CONTACT
    path(
        "contact/",
        views.contact,
        name="contact"
    ),

    # ENQUIRY
    path(
        "enquiry/",
        views.enquiry,
        name="enquiry"
    ),

    # ENQUIRY SUCCESS
    path(
        "enquiry/success/",
        views.enquiry_success,
        name="enquiry_success"
    ),

    # SITEMAP
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap"
    ),
    # ROBOTS.TXT
    path(
        "robots.txt",
        views.robots_txt,
        name="robots_txt"
    ),

    # ADMIN
    path(
        "admin/",
        admin.site.urls
    ),

    # ACCOUNTS
    path(
        "accounts/",
        include("accounts.urls")
    ),
]


# MEDIA FILES (DEVELOPMENT)
if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
