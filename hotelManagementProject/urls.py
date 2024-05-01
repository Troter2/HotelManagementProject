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
from django.contrib.auth import login
from django.urls import path, include
from Cleaning.views import cleaner_page, update_room_status
from User.views import add_guest_view, save_more_guest, save_guest, previous_week, next_week
from Reception.views import reception_ini, reserved_rooms_view, ocuped_rooms_view, rooms_view, \
    contact, what_todo, generate_reservation_pdf, thank_you, \
    update_book_arrive, pay_reservation, booking_filter, reserve_room, booking_filter_check_out, \
    filtrar_por_numero_reserva, order_detail, update_order, add_lost_item, lost_item_list, update_item_reception
from register import views as register
from Restaurant.views import restaurant_reservation_page, restaurant_page, reserved_tables, update_validation, \
    restaurant_reservation_page_uuid, restaurant_validation_page, thanks, restaurant_list_items, create_product, \
    create_item_form, set_order, generate_order_pdf, view_orders_without_reservation

from accounts.views import custom_login
from django.conf import settings
from django.conf.urls.static import static

from register.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/register/", register.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('login/', register.user_login, name='register.user_login'),
    path('', reception_ini, name='home'),
    path('home/',reception_ini, name='home'),
    path('cleaner/', cleaner_page, name='cleaner_page'),
    path('update_room_status/', update_room_status, name='update_room_status'),
    path('update_book_status', update_book_arrive, name='update_book_arrive'),
    path('restaurant/reservations/', restaurant_reservation_page, name='reservation_page'),
    path('reception/reservations/', reserved_rooms_view, name='reserved_rooms_view'),
    path('reception/reservations/filter/', booking_filter, name='booking_filter'),
    path('reception/checkout/', ocuped_rooms_view, name='ocuped_rooms_view'),
    path('reception/checkout/filter/', booking_filter_check_out, name='booking_filter_check_out'),
    path('reception/add_guest/<int:id>/', add_guest_view, name='add_guest_view'),
    path('reception/save_more_guest/', save_more_guest, name='save_more_guest'),
    path('reception/save_guest/<int:id>/', save_guest, name='save_guest'),
    path('pay-reservation/', pay_reservation, name='pay_reservation'),
    path('rooms/', rooms_view, name='rooms_view'),
    path('restaurant/', restaurant_page, name='restaurant_page'),
    path('previous_week/', previous_week, name='previous_week'),
    path('next_week/', next_week, name='next_week'),
    path('reserve/', reserve_room, name='reserve_room'),
    path('contact/', contact, name='contact'),
    path('comprobante/', generate_reservation_pdf, name='comprobante'),
    path('thank_you', thank_you, name='thank_you'),
    path('what_todo/', what_todo, name='what_todo'),
    path('reception/reservations/filter/', booking_filter, name='filtrar_reservas'),
    path('reception/checkout/filter/', booking_filter_check_out, name='booking_filter_check_out'),
    path('restaurant/reservations/<str:uuid>/', restaurant_reservation_page_uuid, name='restaurant_reservation_page_uuid'),
    path('restaurant/items/', restaurant_list_items, name='restaurant_list_items'),
    path('restaurant/create_item_form/', create_item_form, name='restaurant_update_item'),
    path('restaurant/create_product/', create_product, name='create_product'),
    path('camarero/reserved', reserved_tables, name='reserved_tables'),
    path('validar_reserva/', update_validation, name='update_validation'),
    path('filtrar_por_numero_reserva/', filtrar_por_numero_reserva, name='filtrar_por_numero_reserva'),
    path('camarero/', restaurant_validation_page, name='restaurant_validation_page'),
    path('cleaner/lost_item/', add_lost_item, name='add_lost_item'),
    path('camarero/validate', restaurant_validation_page, name='restaurant_validation_page'),
    path('order/', order_detail, name='order_detail'),
    path('order/update_order/', update_order, name='update_order'),
    path('order/thanks/', thanks, name='thanks'),
    path('order/set_order/', set_order, name='set_order'),
    path('reception/lost_items', lost_item_list, name='lost_item_list'),
    path('update_item_reception', update_item_reception, name='update_item_reception'),
    path('order/order_page', view_orders_without_reservation, name='orders_without_page'),
    path('factura/', generate_order_pdf, name='factura'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
