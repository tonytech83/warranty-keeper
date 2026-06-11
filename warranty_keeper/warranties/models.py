from dateutil.relativedelta import relativedelta

from django.db import models
from django.utils.timezone import now

from django.core.validators import MinLengthValidator

from warranty_keeper.core.model_mixins import TimeStampedModel, SoftDeleteMixin
from warranty_keeper.suppliers.models import Supplier


class Period(models.IntegerChoices):
    ONE_MONTH = 1, "1 Month"
    THREE_MONTHS = 3, "3 Months"
    SIX_MONTHS = 6, "6 Months"
    NINE_MONTHS = 9, "9 Months"
    TWELVE_MONTHS = 12, "12 Months"
    TWENTY_FOUR_MONTHS = 24, "24 Months"
    THIRTY_SIX_MONTHS = 36, "36 Months"


class Warranty(TimeStampedModel, SoftDeleteMixin, models.Model):
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

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Purchase price of the item.",
    )

    invoice_img = models.FileField(
        upload_to="invoices/",
        null=True,
        blank=True,
    )

    deleted = models.BooleanField(default=False)

    supplier = models.ForeignKey(
        to=Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    @property
    def warranty_expiration_date(self):
        """Returns the accurate date on which the warranty will expire."""
        return self.purchase_date + relativedelta(months=self.period)

    @property
    def days_before_expiration(self):
        """Returns the number of days before the warranty expires."""
        expiration_date = self.warranty_expiration_date
        return (
            (expiration_date - now().date()).days
            if expiration_date > now().date()
            else 0
        )

    @property
    def is_expired(self):
        """True when the warranty period has already ended."""
        return self.warranty_expiration_date < now().date()
