from django.core.management.base import BaseCommand
from django.utils import timezone

from Reception.models import RoomReservation


class Command(BaseCommand):
    help = 'Deletes room reservations older than 2 years'

    def handle(self, *args, **kwargs):
        two_years_ago = timezone.now() - timezone.timedelta(days=365 * 2)
        old_reservations = RoomReservation.objects.filter(guest_checkout__lt=two_years_ago)
        old_reservations.delete()
        self.stdout.write(self.style.SUCCESS('Deleted room reservations where checkout date is older than 2 years.'))