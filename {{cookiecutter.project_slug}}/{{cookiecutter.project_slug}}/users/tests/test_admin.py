from django.urls import reverse

from {{ cookiecutter.project_slug }}.users.models import User


class TestUserAdmin:
    def test_changelist(self, admin_client):
        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_search(self, admin_client):
        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url, data={"q": "test"})
        assert response.status_code == 200

    def test_add(self, admin_client):
        url = reverse("admin:users_user_add")
        response = admin_client.get(url)
        assert response.status_code == 200

        response = admin_client.post(
            url,
            data={
                {%- if cookiecutter.username_type == "email" %}
                "email": "new-admin@example.com",
                {%- else %}
                "username": "test",
                {%- endif %}
                "password1": "My_R@ndom-P@ssw0rd",
                "password2": "My_R@ndom-P@ssw0rd",
            },
        )
        assert response.status_code == 302
        {%- if cookiecutter.username_type == "email" %}
        assert User.objects.filter(email="new-admin@example.com").exists()
        {%- else %}
        assert User.objects.filter(username="test").exists()
        {%- endif %}

    def test_view_user(self, admin_client):
        {%- if cookiecutter.username_type == "email" %}
        user = User.objects.get(email="admin@example.com")
        {%- else %}
        user = User.objects.get(username="admin")
        {%- endif %}
        url = reverse("admin:users_user_change", kwargs={"object_id": user.pk})
        response = admin_client.get(url)
        assert response.status_code == 200
