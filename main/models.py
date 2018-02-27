import uuid
import datetime

from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class Call(models.Model):
    """Model definition for Call."""

    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    source = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^(\d{2})(\d{8,9})$',
                message='Phone numbers must have 8-9 digits and must be in format AAXXXXXXXXX',
                code='invalid_phone_number'
            ),
        ]
    )
    destination = models.CharField(
        max_length=11,
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
        return str(self.identifier)

    @classmethod
    def get_phone_bill(cls, phone):
        pass

    def start_call(self):
        """Register a call start record."""
        StartRecord.objects.create(call=self)

    def end_call(self):
        """Register a call end record."""
        EndRecord.objects.create(call=self)

    def get_duration_display(self):
        if self.duration:
            secs = round(self.duration.total_seconds())
            hours = int(secs / 3600)
            minutes = int(secs / 60) % 60

            return "{0}h{1}m{2}s".format(hours, minutes, secs)

    @property
    def has_ended(self):
        return hasattr(self, 'ends_at')


class StartRecord(models.Model):
    """Model definition for Start record."""

    call = models.OneToOneField(Call, related_name='starts_at')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Start."""

        verbose_name = 'Start'
        verbose_name_plural = 'Start records'

    def __str__(self):
        """String representation of Start record."""
        return str(self.call.identifier)


class EndRecord(models.Model):
    """Model definition for End record."""

    call = models.OneToOneField(Call, related_name='ends_at')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for End."""

        verbose_name = 'End'
        verbose_name_plural = 'End records'

    def __str__(self):
        """String representation of End record."""
        return str(self.call.identifier)

    def save(self, *args, **kwargs):
        super(EndRecord, self).save(*args, **kwargs)

        if not self.call.duration and not self.call.price:
            self._calculate_call_duration()
            self._calculate_call_price()

    def _calculate_call_duration(self):
        """Calculate a call duration."""
        self.call.duration = self.timestamp - self.call.starts_at.timestamp
        self.call.save()

    def _calculate_call_price(self):
        """Calculte the price of a call record."""
        pass
