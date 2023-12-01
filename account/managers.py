from django.contrib.auth.models import UserManager as BaseUserManager
# from .models import UserResetPassword, User
from project import settings

from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email must be set'))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


# class UserPasswordResetManager:
#
#     def __init__(self, user: User):
#         self.user = user
#
#     def _get_password_reset(self):
#         return UserResetPassword.objects.get_or_create(user=self.user)[0]
#
#     def _make_link(self, password_reset: UserResetPassword) -> str:
#         host = settings.FRONTEND_HOST
#         link = settings.FRONTED_RESET_PASSWORD_LINK
#         field_name = settings.QUERY_FIELD_NAME_RP
#         # return f'{host}{link}?{urlencode({field_name: password_reset.key})}'
#
#     def send_key(self):
#         password_reset = self._get_password_reset()
#         link = self._make_link(password_reset)
#         subject, from_email, to = 'Hurmma.com | Reset Password', settings.EMAIL_HOST_USER, self.user.email
#         html_message = f'Your link to reset password <a href="{link}">here</a>'
#         # plain_message = strip_tags(html_message)
#         # send_mail(subject, plain_message, from_email, [to], html_message=html_message)
#
#     def reset_password(self, new_password, key):
#         password_reset = self._get_password_reset()
#         if password_reset.key == key:
#             self.user.set_password(new_password)
#             self.user.save()
#             password_reset.delete()
#             return True
#         return False
