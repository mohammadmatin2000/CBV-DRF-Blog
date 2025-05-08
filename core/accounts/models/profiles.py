from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from .users import User


# ======================================================================================================================
# Profile Model linked to User Model via ForeignKey
class Profile(models.Model):
    """
    Profile model that stores additional user details.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Establishes relationship with User
    first_name = models.CharField(
        max_length=255
    )  # First name of the user
    last_name = models.CharField(
        max_length=255
    )  # Last name of the user
    image = models.ImageField(
        blank=True, null=True
    )  # Optional profile picture field
    designation = models.CharField(
        max_length=255
    )  # Job title or role
    created_date = models.DateTimeField(
        auto_now_add=True
    )  # Automatically sets profile creation time
    updated_date = models.DateTimeField(
        auto_now=True
    )  # Updates timestamp when modified

    def __str__(self):
        return self.user.email  # Returns the associated user's email


# ======================================================================================================================
# Signal to automatically create a Profile instance whenever a new User is created
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:  # If a new user is created
        Profile.objects.create(
            user=instance
        )  # Create a profile linked to the user


# ======================================================================================================================
