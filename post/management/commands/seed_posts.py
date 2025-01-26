from django.core.management.base import BaseCommand
from post.models import Post
from user.models import CustomUser
from faker import Faker

class Command(BaseCommand):
    help = 'Seed posts into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', 
            type=int, 
            default=10, 
            help='Number of posts to create'
        )

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(self.style.SUCCESS(f'Creating {count} posts...'))

        fake = Faker()
        for _ in range(count):
            post = Post.objects.create(
                user=CustomUser.objects.order_by('?')[0],
                content=fake.text(160)
            )
            post.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} posts'))
