from django import template
from django.utils import timezone
from django.utils.formats import date_format

register = template.Library()

@register.filter(name='localize_datetime')
def localize_datetime(value):
    """
    Convert datetime to local timezone and format it
    """
    if value:
        # Convert to local timezone
        local_dt = timezone.localtime(value)
        # Format the datetime
        return date_format(local_dt, format='SHORT_DATETIME_FORMAT', use_l10n=True)
    return '' 