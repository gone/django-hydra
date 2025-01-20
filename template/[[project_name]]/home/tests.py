from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home(client):
    response = client.get(reverse("home"))

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_error_route(client):
    with pytest.raises(Exception, match="Make response code 500!"):
        client.get(reverse("error"))
