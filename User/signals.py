from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name == 'User':
        # Crear los grupos si no existen
        Group.objects.get_or_create(name='receptionist')
        Group.objects.get_or_create(name='waiter')
        Group.objects.get_or_create(name='cleaner')
        Group.objects.get_or_create(name='client')
        Group.objects.get_or_create(name='restaurant_owner')
