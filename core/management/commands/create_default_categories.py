from django.core.management.base import BaseCommand
from core.models import Category

class Command(BaseCommand):
    help = 'Create default categories for the suggestion box'

    def handle(self, *args, **options):
        default_categories = [
            'Canteen & Food Services',
            'Library & Study Spaces',
            'Classroom & Academic',
            'Transportation & Parking',
            'Technology & IT Support',
            'Facilities & Maintenance',
            'Student Life & Activities',
            'Administrative Services',
            'Health & Wellness',
            'Other'
        ]

        created_count = 0
        for category_name in default_categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new categories')
        ) 