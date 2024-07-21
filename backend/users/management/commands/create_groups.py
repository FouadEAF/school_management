# users/create_groups.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Create custom groups'

    def handle(self, *args, **kwargs):
        groups = ['Administrative', 'Teachers', 'Students']
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Created group: {group_name}'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Group already exists: {group_name}'))
