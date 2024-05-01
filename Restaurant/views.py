from datetime import date
from datetime import datetime
import qrcode

from django.http import HttpResponse
from django.shortcuts import render, redirect
from reportlab.graphics.barcode import code39
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus.tables import TableStyle, Table

from Restaurant.models import RestaurantReservation, RoomReservation, Order, ItemAmount, Item
from Restaurant.forms import RestaurantReservationForm, ItemForm, RestaurantReservationForm, RestaurantBookingForm
from django.db.models import Q


# Create your views here.


def restaurant_page(request):
    return render(request, 'restaurant/restaurant_page.html')


def restaurant_reservation_page(request):
    if request.method == 'POST':
        form = RestaurantBookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thanks')
    else:
        form = RestaurantBookingForm()
    return render(request, 'restaurant/reservation_page.html', {'form': form})


def restaurant_list_items(request):
    items = Item.objects.all()
    return render(request, 'restaurant/list_items.html', {"products": items})


def create_product(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("restaurant_list_items")


def create_item_form(request):
    if request.method == 'POST':
        item = Item.objects.get(pk=request.POST.get('id'))
        if request.POST.get('action') == "active":
            item.active = True
        else:
            item.active = False
        item.save()
        return redirect("restaurant_list_items")


def restaurant_validation_page(request):
    booking = RestaurantReservation.objects.filter(validated=True)
    return render(request, 'restaurant/validated_list.html', {'reservas': booking})


def restaurant_reservation_page_uuid(request, uuid):
    try:
        room_reservation = RoomReservation.objects.get(reservation_number=uuid)
        initial_data = {
            'client_name': room_reservation.guests_name + ' ' + room_reservation.guests_surname,
            'room_reservation': room_reservation,
        }
    except RoomReservation.DoesNotExist:
        return render(request, "restaurant/reservation_failure.html")

    if request.method == 'POST':
        form = RestaurantReservationForm(request.POST)
        if form.is_valid():
            restaurant_reservation = form.save(commit=False)
            restaurant_reservation.room_reservation = room_reservation
            restaurant_reservation.save()
            return render(request, 'restaurant/thank_you.html')
        else:
            print(form.errors)

    return render(request, 'restaurant/autoreservation_page.html', {'data': initial_data})


def reserved_tables(request):
    date_ = date.today()
    if request.method == 'POST':
        if request.POST.get('fecha') == "":
            pass
        else:
            date_ = request.POST.get('fecha')
    booking = RestaurantReservation.objects.filter(date_entrance=date_).filter(validated=False)
    return render(request, 'restaurant/reserved_tables.html', {'reservas': booking})


def update_validation(request):
    if request.method == 'POST':
        reservation = RestaurantReservation.objects.get(id=request.POST.get('reserva_id'))
        reservation.validated = True
        reservation.save()
    return redirect('reserved_tables')


def calculate_total(order):
    total = 0
    items = ItemAmount.objects.filter(order=order)
    for item in items:
        total += item.item.price * item.amount
    return total


def set_order(request):
    if request.method == 'POST':
        if request.POST.get('reservation_id') == "" or request.POST.get('order_number') == "":
            pass
        else:
            order = Order.objects.get(id=request.POST.get('order_number'))
            reservation = RestaurantReservation.objects.get(id=request.POST.get('reservation_id'))
            reservation.order_num = order
            order.total = calculate_total(order)
            order.save()
            reservation.save()
    return redirect("restaurant_validation_page")


def thanks(request):
    return render(request, 'restaurant/thanks.html')


def generate_order_pdf(request):
    now = datetime.now()
    id = request.POST.get('id', '')
    reservation = RestaurantReservation.objects.get(pk=id)
    items_amounts = []
    if reservation.order_num:
        order = reservation.order_num
        items_amounts = ItemAmount.objects.filter(order=order)

    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    img_path = 'static/img/Logo.png'
    img = ImageReader(img_path)
    c.drawImage(img, x=20, y=780, width=50, height=50, mask='auto')


    titleObject = c.beginText(80, 770)
    titleObject.setFont("Helvetica", 21)
    titleObject.setTextOrigin(80, 795)
    titleObject.textLine("Restaurante las Palmeras")
    c.drawText(titleObject)

    text = f"{date.today()} "
    titleObject = c.beginText(30, 770)
    titleObject.setFont("Helvetica", 12)
    titleObject.setTextOrigin(490, 795)
    titleObject.textLine(text)
    c.drawText(titleObject)

    text = f"Nombre: {reservation.client_name}"
    titleObject = c.beginText(30, 770)
    titleObject.setFont("Helvetica", 12)
    titleObject.setTextOrigin(30, 720)
    titleObject.textLine(text)
    c.drawText(titleObject)

    text = f"Nº comensales: {reservation.costumers_number}"
    titleObject = c.beginText(30, 770)
    titleObject.setFont("Helvetica", 12)
    titleObject.setTextOrigin(450, 720)
    titleObject.textLine(text)
    c.drawText(titleObject)


    titleObject = c.beginText(80, 770)
    titleObject.setFont("Helvetica", 21)
    titleObject.setTextOrigin(30, 745)
    titleObject.textLine("Factura nº" + str(order.id))
    c.drawText(titleObject)

    starting_y = 420
    titleObject = c.beginText(30, starting_y)
    titleObject.setFont("Helvetica", 12)

    data=[]


    data.append(["Producto", 'Cantidad', 'Precio', 'Precio total'])
    for item in items_amounts:
        data.append([item.item.name,item.amount,item.item.price, item.amount*item.item.price])
    data.append(["Total","","",order.total])

    num_columns = len(data[0])
    width, height = letter
    column_width = (width-20) / num_columns

    t = Table(data, colWidths=[column_width] * num_columns)

    style = TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
    ])

    # Aplicamos el estilo a la tabla
    t.setStyle(style)
    t.setStyle(style)
    t.wrapOn(c, 0, 0)
    t.drawOn(c, 30, 600)

    c.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura.pdf"'
    return response


def view_orders_without_reservation(request):
    orders_with_reservation = RestaurantReservation.objects.exclude(order_num_id=None).values_list('order_num_id',
                                                                                                   flat=True)
    orders_without_reservation = Order.objects.exclude(id__in=orders_with_reservation)
    return render(request, 'restaurant/OrdersWithoutRes.html',
                  {'orders_without_reservation': orders_without_reservation})
