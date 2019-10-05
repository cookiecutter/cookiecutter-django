from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views import defaults as default_views

from graphene_file_upload.django import FileUploadGraphQLView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)


urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    re_path(r'^app/(?P<route>.*)$', TemplateView.as_view(template_name="index.html"), name='app'),

    # APIs
    path("api/", include(router.urls)),
    path("api-docs/", include_docs_urls(title="{{ cookiecutter.project_name }} REST API", public=False)),
    path("graphql/", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, pretty=True))),

    # User management from django-all-auth
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("users/", include("{{ cookiecutter.project_slug }}.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),

    # Django Admin, use {% raw %}{% url 'admin:index' %}{% endraw %}
    path(settings.ADMIN_URL, admin.site.urls),

    # Your stuff: custom urls includes go here

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
