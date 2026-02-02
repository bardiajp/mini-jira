import factory
from issues.models import Issue
from accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    full_name = factory.Faker('name')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')


class IssueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Issue

    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text')
    status = factory.Iterator([0, 1, 2])
    priority = factory.Iterator([0, 1, 2])

    assigned_to = factory.SubFactory(UserFactory)