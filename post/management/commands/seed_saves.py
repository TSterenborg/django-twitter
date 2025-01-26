from django.core.management.base import BaseCommand
from post.models import Post, Save
from user.models import CustomUser
from faker import Faker

class Command(BaseCommand):
    help = 'Seed saves into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', 
            type=int, 
            default=10, 
            help='Number likes saves to create'
        )

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(self.style.SUCCESS(f'Creating {count} saves...'))

        fake = Faker()
        for _ in range(count):
            
            try:
                save = Save.objects.create(
                    user=CustomUser.objects.order_by('?')[0],
                    post=Post.objects.order_by('?')[0]
                    )

                save.save()
                
            except:
                print(":(")

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} save'))
