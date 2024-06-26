import datetime
from PyPDF2 import PdfMerger
from decimal import Decimal

import barcode
from datetime import datetime
from datetime import date

import qrcode
import json
from barcode.writer import ImageWriter
from django.db.models import Q, F, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from reportlab.graphics.barcode import code39
from reportlab.lib.pagesizes import letter

from Reception.models import RoomReservation, RoomType, Room
from Reception.forms import ReservationForm
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import uuid
from Reception.models import LostItem

from Restaurant.models import Order, Item, ItemAmount, RestaurantReservation
from Restaurant.views import calculate_total, create_order_pdf_bytes
from Billing.models import Promotion, Coupon


def reception_ini(request):
    promotions = Promotion.objects.all()
    return render(request, 'reception/home.html', {'promotions': promotions})


def rooms_view(request):
    rooms = RoomType.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'reception/roomsType.html', context)


def update_book_arrive(request):
    if request.user.has_perm('recepcionist'):
        if request.method == 'POST':
            reservation = RoomReservation.objects.get(id=request.POST.get('id'))
            reservation.guest_is_here = True
            reservation.save()
        return redirect('reserved_rooms_view')
    return redirect('home')


def update_book_gone(request):
    if request.user.has_perm('recepcionist'):
        if request.method == 'POST':
            reservation = RoomReservation.objects.get(id=request.POST.get('id'))
            reservation.guest_leaved = True
            reservation.save()
        return redirect('ocuped_rooms_view')
    return redirect('home')


def reserved_rooms_view(request):
    if request.user.has_perm('recepcionist'):
        reserves = RoomReservation.objects.all().filter(guest_is_here=False, guest_checkin=datetime.today())
        context = {
            'reserves': reserves
        }
        return render(request, 'reception/reservedRooms.html', context)
    return redirect('home')


def ocuped_rooms_view(request):
    if request.user.has_perm('recepcionist'):
        room_reservations = RoomReservation.objects.filter(guest_is_here=True, guest_leaved=False,
                                                           guest_checkout=datetime.today())
        room_reservations_with_prices = []

        for room_reservation in room_reservations:
            restaurant_reservations = RestaurantReservation.objects.filter(room_reservation=room_reservation)
            total_sum = restaurant_reservations.aggregate(total=Sum('order_num__total'))['total'] or 0

            room_reservation_data = {
                'other_spends': total_sum,
                'room_reservation': room_reservation,
                'restaurant_price': total_sum + room_reservation.price
            }

            room_reservations_with_prices.append(room_reservation_data)

        context = {
            'reserves': room_reservations_with_prices
        }
        return render(request, 'reception/ocuped_rooms.html', context)
    return redirect('home')


def pay_reservation(request):
    if request.user.has_perm('recepcionist'):
        if request.method == 'POST':
            reserva_id = request.POST.get('id')
            reserva = RoomReservation.objects.get(pk=reserva_id)
            reserva.room_is_payed = True
            reserva.guest_leaved = True
            reserva.save()
        return redirect('ocuped_rooms_view')
    return redirect('home')


def generate_room_invoice(request, uuid=None):
    if request.user.has_perm(['recepcionist', 'accountant']):
        if request.method == 'GET':
            reserve_uuid = request.GET.get('uuid')
        elif uuid != None:
            reserve_uuid = uuid
        else:
            return redirect('home')


        buffer_main = BytesIO()
        room_reservation = get_object_or_404(RoomReservation, reservation_number=reserve_uuid)
        restaurant_reservation = RestaurantReservation.objects.filter(room_reservation=room_reservation)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

        c = canvas.Canvas(buffer_main, pagesize=letter)

        img_path = 'static/img/Logo.png'
        img = ImageReader(img_path)
        c.drawImage(img, x=20, y=720, width=50, height=50, mask='auto')

        titleObject = c.beginText(80, 770)
        titleObject.setFont("Helvetica", 21)
        titleObject.setTextOrigin(80, 735)
        titleObject.textLine("Restaurante las Palmeras")
        c.drawText(titleObject)

        titleObject = c.beginText(80, 770)
        titleObject.setFont("Helvetica", 21)
        titleObject.setTextOrigin(30, 685)
        titleObject.textLine("Factura nº" + str(room_reservation.id))
        c.drawText(titleObject)

        text = f"Check-in: {room_reservation.guest_checkin}"
        titleObject = c.beginText(30, 770)
        titleObject.setFont("Helvetica", 12)
        titleObject.setTextOrigin(30, 630)
        titleObject.textLine(text)
        c.drawText(titleObject)

        text = f"Precio por noche: {room_reservation.room_number.room_type.price}"
        titleObject = c.beginText(30, 770)
        titleObject.setFont("Helvetica", 12)
        titleObject.setTextOrigin(30, 610)
        titleObject.textLine(text)
        c.drawText(titleObject)

        text = f"Nº noches: {(room_reservation.guest_checkout - room_reservation.guest_checkin).days}"
        titleObject = c.beginText(30, 770)
        titleObject.setFont("Helvetica", 12)
        titleObject.setTextOrigin(30, 590)
        titleObject.textLine(text)
        c.drawText(titleObject)

        text = f"Check-out: {room_reservation.guest_checkout}"
        titleObject = c.beginText(30, 740)
        titleObject.setFont("Helvetica", 12)
        titleObject.setTextOrigin(450, 630)
        titleObject.textLine(text)
        c.drawText(titleObject)

        text = f"Precio sin impuestos: {room_reservation.price - (room_reservation.guests_number *
                                                                  (room_reservation.guest_checkout -
                                                                   room_reservation.guest_checkin).days)}€"
        titleObject = c.beginText(30, 770)
        titleObject.setFont("Helvetica", 12)
        titleObject.setTextOrigin(30, 570)
        titleObject.textLine(text)
        c.drawText(titleObject)

        text = f"Impuesto turístico: {room_reservation.guests_number *
                                      (room_reservation.guest_checkout -
                                       room_reservation.guest_checkin).days}€"
        titleObject = c.beginText(30, 770)
        titleObject.setFont("Helvetica", 12)
        titleObject.setTextOrigin(30, 550)
        titleObject.textLine(text)
        c.drawText(titleObject)

        suma = 0
        for reservation in restaurant_reservation:
            suma += reservation.order_num.total

        text = f"Servicios extra: {suma}€"
        titleObject = c.beginText(30, 770)
        titleObject.setFont("Helvetica", 12)
        titleObject.setTextOrigin(30, 530)
        titleObject.textLine(text)
        c.drawText(titleObject)

        text = f"Total: {room_reservation.price + suma}€"
        titleObject = c.beginText(30, 770)
        titleObject.setFont("Helvetica-Bold", 12)
        titleObject.setTextOrigin(30, 510)
        titleObject.textLine(text)
        c.drawText(titleObject)

        c.showPage()
        c.save()

        buffers = [buffer_main]

        for reservation in restaurant_reservation:
            if reservation.order_num:
                buffer_individual = create_order_pdf_bytes(reservation)
                buffers.append(buffer_individual)

        merger = PdfMerger()
        for buffer in buffers:
            merger.append(buffer)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="combined.pdf"'

        merger.write(response)
        merger.close()

        return response


def generate_room_invoice_for_preview(request):
    if request.user.has_perm(['recepcionist', 'accountant']):
        if request.method == 'GET':
            buffer_main = BytesIO()

            reserve_uuid = request.GET.get('uuid')
            room_reservation = get_object_or_404(RoomReservation, reservation_number=reserve_uuid)
            restaurant_reservation = RestaurantReservation.objects.filter(room_reservation=room_reservation)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="reporte.pdf"'

            c = canvas.Canvas(buffer_main, pagesize=letter)

            img_path = 'static/img/Logo.png'
            img = ImageReader(img_path)
            c.drawImage(img, x=20, y=720, width=50, height=50, mask='auto')

            titleObject = c.beginText(80, 770)
            titleObject.setFont("Helvetica", 21)
            titleObject.setTextOrigin(80, 735)
            titleObject.textLine("Restaurante las Palmeras")
            c.drawText(titleObject)

            titleObject = c.beginText(80, 770)
            titleObject.setFont("Helvetica", 21)
            titleObject.setTextOrigin(30, 685)
            titleObject.textLine("Factura nº" + str(room_reservation.id))
            c.drawText(titleObject)

            text = f"Nº huespedes: {room_reservation.guests_number}"
            titleObject = c.beginText(30, 770)
            titleObject.setFont("Helvetica", 12)
            titleObject.setTextOrigin(450, 630)
            titleObject.textLine(text)
            c.drawText(titleObject)

            text = f"Check-in: {room_reservation.guest_checkin}"
            titleObject = c.beginText(30, 770)
            titleObject.setFont("Helvetica", 12)
            titleObject.setTextOrigin(30, 630)
            titleObject.textLine(text)
            c.drawText(titleObject)

            text = f"Precio por noche: {room_reservation.room_number.room_type.price}€"
            titleObject = c.beginText(30, 770)
            titleObject.setFont("Helvetica", 12)
            titleObject.setTextOrigin(30, 610)
            titleObject.textLine(text)
            c.drawText(titleObject)

            text = f"Nº noches: {(room_reservation.guest_checkout - room_reservation.guest_checkin).days}"
            titleObject = c.beginText(30, 770)
            titleObject.setFont("Helvetica", 12)
            titleObject.setTextOrigin(30, 590)
            titleObject.textLine(text)
            c.drawText(titleObject)

            text = f"Check-out: {room_reservation.guest_checkout}"
            titleObject = c.beginText(30, 740)
            titleObject.setFont("Helvetica", 12)
            titleObject.setTextOrigin(450, 610)
            titleObject.textLine(text)
            c.drawText(titleObject)

            text = f"Precio sin impuestos: {room_reservation.price - (room_reservation.guests_number *
                                                                      (room_reservation.guest_checkout -
                                                                       room_reservation.guest_checkin).days)}€"
            titleObject = c.beginText(30, 770)
            titleObject.setFont("Helvetica", 12)
            titleObject.setTextOrigin(30, 570)
            titleObject.textLine(text)
            c.drawText(titleObject)

            text = f"Impuesto turístico: {room_reservation.guests_number *
                                          (room_reservation.guest_checkout -
                                           room_reservation.guest_checkin).days}€"
            titleObject = c.beginText(30, 770)
            titleObject.setFont("Helvetica", 12)
            titleObject.setTextOrigin(30, 550)
            titleObject.textLine(text)
            c.drawText(titleObject)

            suma = 0
            for reservation in restaurant_reservation:
                suma += reservation.order_num.total

            text = f"Servicios extra: {suma}€"
            titleObject = c.beginText(30, 770)
            titleObject.setFont("Helvetica", 12)
            titleObject.setTextOrigin(30, 530)
            titleObject.textLine(text)
            c.drawText(titleObject)

            text = f"Total: {room_reservation.price + suma}€"
            titleObject = c.beginText(30, 770)
            titleObject.setFont("Helvetica-Bold", 12)
            titleObject.setTextOrigin(30, 510)
            titleObject.textLine(text)
            c.drawText(titleObject)

            c.showPage()
            c.save()

            buffer_main.seek(0)
            buffers = [buffer_main]

            for reservation in restaurant_reservation:
                if reservation.order_num:
                    buffer_individual = create_order_pdf_bytes(reservation)
                    buffers.append(buffer_individual)

            merger = PdfMerger()
            for buffer in buffers:
                merger.append(buffer)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="combined.pdf"'

            merger.write(response)
            merger.close()

            return response
        else:
            return HttpResponse("Method not allowed", status=405)
    else:
        return HttpResponse("Permission denied", status=403)


def pay_reservation_with_invoices(request):
    if request.user.has_perm('recepcionist'):
        if request.method == 'POST':
            reserva_id = request.POST.get('id')
            reserva = RoomReservation.objects.get(pk=reserva_id)
            reserva.room_is_payed = True
            reserva.guest_leaved = True
            reserva.save()
            return generate_room_invoice(request,reserva.reservation_number)

        return redirect('ocuped_rooms_view')
    return redirect('home')


def habitaciones_libres(guest_entry, guest_leave, room_type=None):
    guest_entry_start = datetime.combine(guest_entry, datetime.min.time())
    guest_entry_end = datetime.combine(guest_entry, datetime.max.time())
    guest_leave_start = datetime.combine(guest_leave, datetime.min.time())
    guest_leave_end = datetime.combine(guest_leave, datetime.max.time())

    reservas_ocupadas = RoomReservation.objects.filter(
        Q(guest_checkin__lte=guest_entry_end, guest_checkout__gt=guest_entry_start) |
        Q(guest_checkin__lt=guest_leave_end, guest_checkout__gte=guest_leave_start) |
        Q(guest_checkin__gte=guest_entry_start, guest_checkout__lte=guest_leave_end)
    ).values_list('room_number_id', flat=True)

    habitaciones_disponibles = Room.objects.exclude(id__in=reservas_ocupadas)
    habitaciones_disponibles = habitaciones_disponibles.filter(room_type=room_type)

    return habitaciones_disponibles


def reserve_room(request):
    roomTypes = RoomType.objects.all()
    active_coupons = Coupon.objects.filter(active=True)
    coupons_data = {coupon.discount_code: float(coupon.discount_percentage) for coupon in active_coupons}

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            dni = request.POST.get('DNI')
            fecha_entrada = datetime.strptime(request.POST['guest_checkin'], '%Y-%m-%d')
            fecha_salida = datetime.strptime(request.POST['guest_checkout'], '%Y-%m-%d')
            room_type = request.POST.get('room_type')
            free_rooms = habitaciones_libres(fecha_entrada, fecha_salida, room_type=room_type)
            guests_phone = request.POST.get('guests_phone')
            guests_number = request.POST.get('guests_number')
            coupon_code = request.POST.get('coupon_code')
            discount_percentage = coupons_data.get(coupon_code, 0)

            if not validar_dni(dni):
                form.add_error('DNI', 'El DNI no es válido.')
            if len(free_rooms) < 1:
                form.add_error('guest_checkin', 'No existe habitacion disponible para las fechas elegidas')
            if not validate_guests_phone(guests_phone):
                form.add_error('guests_phone', 'El telefono introducido no es válido.')
            if validate_guests_number(guests_number):
                form.add_error('guests_number', 'El numero de huespedes no puede ser 0.')
            if len(form.errors) > 0:
                return render(request, 'reception/reservation_form.html',
                              {'form': form, 'roomTypes': roomTypes, 'coupons': coupons_data})

            uid = uuid.uuid4()
            nights = (fecha_salida - fecha_entrada).days
            room_type = RoomType.objects.filter(id=request.POST['room_type'])[0].price
            turistic_import = int(guests_number) * nights
            total_price = (room_type * nights) + turistic_import
            discounted_price = total_price - (total_price * (Decimal(discount_percentage) / 100))
            room = RoomReservation.objects.create(
                reservation_number=uid,
                DNI=request.POST['DNI'],
                guests_name=request.POST['guests_name'],
                guests_surname=request.POST['guests_surname'],
                guests_email=request.POST['guests_email'],
                guests_phone=request.POST['guests_phone'],
                guest_checkin=request.POST['guest_checkin'],
                guest_checkout=request.POST['guest_checkout'],
                guests_number=request.POST['guests_number'],
                price=discounted_price,
                room_number=free_rooms[0]
            )

            if 'save_data' in request.POST and request.POST['save_data'] == 'on':
                if request.user.is_authenticated:
                    user = request.user
                    user.DNI = request.POST['DNI']
                    user.telefono = request.POST['guests_phone']
                    user.first_name = request.POST['guests_name']
                    user.last_name = request.POST['guests_surname']
                    user.email = request.POST['guests_email']
                    user.save()

            return render(request, 'reception/thank_you.html', {'id': room.id})

    else:
        form = ReservationForm()
        if request.user.is_authenticated:
            user = request.user
            user_data = {
                'dni': user.DNI,
                'name': user.first_name,
                'lastname': user.last_name,
                'mail': user.email,
                'phone': user.telefono,
            }
            return render(request, 'reception/reservation_form.html',
                          {'form': form, 'roomTypes': roomTypes, 'user_data': user_data, 'coupons': coupons_data})

        return render(request, 'reception/reservation_form.html',
                      {'form': form, 'roomTypes': roomTypes, 'coupons': coupons_data})


def validar_dni(dni):
    if len(dni) != 9:
        return False
    if not dni[:8].isdigit():
        return False
    if not dni[8].isalpha():
        return False
    return True


def validate_guests_phone(guests_phone):
    return len(guests_phone) == 9 or len(guests_phone) == 11


def validate_guests_number(guests_number):
    return len(guests_number) == 0


def booking_filter(request):
    if request.user.has_perm('recepcionist'):

        nombre_habitacion = request.GET.get('nombre_habitacion', None)
        fecha = request.GET.get('fecha', None)

        reserves_filtradas = RoomReservation.objects.all()
        if not nombre_habitacion and not fecha:
            reserves_filtradas = RoomReservation.objects.filter(guest_is_here=False, guest_checkin=datetime.today())

        if nombre_habitacion:
            reserves_filtradas = reserves_filtradas.filter(guests_name=nombre_habitacion,
                                                           guest_is_here=False)
        if fecha:
            reserves_filtradas = reserves_filtradas.filter(guest_checkin=fecha, guest_is_here=False)

        return render(request, 'reception/reservedRooms.html', {'reserves': reserves_filtradas})

    return redirect('home')


def what_todo(request):
    return render(request, 'generic/what_to_do.html')


def contact(request):
    return render(request, 'generic/contact.html')


def booking_filter_check_out(request):
    if request.user.has_perm('recepcionist'):
        nombre_habitacion = request.GET.get('nombre_habitacion', None)
        fecha = request.GET.get('fecha', None)

        reserves_filtradas = RoomReservation.objects.filter(guest_leaved=False, guest_is_here=True)

        if not nombre_habitacion and not fecha:
            reserves_filtradas = RoomReservation.objects.filter(guest_leaved=False, guest_is_here=True)
        if nombre_habitacion:
            reserves_filtradas = reserves_filtradas.filter(guests_name=nombre_habitacion)
        if fecha:
            reserves_filtradas = reserves_filtradas.filter(guest_checkout=fecha)

        room_reservations_with_prices = []

        for room_reservation in reserves_filtradas:
            restaurant_reservations = RestaurantReservation.objects.filter(room_reservation=room_reservation)
            total_sum = restaurant_reservations.aggregate(total=Sum('order_num__total'))['total'] or 0

            room_reservation_data = {
                'other_spends': total_sum,
                'room_reservation': room_reservation,
                'restaurant_price': total_sum + room_reservation.price
            }

            room_reservations_with_prices.append(room_reservation_data)

        context = {
            'reserves': room_reservations_with_prices
        }
        return render(request, 'reception/ocuped_rooms.html', context)
    return redirect('home')


def lost_item_list(request):
    if request.user.has_perm('recepcionist'):
        items = LostItem.objects.all()

        return render(request, 'reception/lost_items_list.html', {'items': items})
    return redirect('home')


def update_item_reception(request):
    if request.user.has_perm('recepcionist'):
        if request.method == 'POST':
            id = request.POST.get("id")
            context = {}
            try:
                item_to_delete = LostItem.objects.get(id=int(id))
                item_to_delete.delete()
            except:
                items = LostItem.objects.all()
                context.update({'error': 'No se pudo entregar el objeto, porfavor intentelo de nuevo'})
            items = LostItem.objects.all()
            context.update({'items': items})
            return render(request, 'reception/lost_items_list.html',
                          context)

        return redirect('lost_item_list')
    return redirect('home')


def delete_booking(request):
    if request.user.has_perm('receptionist'):
        borrar_reserva = request.POST['id']
        reservation = RoomReservation.objects.get(pk=borrar_reserva)
        reservation.delete()
        return redirect(reserved_rooms_view)
    return redirect('home')


def generate_reservation_pdf(request):
    now = datetime.now()
    id = request.POST.get('id', '')
    reservation = RoomReservation.objects.get(pk=id)

    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    img_path = 'static/img/Logo.png'
    img = ImageReader(img_path)
    c.drawImage(img, x=20, y=780, width=50, height=50, mask='auto')

    img_path = 'static/img/playa-pdf.jpg'
    img = ImageReader(img_path)
    c.drawImage(img, x=0, y=550, width=600, height=220, mask='auto')

    # Dibujar el texto en diferentes líneas
    titleObject = c.beginText(80, 770)
    titleObject.setFont("Helvetica", 21)
    titleObject.setTextOrigin(80, 795)
    titleObject.textLine("Hotel las Palmeras")
    c.drawText(titleObject)

    text = f"{date.today()} "
    titleObject = c.beginText(30, 770)
    titleObject.setFont("Helvetica", 12)
    titleObject.setTextOrigin(490, 795)
    titleObject.textLine(text)
    c.drawText(titleObject)

    text = f"Nombre: {reservation.guests_name} {reservation.guests_surname}"
    titleObject = c.beginText(30, 770)
    titleObject.setFont("Helvetica", 12)
    titleObject.setTextOrigin(50, 470)
    titleObject.textLine(text)
    c.drawText(titleObject)

    text = f"Nº huespedes: {reservation.guests_number}"
    titleObject = c.beginText(30, 770)
    titleObject.setFont("Helvetica", 12)
    titleObject.setTextOrigin(50, 445)
    titleObject.textLine(text)
    c.drawText(titleObject)

    text = f"Entrada: {reservation.guest_checkin}"
    titleObject = c.beginText(30, 770)
    titleObject.setFont("Helvetica", 12)
    titleObject.setTextOrigin(443, 495)
    titleObject.textLine(text)
    c.drawText(titleObject)

    text = f"Salida: {reservation.guest_checkout}"
    titleObject = c.beginText(30, 770)
    titleObject.setFont("Helvetica", 12)
    titleObject.setTextOrigin(450, 470)
    titleObject.textLine(text)
    c.drawText(titleObject)

    text = f"DNI: {reservation.DNI} "
    titleObject = c.beginText(30, 770)
    titleObject.setFont("Helvetica", 12)
    titleObject.setTextOrigin(50, 495)
    titleObject.textLine(text)
    c.drawText(titleObject)

    text = "Localizado en C/Ejemplo nº 12"
    titleObject = c.beginText(30, 770)
    titleObject.setFont("Helvetica", 12)
    titleObject.setTextOrigin(50, 420)
    titleObject.textLine(text)
    c.drawText(titleObject)

    titleObject = c.beginText(80, 770)
    titleObject.setFont("Helvetica", 21)
    titleObject.setTextOrigin(190, 520)
    titleObject.textLine("Comprobante de reserva")
    c.drawText(titleObject)

    barcode = code39.Standard39(reservation.reservation_number, barWidth=0.8, barHeight=50, humanReadable=True)
    barcode.drawOn(c, 60, 100)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(
        "http://localhost:8000/restaurant/reservations/" + str(reservation.reservation_number))
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    c.drawInlineImage(qr_img, 250, 250, 100, 100)

    titleObject = c.beginText(80, 770)
    titleObject.setFont("Helvetica", 14)
    titleObject.setTextOrigin(150, 350)
    titleObject.textLine("Escanea el QR para reservar en el restaurante")
    c.drawText(titleObject)

    c.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="comprobante.pdf"'
    return response


def thank_you(request):
    return render(request, 'reception/thank_you.html')


def filtrar_por_numero_reserva(request):
    if request.user.has_perm('recepcionist'):
        if request.method == 'POST':
            numero_reserva = request.POST.get('numero_reserva')  # Obtener el número de reserva del formulario
            numero_reserva = numero_reserva[:-1].lower()
            if numero_reserva:
                reservas_filtradas = RoomReservation.objects.filter(reservation_number=numero_reserva,
                                                                    guest_is_here=False)
            else:
                reservas_filtradas = RoomReservation.objects.filter(guest_is_here=False, guest_checkin=datetime.today())

            return render(request, 'reception/reservedRooms.html', {'reserves': reservas_filtradas})
        else:
            return reserved_rooms_view(request)
    return redirect('home')


def order_detail(request):
    if request.user.has_perm('recepcionist'):
        order = Order.objects.create(total=0)
        items = Item.objects.filter(active=True)
        return render(request, 'restaurant/order_page.html', {'order': order, 'items': items})
    return redirect('home')


def update_order(request):
    if request.user.has_perm('recepcionist'):
        if request.method == 'POST':
            order_data = json.loads(request.body.decode("utf-8"))
            order_id = order_data['order_id']
            order_total = Order.objects.get(id=order_id)
            items_data = order_data['items']

            for item_data in items_data:
                item_id = item_data['item_id']
                amount = item_data['amount']
                if int(amount) >= 0:
                    items = ItemAmount.objects.filter(item_id=item_id, order_id=order_id)
                    if len(items) > 0:
                        items[0].amount = amount
                        items[0].save()
                    else:
                        ItemAmount.objects.get_or_create(item_id=item_id, amount=amount, order_id=order_id)

            order_total.total = calculate_total(order_total)
            order_total.save()

            return redirect('orders_without_page')
    return redirect('home')


def add_lost_item(request):
    if request.user.has_perm('recepcionist'):
        if request.method == 'POST':
            room_number = Room.objects.get(id=request.POST.get('room'))
            item_name = request.POST.get('objectName')
            encounter_hour = datetime.now().time()
            encounter_date = datetime.now().date()

            LostItem.objects.create(
                item_name=item_name,
                encounter_hour=encounter_hour,
                encounter_date=encounter_date,
                room_number=room_number
            )

            return redirect('cleaner_page')

        return render(request, 'cleaner/cleaner_page.html')
    return redirect('home')
