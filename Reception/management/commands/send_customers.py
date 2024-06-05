import json
from django.core.management import BaseCommand
from django.utils import timezone

from Reception.models import RoomReservation
from User.models import Customer


class Command(BaseCommand):
    help = "Send customers to police."

    def handle(self, *args, **options):
        cur_date = timezone.now()
        reservations = RoomReservation.objects.filter(guest_checkin__lte=cur_date, guest_checkout__gt=cur_date)
        customers = Customer.objects.filter(reservation__in=reservations)
        dni = [customer.DNI for customer in customers]
        dni_json = json.dumps(dni)


        self.stdout.write(self.style.SUCCESS(dni_json))
        self.stdout.write(self.style.SUCCESS('Successfully sent customers'))
