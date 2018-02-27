import uuid
import datetime

from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class Call(models.Model):
    """Model definition for Call."""

    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    source = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^(\d{2})(\d{8,9})$',
                message='Phone numbers must have 8-9 digits and must be in format AAXXXXXXXXX',
                code='invalid_phone_number'
            ),
        ]
    )
    destination = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^(\d{2})(\d{8,9})$',
                message='Phone numbers must have 8-9 digits and must be in format AAXXXXXXXXX',
                code='invalid_phone_number'
            ),
        ]
    )
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    duration = models.DurationField(default=datetime.timedelta(minutes=0))

    class Meta:
        """Meta definition for Call."""

        verbose_name = 'Call'
        verbose_name_plural = 'Calls'

    def __str__(self):
        """str representation of Call."""
        pass

    @classmethod
    def get_phone_bill(cls, phone):
        pass

    @property
    def has_ended(self):
        return self.ends_at.exists()


class Start(models.Model):
    """Model definition for Start record."""

    call = models.OneToOneField(Call, related_name='starts_at')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Start."""

        verbose_name = 'Start'
        verbose_name_plural = 'Start records'

    def __str__(self):
        """String representation of Start record."""
        pass


class End(models.Model):
    """Model definition for End record."""

    call = models.OneToOneField(Call, related_name='ends_at')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for End."""

        verbose_name = 'End'
        verbose_name_plural = 'End records'

    def __str__(self):
        """String representation of End record."""
        pass

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            self._calculate_call_duration()
            self._calculate_call_cost()

        return super(End, self).save(*args, **kwargs)

    def _calculate_call_duration(self):
        """Calculate a call duration."""
        pass

    def _calculate_call_cost(self):
        """Calculte the cost of a call record."""
        pass
