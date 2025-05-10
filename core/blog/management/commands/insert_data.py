from django.core.management.base import BaseCommand
from faker import Faker
from datetime import datetime
from random import choice
from accounts.models.users import User
from accounts.models.profiles import Profile
from ...models import Post, Category

# ======================================================================================================================
category_list = [
    "It",
    "Test",
    "Art",
    "Sport",
]


class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.fake = Faker()

    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        user = User.objects.create_user(email=self.fake.email(), password="m1387m2008m")
        profile = Profile.objects.create(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.designation = self.fake.paragraph(nb_sentences=5)
        profile.save()

        for name in category_list:
            Category.objects.get_or_create(name=name)
        for _ in range(5):
            Post.objects.create(
                author=profile,
                title=self.fake.paragraph(nb_sentences=1),
                content=self.fake.text(),
                status=True,
                category=Category.objects.get(name=choice(category_list)),
                published_date=datetime.now(),
            )
# ======================================================================================================================
