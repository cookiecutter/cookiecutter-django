from django.urls import path

from {{ cookiecutter.project_slug }}.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    GoogleLogin
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),

]
