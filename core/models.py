from django.db import models


class UserData(models.Model):
    """
    Model for storing user data from Telegram.

    This model keeps track of users interacting with the system
    through Telegram, identified by their usernames.
    """

    telegram_username = models.CharField(max_length=50)

    def __str__(self):
        """String representation of the UserData object."""
        return self.telegram_username
