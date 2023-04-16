from django.urls import path

from {{ cookiecutter.project_slug }}.users.views import (
    user_redirect_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),

]
