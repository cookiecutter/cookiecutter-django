from django.urls import path

from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    {%- if cookiecutter.username_type == "email" %}
    path("<int:pk>/", view=user_detail_view, name="detail"),
    {%- else %}
    path("<str:username>/", view=user_detail_view, name="detail"),
    {%- endif %}
]
