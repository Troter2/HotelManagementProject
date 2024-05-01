from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from accounts.models import CustomUser

@receiver(post_migrate)
def create_groups_and_users(sender, **kwargs):
    if sender.name == 'django.contrib.auth':
        CustomUser = get_user_model()

        # Crear los grupos si no existen
        reception_group, created = Group.objects.get_or_create(name='receptionist')
        waiter_group, created = Group.objects.get_or_create(name='waiter')
        cleaner_group, created = Group.objects.get_or_create(name='cleaner')
        client_group, created = Group.objects.get_or_create(name='client')
        restaurant_owner_group, created = Group.objects.get_or_create(name='restaurant_owner')
        accountant_group, created = Group.objects.get_or_create(name='accountant')

        # Crear usuarios
        reception_user = CustomUser.objects.create_user(username='receptionuser', password='admin')
        waiter_user = CustomUser.objects.create_user(username='waiteruser', password='admin')
        cleaner_user = CustomUser.objects.create_user(username='cleaneruser', password='admin')
        client_user = CustomUser.objects.create_user(username='clientuser', password='admin')
        restaurant_owner_user = CustomUser.objects.create_user(username='restowneruser', password='admin')
        accountant_user = CustomUser.objects.create_user(username='accountantuser', password='admin')

        # Agregar usuarios a grupos
        reception_user.groups.add(reception_group)
        waiter_user.groups.add(waiter_group)
        cleaner_user.groups.add(cleaner_group)
        client_user.groups.add(client_group)
        restaurant_owner_user.groups.add(restaurant_owner_group)
        accountant_user.groups.add(accountant_group)

        superuser = CustomUser.objects.create_superuser(username='admin', password='admin')
        superuser.groups.add(reception_group, waiter_group, cleaner_group, client_group, restaurant_owner_group,
                             accountant_group)
