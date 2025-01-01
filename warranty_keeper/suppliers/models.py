from django.db import models
from django.core.validators import MinLengthValidator

from phonenumber_field.modelfields import PhoneNumberField

from warranty_keeper.core.model_mixins import TimeStampedModel, SoftDeleteMixin


class Supplier(TimeStampedModel, SoftDeleteMixin, models.Model):
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 50

    MAX_PHONE_LENGTH = 15

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(MinLengthValidator(MIN_NAME_LENGTH),),
        unique=True,
        null=False,
        blank=False,
    )

    # TODO: To limit uploads only to png, svc and pictures at all.
    logo = models.ImageField(
        upload_to="logos/",
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )

    phone_number = PhoneNumberField(
        null=True,
        blank=True,
        unique=True,
        help_text="Please enter a valid phone number, including country code.",
    )

    website = models.URLField(
        null=True,
        blank=True,
    )
    
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
