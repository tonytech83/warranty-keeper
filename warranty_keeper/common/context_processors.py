from django.conf import settings


def app_settings(request):
    """Expose selected settings to every template."""
    return {
        "CURRENCY": settings.CURRENCY,
    }
