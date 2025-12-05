from django.core.management.base import BaseCommand
from accounts.models import LeaveType


class Command(BaseCommand):
    help = 'Create default leave types'

    def handle(self, *args, **kwargs):
        leave_types = [
            {'name': 'Casual Leave', 'default_days': 12, 'description': 'For personal matters'},
            {'name': 'Sick Leave', 'default_days': 10, 'description': 'For medical reasons'},
            {'name': 'Earned Leave', 'default_days': 15, 'description': 'Annual earned leave'},
            {'name': 'Emergency Leave', 'default_days': 5, 'description': 'For emergencies'},
        ]
        
        for lt in leave_types:
            obj, created = LeaveType.objects.get_or_create(
                name=lt['name'],
                defaults={
                    'default_days': lt['default_days'],
                    'description': lt['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {lt["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'→ Already exists: {lt["name"]}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Leave types setup complete!'))
