from django.conf import settings


def settings_context(_request):
    # Be explicit
    return {"DEBUG": settings.DEBUG}
