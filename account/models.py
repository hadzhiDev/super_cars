from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

from utils.models import TimeStampAbstractModel
from account.managers import UserManager


class User(AbstractUser, TimeStampAbstractModel):
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-date_joined',)

    username = models.CharField(max_length=150)
    avatar = ResizedImageField(size=[500, 500], crop=['middle', 'center'], upload_to='avatars/',
                               force_format='WEBP', quality=90, verbose_name='аватарка',
                               null=True, blank=True)
    phone = PhoneNumberField(max_length=100, unique=True, verbose_name='номер телефона', blank=True, null=True)
    email = models.EmailField(verbose_name='электронная почта', unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    get_full_name.fget.short_description = 'полное имя'

    def __str__(self):
        return f'{self.get_full_name or str(self.email)}'


def get_expire_date():
    return timezone.now() + timezone.timedelta(days3)


class UserResetPassword(TimeStampAbstractModel):

    class Meta:
        verbose_name = _('Ключ для сброса пароля')
        verbose_name_plural = _('Ключи для сброса пароля')
        ordering = ('-created_at', '-updated_at')

    user = models.OneToOneField('account.User', on_delete=models.CASCADE, verbose_name=_('пользователь'))
    key = models.UUIDField(_('ключ'), default=uuid4, editable=False)
    expire_date = models.DateTimeField(_('срок действия'), default=get_expire_date)

    def __str__(self):
        return f'{self.user}'

    def is_expired(self):
        return timezone.now() > self.expire_date


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     email_plaintext_message = ("{}?token="
#                                "{}").format(reverse('password_reset:reset-password-'
#                                                     'request'), reset_password_token.key)
#
#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "hadzhi.00703@gmail.com",
#         # to:
#         [reset_password_token.user.email]
#     )
