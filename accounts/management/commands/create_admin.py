from django.core.management.base import BaseCommand
from accounts.models import User
import os


class Command(BaseCommand):
    help = 'Create admin user from environment variables'

    def handle(self, *args, **kwargs):
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@leaveflow.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        if User.objects.filter(email=admin_email).exists():
            self.stdout.write(self.style.WARNING(f'→ Admin user already exists: {admin_email}'))
            return
        
        User.objects.create_superuser(
            email=admin_email,
            password=admin_password,
            full_name='Admin User',
            role='admin'
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Admin user created: {admin_email}'))
        self.stdout.write(self.style.SUCCESS(f'  Password: {admin_password}'))
