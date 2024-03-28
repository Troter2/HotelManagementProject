"""
URL configuration for hotelManagementProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views*
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Cleaning.views import cleaner_page, update_room_status
from Reception.views import receptionIni, book_room, checkin_form
from register import views as register
from Restaurant.views import restaurant_reservation_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/register/", register.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', receptionIni),
    path('formulari/', book_room, name="book_room"),
    path('cleaner', cleaner_page, name='cleaner_page'),
    path('update_room_status/', update_room_status, name='update_room_status'),
    path('restaurant/reservations/', restaurant_reservation_page, name='restaurant_reservation_page'),
    path('checkin/', checkin_form, name='checkin_form'),

]
