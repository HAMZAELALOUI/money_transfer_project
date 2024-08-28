from django.contrib.auth import get_user_model
from django.db import transaction

from wallets.models import Wallet


User = get_user_model()


class UserService:
    @staticmethod
    def create_user(username, email, password, phone_number, user_type):
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone_number=phone_number,
                user_type=user_type,
            )
            Wallet.objects.create(user=user)
        return user

    @staticmethod
    def get_user_by_username(username):
        return User.objects.filter(username=username).first()

    @staticmethod
    def get_user_by_phone(phone_number):
        return User.objects.filter(phone_number=phone_number).first()

    @staticmethod
    def update_user_type(user, new_user_type):
        user.user_type = new_user_type
        user.save()
        return user
