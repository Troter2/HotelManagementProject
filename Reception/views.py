import datetime
import barcode
from datetime import datetime
from datetime import date

from barcode.writer import ImageWriter
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.graphics.barcode import code39


from Reception.models import RoomReservation, RoomType, Room
from Reception.forms import ReservationForm
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import uuid


def reception_ini(request):
    return render(request, 'reception/home.html')


def rooms_view(request):
    rooms = RoomType.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'reception/roomsType.html', context)


def update_book_arrive(request):
    if request.method == 'POST':
        reservation = RoomReservation.objects.get(id=request.POST.get('id'))
        reservation.guest_is_here = True
        reservation.save()
    return redirect('reserved_rooms_view')


def update_book_gone(request):
    if request.method == 'POST':
        reservation = RoomReservation.objects.get(id=request.POST.get('id'))
        reservation.guest_is_here = True
        reservation.save()
    return redirect('reserved_rooms_view')


def reserved_rooms_view(request):
    reserves = RoomReservation.objects.all().filter(guest_is_here=False)
    context = {
        'reserves': reserves
    }
    return render(request, 'reception/reservedRooms.html', context)


def ocuped_rooms_view(request):
    reserves = RoomReservation.objects.all().filter(guest_is_here=False)
    context = {
        'reserves': reserves
    }
    return render(request, 'reception/ocuped_rooms.html', context)


def pay_reservation(request):
    if request.method == 'POST':
        reserva_id = request.POST.get('id')
        reserva = RoomReservation.objects.get(pk=reserva_id)
        reserva.room_is_payed = True
        reserva.save()
    return redirect('ocuped_rooms_view')


def habitaciones_libres(guest_entry, guest_leave):
    reservas_ocupadas = RoomReservation.objects.filter(
        Q(guest_checkin__lte=guest_entry, guest_checkout__gte=guest_entry) |
        Q(guest_checkin__lte=guest_leave, guest_checkout__gte=guest_leave) |
        Q(guest_checkin__gte=guest_entry, guest_checkout__lte=guest_leave)
    ).values_list('room_number_id', flat=True)

    habitaciones_libres = Room.objects.exclude(id__in=reservas_ocupadas)

    return habitaciones_libres


def reserve_room(request):
    roomTypes = RoomType.objects.all()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['DNI']
            if not validar_dni(dni):
                form.add_error('DNI', 'El DNI no es válido.')
                return render(request, 'reception/reservation_form.html', {'form': form, 'roomTypes': roomTypes})
            form.instance.price = 60
            uid = uuid.uuid4()
            uid_str = str(uid)
            nights = (datetime.strptime(request.POST['guest_checkout'], '%Y-%m-%d') - datetime.strptime(
                request.POST['guest_checkin'], '%Y-%m-%d')).days
            free_rooms = habitaciones_libres(datetime.strptime(request.POST['guest_checkin'], '%Y-%m-%d'),
                                             datetime.strptime(request.POST['guest_checkout'], '%Y-%m-%d'))
            if len(free_rooms) < 1:
                return render(request, 'reception/reservation_form.html', {'form': form, 'roomTypes': roomTypes})

            room = RoomReservation.objects.create(reservation_number=uuid, DNI=request.POST['DNI'],
                                                  guests_name=request.POST['guests_name'],
                                                  guests_surname=request.POST['guests_surname'],
                                                  guests_email=request.POST['guests_email'],
                                                  guests_phone=request.POST['guests_phone'],
                                                  guest_checkin=request.POST['guest_checkin'],
                                                  guest_checkout=request.POST['guest_checkout'],
                                                  guests_number=request.POST['guests_number'],
                                                  price=(RoomType.objects.filter(id=request.POST['room_type'])[
                                                             0].price + int(request.POST['guests_number'])) * nights,
                                                  room_number=free_rooms[0]

                                                  )
            return render(request, 'reception/thank_you.html', {'id': room.id})

    else:
        form = ReservationForm()
    return render(request, 'reception/reservation_form.html', {'form': form, 'roomTypes': roomTypes})


def validar_dni(dni):
    if len(dni) != 9:
        return False
    if not dni[:8].isdigit():
        return False
    if not dni[8].isalpha():
        return False
    return True


def booking_filter(request):
    # Obtener los parámetros de filtrado desde la URL
    nombre_habitacion = request.GET.get('nombre_habitacion', None)
    fecha = request.GET.get('fecha', None)

    # Filtrar las reservas basadas en los parámetros recibidos
    reserves_filtradas = RoomReservation.objects.all()
    if nombre_habitacion:
        reserves_filtradas = reserves_filtradas.filter(guests_name=nombre_habitacion)
    if fecha:
        reserves_filtradas = reserves_filtradas.filter(guest_checkin=fecha)

    # Renderizar la plantilla con las reservas filtradas
    return render(request, 'reception/reservedRooms.html', {'reserves': reserves_filtradas})


def what_todo(request):
    return render(request, 'generic/what_to_do.html')


def contact(request):
    return render(request, 'generic/contact.html')


def booking_filter_check_out(request):
    # Obtener los parámetros de filtrado desde la URL
    nombre_habitacion = request.GET.get('nombre_habitacion', None)
    fecha = request.GET.get('fecha', None)

    # Filtrar las reservas basadas en los parámetros recibidos
    reserves_filtradas = RoomReservation.objects.all()
    if nombre_habitacion:
        reserves_filtradas = reserves_filtradas.filter(guests_name=nombre_habitacion)
    if fecha:
        reserves_filtradas = reserves_filtradas.filter(guest_checkout=fecha)

    # Renderizar la plantilla con las reservas filtradas
    return render(request, 'reception/ocuped_rooms.html', {'reserves': reserves_filtradas})


def generate_reservation_pdf(request):
    now = datetime.now()
    # Recuperar el número de reserva de la solicitud POST
    id = request.POST.get('id', '')
    reservation = RoomReservation.objects.get(pk=id)

    # Generar el contenido del PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    # Agregar el logotipo al PDF
    img_path = 'static/img/Logo.png'  # Ruta al archivo de imagen del logo
    img = ImageReader(img_path)
    c.drawImage(img, x=20, y=780, width=50, height=50, mask='auto')

    img_path = 'static/img/playa-pdf.jpg'  # Ruta al archivo de imagen del logo
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

    text = "Localizado en C/Ejemplo"
    titleObject = c.beginText(30, 770)
    titleObject.setFont("Helvetica", 12)
    titleObject.setTextOrigin(50, 495)
    titleObject.textLine(text)
    c.drawText(titleObject)

    titleObject = c.beginText(80, 770)
    titleObject.setFont("Helvetica", 21)
    titleObject.setTextOrigin(190, 520)
    titleObject.textLine("Comprovante de reserva")
    c.drawText(titleObject)



    barcode = code39.Standard39(reservation.reservation_number, barWidth=0.8, barHeight=50, humanReadable=True)
    barcode.drawOn(c, 60, 250 )
    c.save()

    # Preparar la respuesta HTTP con el PDF
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="comprobante.pdf"'
    return response


def thank_you(request):
    return render(request, 'reception/thank_you.html')
