"""GitHub sign-in through Mockatoo, the mock OAuth provider in local and test settings.

The full sign-in test needs a free Mockatoo test account
(https://app.mockatoo.globalunderdog.com). Set MOCKATOO_TEST_EMAIL and
MOCKATOO_TEST_PASSWORD to run it; it is skipped otherwise.
"""

from __future__ import annotations

import html
import os
import re
from http import HTTPStatus
from typing import TYPE_CHECKING
from urllib.parse import urljoin
from urllib.parse import urlsplit

import pytest
import requests
from django.contrib.auth import get_user
from django.urls import reverse

if TYPE_CHECKING:
    from django.test import Client

MOCKATOO_URL = "https://app.mockatoo.globalunderdog.com"
EMAIL = os.environ.get("MOCKATOO_TEST_EMAIL", "")
PASSWORD = os.environ.get("MOCKATOO_TEST_PASSWORD", "")
TIMEOUT = 30
FORM = re.compile(r'<form method="post" action="([^"]+)">(.*?)</form>', re.DOTALL)
HIDDEN_INPUT = re.compile(r'<input type="hidden" name="([^"]+)" value="([^"]*)"')

pytestmark = pytest.mark.django_db


def test_github_login_redirects_to_mockatoo(client: Client):
    response = client.post(reverse("github_login"))

    assert response.status_code == HTTPStatus.FOUND
    authorize_url = f"{MOCKATOO_URL}/github/login/oauth/authorize?"
    assert response["Location"].startswith(authorize_url)


def submit_form(
    session: requests.Session,
    page: requests.Response,
    **fields: str,
) -> requests.Response:
    """Post the first form on a Mockatoo page, keeping its hidden inputs."""
    form = FORM.search(page.text)
    assert form, f"No form on {page.url}"
    hidden = HIDDEN_INPUT.findall(form.group(2))
    data = {name: html.unescape(value) for name, value in hidden} | fields
    return session.post(
        urljoin(page.url, form.group(1)),
        data=data,
        headers={"Origin": MOCKATOO_URL},
        allow_redirects=False,
        timeout=TIMEOUT,
    )


@pytest.mark.skipif(
    not (EMAIL and PASSWORD),
    reason="Set MOCKATOO_TEST_EMAIL and MOCKATOO_TEST_PASSWORD to run it.",
)
def test_github_sign_in_with_mockatoo(client: Client):
    authorize_url = client.post(reverse("github_login"))["Location"]

    with requests.Session() as mockatoo:
        login_page = mockatoo.get(authorize_url, timeout=TIMEOUT)
        login = submit_form(mockatoo, login_page, email=EMAIL, password=PASSWORD)
        assert login.status_code == HTTPStatus.SEE_OTHER, "Mockatoo login failed"
        consent_url = urljoin(login_page.url, login.headers["Location"])
        consent_page = mockatoo.get(consent_url, timeout=TIMEOUT)
        callback = submit_form(mockatoo, consent_page, decision="approve")

    callback_url = urlsplit(callback.headers["Location"])
    assert callback_url.path == reverse("github_callback")
    client.get(f"{callback_url.path}?{callback_url.query}")

    user = get_user(client)
    assert user.is_authenticated
    assert user.email == EMAIL
