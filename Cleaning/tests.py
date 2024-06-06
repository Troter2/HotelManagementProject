from django.test import TestCase
from django.urls import reverse
from Reception.models import Room,RoomType


class CleanerViewsTestCase(TestCase):
    def setUp(self):
        # Creamos algunas habitaciones para usar en las pruebas
        self.roomType = RoomType.objects.create(name='indiv', capacity=2, description='abc', square_meter=8, price=30)
        self.room1 = Room.objects.create(room_type= self.roomType,room_number='101', is_clean=True)
        self.room2 = Room.objects.create(room_type= self.roomType,room_number='102', is_clean=False)

    def test_update_room_status_view(self):
        self.assertFalse(self.room2.is_clean)
        # Probamos la vista update_room_status enviando una solicitud POST para marcar una habitación como limpia
        response = self.client.post(reverse('update_room_status'), data={'room_id': self.room2.id, 'action': 'clean'})
        self.assertEqual(response.status_code, 302)  # Redirección después de la actualización
        self.room2.refresh_from_db()  # Actualizamos el objeto desde la base de datos
        self.assertTrue(self.room2.is_clean)  # Verificamos que la habitación ahora esté limpia



