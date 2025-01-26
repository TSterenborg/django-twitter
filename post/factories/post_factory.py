import factory
from faker import Faker
from post.models import Post
from user.models import CustomUser

fake = Faker()

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
    
    user = factory.LazyAttribute(lambda _: CustomUser.objects.order_by('?')[0])
    content = factory.LazyAttribute(lambda _: fake.text(160))
    