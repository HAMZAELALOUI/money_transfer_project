from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.models import BaseModel


class User(AbstractUser, BaseModel):
    phone_number = models.CharField(max_length=20)
    user_type = models.CharField(
        max_length=20,
        choices=[
            ("SENDER", "Sender"),
            ("RECEIVER", "Receiver"),
            ("AGENT", "Agent"),
        ],
    )

    def __str__(self):
        return self.username
