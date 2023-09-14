from django.contrib.auth.models import Group


def create_groups():
    admin_group, created = Group.objects.get_or_create(name='Admins')
    manager_group, created = Group.objects.get_or_create(name='Managers')
    salerep_group, created = Group.objects.get_or_create(name='Salereps')

