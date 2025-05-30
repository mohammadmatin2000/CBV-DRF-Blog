from django.core.management.base import BaseCommand  # Importing Django's management command base class
from faker import Faker  # Importing Faker for generating fake data
from datetime import datetime  # Importing datetime for setting publication dates
from random import choice  # Importing choice for selecting random values
from accounts.models.users import User  # Importing the User model
from accounts.models.profiles import Profile  # Importing the Profile model
from ...models import Post, Category  # Importing Post and Category models

# ======================================================================================================================
# List of predefined categories
category_list = [
    "It",
    "Test",
    "Art",
    "Sport",
]

# ======================================================================================================================
# Custom Django Management Command
class Command(BaseCommand):
    """
    Custom Django command to generate fake users, profiles, categories, and posts.
    """

    def __init__(self):
        super(Command, self).__init__()
        self.fake = Faker()  # Initializing the Faker library for generating fake data

    help = "Closes the specified poll for voting"  # Description for the command (not relevant here)

    def handle(self, *args, **options):
        """
        The main execution method for the command.
        """

        # Creating a fake user with a predefined password
        user = User.objects.create_user(email=self.fake.email(), password="m1387m2008m")

        # Creating a profile for the user
        profile = Profile.objects.create(user=user)
        profile.first_name = self.fake.first_name()  # Generating a fake first name
        profile.last_name = self.fake.last_name()  # Generating a fake last name
        profile.designation = self.fake.paragraph(nb_sentences=5)  # Generating a fake description
        profile.save()

        # Creating predefined categories if they don't already exist
        for name in category_list:
            Category.objects.get_or_create(name=name)

        # Generating 5 fake posts
        for _ in range(5):
            Post.objects.create(
                author=profile,  # Assigning the post to the created profile
                title=self.fake.paragraph(nb_sentences=1),  # Generating a fake title
                content=self.fake.text(),  # Generating fake content
                status=True,  # Setting the post as published
                category=Category.objects.get(name=choice(category_list)),  # Assigning a random category
                published_date=datetime.now(),  # Setting the current timestamp as the publication date
            )
# ======================================================================================================================