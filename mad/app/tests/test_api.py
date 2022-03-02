import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from mad.app.exceptions import INCORRECT_LOGIN_OR_PASSWORD, USER_IS_NOT_ACTIVE
from mad.app.tests.asserts import PatientSerializerChecker
from mad.app.tests.factories import UserFactory, PatientFactory, DiagnoseFactory


@pytest.mark.django_db
class TestLoginViaUsernameAndPasswordAPI:
    url = reverse("app:login")

    def test_required_fields(self, api_client: APIClient):
        request_body = {}

        response = api_client.post(self.url, request_body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["username"]
        assert response.data["password"]
        assert set(response.data.keys()) == {"username", "password"}

    def test_should_raise_400_if_username_is_invalid(self, api_client: APIClient):
        request_body = {"username": "invalid", "password": "maybe_correct"}

        response = api_client.post(self.url, request_body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["code"] == INCORRECT_LOGIN_OR_PASSWORD

    def test_should_raise_400_if_password_is_invalid(self, api_client: APIClient):
        user = UserFactory()
        request_body = {"username": user.username, "password": "invalid"}

        response = api_client.post(self.url, request_body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["code"] == INCORRECT_LOGIN_OR_PASSWORD

    def test_should_raise_403_if_user_is_not_active(self, api_client: APIClient):
        user = UserFactory(is_active=False)
        request_body = {"username": user.username, "password": "admin"}

        response = api_client.post(self.url, request_body)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["code"] == USER_IS_NOT_ACTIVE

    def test_should_return_access_token(self, api_client: APIClient):
        user = UserFactory()
        request_body = {"username": user.username, "password": "admin"}

        response = api_client.post(self.url, request_body)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["token"]


@pytest.mark.django_db
class TestPatientListAPI:
    url = reverse("app:patients")

    def test_should_raise_403_if_user_is_not_provided_auth_token(self, api_client: APIClient):
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["code"] == "not_authenticated"

    def test_should_return_last_three_patients(self, auth_api_client: APIClient):
        diagnoses = DiagnoseFactory.create_batch(3)
        patients = PatientFactory.create_batch(4, diagnoses=diagnoses)
        patients = reversed(patients)

        response = auth_api_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        PatientSerializerChecker.assert_equal_list(response.data, list(patients)[:3])
