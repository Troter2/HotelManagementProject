
from django.core.management import BaseCommand
from django.utils import timezone

from Reception.models import RoomReservation
import smtplib
from email.mime.text import MIMEText

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


    def handle(self, *args, **options):
        subject = "Email Subject"
        body = "This is the body of the text message"
        sender = "hotellaspalmeras07@gmail.com"
        recipients = ["sergivilamonguia@gmail.com"]
        password = ".abcd1234"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")
