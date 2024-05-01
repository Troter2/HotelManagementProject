from django.core.files.images import ImageFile
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import RoomType, Room


@receiver(post_migrate)
def crear_tipos_habitaciones(sender, **kwargs):
    if sender.name == 'Reception':
        room_types = [
            {"name": "Individual", "description": "Disfruta de la comodidad y la privacidad en nuestra acogedora "
                                                  "habitación individual. Perfecta para viajeros solitarios o aquellos "
                                                  "que buscan un espacio íntimo, esta habitación ofrece todo lo que"
                                                  " necesitas para una estancia confortable. Con una decoración moderna y"
                                                  " funcional, esta habitación cuenta con una cama individual"
                                                  "un baño privado y todas las comodidades necesarias para tu relax,",
             "square_meter": 15, "capacity": 1, "price": 50.00,
             "photo": ImageFile(open("static/img/Single-room.webp", "rb"))},

            {"name": "Doble", "description": "Experimenta el lujo compartido en nuestra amplia habitación doble. "
                                             "Con una decoración elegante y moderna, ofrece una escapada cómoda para"
                                             " dos personas. Disfruta de la intimidad con tu compañero de viaje en un "
                                             "espacio diseñado para relajarse y descansar.",
             "square_meter": 20, "capacity": 2, "price": 80.00,
             "photo": ImageFile(open("static/img/Hab-doble.webp", "rb"))},

            {"name": "Deluxe",
             "description": "Sumérgete en el lujo en nuestra habitación deluxe. Espaciosa y sofisticada,"
                            " ofrece una experiencia de hospedaje excepcional. Disfruta de comodidades"
                            " exclusivas y detalles cuidadosamente seleccionados para una estancia inolvidable.",
             "square_meter": 25, "capacity": 2, "price": 120.00,
             "photo": ImageFile(open("static/img/Hab-DELUXE.jpg", "rb"))},

            {"name": "Suite", "description": "Vive el máximo confort en nuestra lujosa suite. Amplia y elegante, "
                                             "combina espacio y estilo para una experiencia exclusiva. Disfruta de "
                                             "zonas separadas para dormir y relajarte, junto con servicios de "
                                             "primera clase para una estancia inigualable.", "square_meter": 30,
             "capacity": 2,
             "price": 200.00, "photo": ImageFile(open("static/img/SUIT.jpg", "rb"))}
        ]

        for type in room_types:
            RoomType.objects.get_or_create(name=type["name"], defaults=type)


@receiver(post_migrate)
def generate_rooms(sender, **kwargs):
    if sender.name == 'Reception':
        individual = RoomType.objects.get(name='Individual')
        doble = RoomType.objects.get(name='Doble')
        delux = RoomType.objects.get(name='Deluxe')
        suite = RoomType.objects.get(name='Suite')

        individuales = list(range(101, 118)) + list(range(201, 219))
        dobles = list(range(301, 313)) + list(range(401, 414))
        deluxs = list(range(501, 516))
        suites = list(range(601, 606))

        for num in individuales:
            Room.objects.get_or_create(room_type=individual, room_number=str(num))

        for num in dobles:
            Room.objects.get_or_create(room_type=doble, room_number=str(num))

        for num in deluxs:
            Room.objects.get_or_create(room_type=delux, room_number=str(num))

        for num in suites:
            Room.objects.get_or_create(room_type=suite, room_number=str(num))
