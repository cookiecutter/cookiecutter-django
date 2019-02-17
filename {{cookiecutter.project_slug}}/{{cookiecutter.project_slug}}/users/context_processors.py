from django.conf import settings


def expose_settings(request):
    # expose any necessary settings
    return {
        'ACCOUNT_HIDE_INTERMEDIARY_LOGOUT': settings.ACCOUNT_HIDE_INTERMEDIARY_LOGOUT
    }
