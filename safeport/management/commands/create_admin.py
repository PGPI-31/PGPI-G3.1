from django.core.management.base import BaseCommand
from django.conf import settings
from authentication.models import User

class Command(BaseCommand):
    help = 'Create an admin user if not already created'

    def handle(self, *args, **kwargs):
        email = 'admin@example.com'
        password = 'pgpi1234'

        # Check if a superuser already exists
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                email=email,
                password=password,
                telephone='1234567890',
                address='Admin Address',
                dni='12345678A',
                birthdate='2000-01-01',
            )
            self.stdout.write(self.style.SUCCESS('Admin user created successfully!'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))