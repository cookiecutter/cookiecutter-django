from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from {{ cookiecutter.project_slug }}.users.api.views import UserViewSet  # isort:skip
{% if cookiecutter.use_fruit_demo == "y" -%}
from fruit.api.views import FruitViewSet  # isort:skip

{% endif -%}

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
{% if cookiecutter.use_fruit_demo == "y" -%}
router.register("fruits", FruitViewSet)
{%- endif %}

app_name = "api"
urlpatterns = router.urls
