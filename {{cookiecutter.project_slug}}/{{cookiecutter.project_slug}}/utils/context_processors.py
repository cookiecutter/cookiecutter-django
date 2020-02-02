from django.conf import settings


def settings_context(_request):
    return {"settings": settings}
