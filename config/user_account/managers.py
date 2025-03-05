from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, username, password=None):
        """
        Creates and saves a User with the given phone number, username and password.
        """
        if not phone_number:
            raise ValueError("Users must have an phone number address")
        
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            phone_number=phone_number,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, password=None):
        """
        Creates and saves a superuser with the given phone number, username and password.
        """
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            username=username,
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    