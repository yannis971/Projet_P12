from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime

@deconstructible
class DateTimeValidator:
    """Validate that the datetime is valid."""
    message = _('datetime field is not valid')
    code = 'Allowed datime is timezone or datetime'
    tz_now = timezone.now()

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if not isinstance(value, datetime):
            raise ValidationError(self.message, code=self.code, params={'value': value})


