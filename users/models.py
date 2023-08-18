
import hashlib
import time

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import NotAcceptable


class CustomUser(AbstractUser):
    username = None
    phone_number = PhoneNumberField(unique=True)
    security_code = models.CharField(max_length=4)
    is_verified = models.BooleanField(default=False)
    invitation_code = models.CharField(max_length=6)
    invited_by_code = models.CharField(max_length=6)
    invited_by = models.ForeignKey('self',
                                   to_field='phone_number',
                                   on_delete=models.SET_DEFAULT,
                                   default=None, null=True)
    invitations_by_user = models.ManyToManyField('self')

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.phone_number.as_e164

    def generate_referral_code(self):
        """
        This function generates a referral code by hashing
        entered phone number with a length of 6 symbols
        """
        self.invitation_code = hashlib.shake_128(str(self.phone_number)
                                                 .encode("utf-8")).hexdigest(3)
        return self.invitation_code

    def generate_security_code(self):
        """
        Returns a unique random `security_code` for given
        `TOKEN_LENGTH` in the settings.
        Default token length = 4
        """
        token_length = getattr(settings, 'TOKEN_LENGTH', 4)
        self.security_code = get_random_string(token_length, allowed_chars='0123456789')
        return self.security_code

    def send_confirmation(self):
        """
        Emulate the sms code sending
        """
        time.sleep(2)
        self.security_code = self.generate_security_code()
        return print(f'Your confirmation code is {self.security_code}')

    def check_verification(self, security_code):
        if (
            security_code == self.security_code and not self.is_verified
        ):
            self.is_verified = True
            self.save()
        else:
            raise NotAcceptable(
                _('Your security code is wrong, expired or this phone is verified before.'))

        return self.is_verified
