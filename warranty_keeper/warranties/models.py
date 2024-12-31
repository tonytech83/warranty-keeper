from django.db import models

from django.core.validators import MinLengthValidator


from warranty_keeper.suppliers.models import Supplier


class Period(models.IntegerChoices):
    ONE_MONTH = 1, "1 Month"
    THREE_MONTHS = 3, "3 Months"
    SIX_MONTHS = 6, "6 Months"
    NINE_MONTHS = 9, "9 Months"
    TWELVE_MONTHS = 12, "12 Months"
    TWENTY_FOUR_MONTHS = 24, "24 Months"
    THIRTY_SIX_MONTHS = 36, "36 Months"


class Warranty(models.Model):
    MAX_NAME_LENGTH = 100
    MIN_NAME_LENGTH = 2

    item_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(MinLengthValidator(MIN_NAME_LENGTH),),
        unique=False,
        null=False,
        blank=False,
    )

    purchase_date = models.DateField(
        null=False,
        blank=False,
    )

    period = models.IntegerField(
        choices=Period.choices,
        default=Period.TWENTY_FOUR_MONTHS,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    invoice_img = models.FileField(
        upload_to="invoices/",
        null=True,
        blank=True,
    )

    supplier = models.ForeignKey(
        to=Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
