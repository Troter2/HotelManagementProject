from django_cron import CronJobBase, Schedule
from django.utils import timezone
from .models import RoomReservation


class MarcarHabitacionesSuciasCronJob(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'Reception.cron.MarcarHabitacionesSuciasCronJob'

    def do(self):
        cur_date = timezone.now()
        reservations = RoomReservation.objects.filter(guest_checkin__lte=cur_date, guest_checkout__gt=cur_date)
        rooms = [reservation.room_number for reservation in reservations]
        for room in rooms:
            room.is_clean = False
            room.save()