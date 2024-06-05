
from django.core.management import BaseCommand
from django.utils import timezone

from Reception.models import RoomReservation


class Command(BaseCommand):
    help = "Set rooms to not clean if occupied."

    def handle(self, *args, **options):
        cur_date = timezone.now()
        reservations = RoomReservation.objects.filter(guest_checkin__lte=cur_date, guest_checkout__gt=cur_date)
        rooms = [reservation.room_number for reservation in reservations]
        for room in rooms:
            room.is_clean = False
            room.save()
        self.stdout.write(self.style.SUCCESS('Successfully set rooms to not clean'))
