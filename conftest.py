from typing import TYPE_CHECKING

import pytest
from rest_framework.test import APIClient

from mad.app.services import generate_access_token
from mad.app.tests.factories import UserFactory

if TYPE_CHECKING:
    from django.contrib.auth.models import User


pytest.register_assert_rewrite(
    "app.tests.asserts",
)


class AuthAPIClient(APIClient):
    user: "User"


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def auth_api_client() -> AuthAPIClient:
    user = UserFactory()
    client = AuthAPIClient()
    client.user = user
    client.defaults.update({"HTTP_AUTHORIZATION": generate_access_token(user.id)})
    return client
