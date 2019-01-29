from django.conf import settings


def allauth_settings(request):
    # return any necessary values
    return {
        'ACCOUNT_ALLOW_REGISTRATION': settings.ACCOUNT_ALLOW_REGISTRATION
    }
