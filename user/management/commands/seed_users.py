from django.core.management.base import BaseCommand
from user.models import CustomUser
from faker import Faker

class Command(BaseCommand):
    help = 'Seed users into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', 
            type=int, 
            default=10, 
            help='Number of users to create'
        )

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(self.style.SUCCESS(f'Creating {count} users...'))

        fake = Faker()
        for _ in range(count):
            user = CustomUser.objects.create(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                display_name=fake.name()
            )
            user.set_password(user.password)
            user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} users'))
