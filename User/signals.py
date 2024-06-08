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
        rrhh_user_group, created = Group.objects.get_or_create(name='rrhh')

        # Crear usuarios
        reception_user = CustomUser.objects.create_user(username='reception', password='admin',first_name='reception',email='reception@laspalmeras.es',telefono='123456789')
        waiter_user = CustomUser.objects.create_user(username='waiter', password='admin',first_name='waiter',email='waiter@laspalmeras.es',telefono='123456789')
        cleaner_user = CustomUser.objects.create_user(username='cleaner', password='admin',first_name='cleaner',email='cleaner@laspalmeras.es',telefono='123456789')
        client_user = CustomUser.objects.create_user(username='client', password='admin',first_name='cleaner',email='cleaner@laspalmeras.es',telefono='123456789')
        restaurant_owner_user = CustomUser.objects.create_user(username='restowner', password='admin',first_name='restaurant owner',email='restaurant@owner.es',telefono='123456789')
        accountant_user = CustomUser.objects.create_user(username='accountant', password='admin',first_name='contable',email='contable@laspalmeras.es',telefono='123456789')
        rrhh_user = CustomUser.objects.create_user(username='rrhh', password='admin',first_name='rrhh',email='rrhh@laspalmeras.es',telefono='123456789')

        # Agregar usuarios a grupos
        rrhh_user.groups.add(rrhh_user_group)
        reception_user.groups.add(reception_group)
        waiter_user.groups.add(waiter_group)
        cleaner_user.groups.add(cleaner_group)
        client_user.groups.add(client_group)
        restaurant_owner_user.groups.add(restaurant_owner_group)
        accountant_user.groups.add(accountant_group)

        superuser = CustomUser.objects.create_superuser(username='admin', password='admin',first_name='admin',email='admin@laspalmeras.es',telefono='123456789')
        superuser.groups.add(reception_group, waiter_group, cleaner_group, client_group, restaurant_owner_group,
                             accountant_group,rrhh_user_group)
