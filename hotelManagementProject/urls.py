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
from Cleaning.views import cleaner_page, update_room_status, cleaner_shift
from User.views import add_guest_view, save_more_guest, save_guest, shift_management_page, previous_week, next_week
from Reception.views import reception_ini, reserved_rooms_view, ocuped_rooms_view, rooms_view, \
    checkin_form, update_book_arrive, pay_reservation, filtrar_reservas, reserve_room
from register import views as register
from Restaurant.views import restaurant_reservation_page, restaurant_page
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/register/", register.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', reception_ini, name="home"),
    path('cleaner/', cleaner_page, name='cleaner_page'),
    path('shifts/', cleaner_shift, name="shift"),
    path('update_room_status/', update_room_status, name='update_room_status'),
    path('update_book_status', update_book_arrive, name='update_book_arrive'),
    path('restaurant/reservations/', restaurant_reservation_page, name='restaurant_reservation_page'),
    path('reception/reservations/filtrar', filtrar_reservas, name='filtrar_reservas'),
    path('checkin/', checkin_form, name='checkin_form'),
    path('reception/reservations/', reserved_rooms_view, name='reserved_rooms_view'),
    path('reception/checkout/', ocuped_rooms_view, name='ocuped_rooms_view'),
    path('reception/add_guest/<int:id>/', add_guest_view, name='add_guest_view'),
    path('reception/save_more_guest/', save_more_guest, name='save_more_guest'),
    path('reception/save_guest/<int:id>/', save_guest, name='save_guest'),
    path('pay-reservation/', pay_reservation, name='pay_reservation'),
    path('rooms/', rooms_view, name='rooms_view'),
    path('restaurant/', restaurant_page, name='restaurant_page'),
    path('shift_management_page/', shift_management_page, name='shift_management_page'),
    path('previous_week/', previous_week, name='previous_week'),
    path('next_week/', next_week, name='next_week'),
    path('reserve/', reserve_room, name='reserve_room'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
