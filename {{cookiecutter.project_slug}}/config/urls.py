from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
{% if cookiecutter.js_task_runner == 'CreateReactApp' %}
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt import views as jwt_views
{% endif %}

urlpatterns = [
    {% if cookiecutter.js_task_runner != 'CreateReactApp' %}
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

    # Django Admin, use {% raw %}{% url 'admin:index' %}{% endraw %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('{{ cookiecutter.project_slug }}.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    {% endif %}{% if cookiecutter.js_task_runner == 'CreateReactApp' %}
    url(r'^app/', TemplateView.as_view(template_name="index.html")),

    # REST framework
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # OAUTH2: https://github.com/evonove/django-oauth-toolkit
    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # REST AUTH
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^api-token-auth/', jwt_views.obtain_jwt_token),
    url(r'^api-token-refresh/', jwt_views.refresh_jwt_token),
    url(r'^api-token-verify/', jwt_views.verify_jwt_token),

    # API documentation
    url(r'^docs/', include_docs_urls(title='{{ cookiecutter.project_name }} API')),
    {% endif %}

    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
