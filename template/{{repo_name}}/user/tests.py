# pylint: disable=redefined-outer-name
import uuid
from http import HTTPStatus

import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from model_bakery import baker
from playwright.sync_api import Page, expect
from pytest_django.asserts import assertRedirects

from .models import User


@pytest.fixture
def password():
    """Generate a unique password string.

    Can be referenced by tests also. For instance, we create a super user, then log in that
    super user using the data from this password fixture.
    """
    return uuid.uuid4().hex


@pytest.fixture
def super_user(password) -> User:
    return baker.make_recipe(
        "{{cookiecutter.project_name}}.user.user",
        is_superuser=True,
        is_staff=True,
        password=make_password(password),
    )


@pytest.fixture
def form_data(password) -> dict:
    return {
        "email": "ben@coolguy.com",
        "email2": "ben@coolguy.com",
        "password1": password,
        "password2": password,
        "first_name": "ben",
        "last_name": "beecher",
    }


@pytest.mark.django_db
def test_create_user(password):
    user = User.objects.create_user(  # noqa: S106
        "jonnyrico@fednet.gov",
        password=password,
    )  # nosec
    User.objects.get(id=user.id)


@pytest.mark.integration
def test_login_live(page: Page, live_server, super_user, password):
    header = page.locator("h2")

    page.goto(f"{live_server.url}{reverse('account_login')}")
    expect(header).to_have_text("Sign In")

    page.fill("input[name=login]", super_user.email)
    page.fill("input[name=password]", password)
    page.click("button[type=submit]")
    expect(page).to_have_url(f"{live_server.url}/")


@pytest.mark.integration
def test_login_redirection_live(page: Page, live_server, super_user, password):
    header = page.locator("h2")

    page.goto(f"{live_server.url}{reverse('account_login')}?next=/admin/")
    expect(header).to_have_text("Sign In")

    page.fill("input[name=login]", super_user.email)
    page.fill("input[name=password]", password)
    page.click("button[type=submit]")
    expect(page).to_have_url(f"{live_server.url}/admin/")


@pytest.mark.integration
def test_login_no_password_live(page: Page, live_server, super_user):
    header = page.locator("h2")

    page.goto(f"{live_server.url}{reverse('account_login')}")
    expect(header).to_have_text("Sign In")
    page.fill("input[name=login]", super_user.email)
    page.click("button[type=submit]")
    expect(page.locator("input[name=password]")).to_be_focused()


@pytest.mark.integration
def test_login_email_case_insensitive_live(page: Page, live_server, super_user, password):
    header = page.locator("h2")

    page.goto(f"{live_server.url}{reverse('account_login')}")
    expect(header).to_have_text("Sign In")
    page.fill("input[name=login]", super_user.email.upper())
    page.fill("input[name=password]", password)
    page.click("button[type=submit]")
    expect(page).to_have_url(f"{live_server.url}/")


@pytest.mark.integration
def test_login_badpass_live(page: Page, live_server, super_user):
    header = page.locator("h2")

    page.goto(f"{live_server.url}{reverse('account_login')}")
    expect(header).to_have_text("Sign In")
    page.fill("input[name=login]", super_user.email.upper())
    page.fill("input[name=password]", "BUGSRULE")
    page.click("button[type=submit]")

    expect(page.locator(".errorlist")).to_contain_text(
        "The e-mail address and/or password you specified are not correct.",
    )


@pytest.mark.django_db
def test_register(client, form_data):
    user_password = form_data["password1"]

    assert User.objects.count() == 0

    response = client.post(reverse("account_signup"), form_data, follow=True)
    assertRedirects(response, "/")

    assert User.objects.count() == 1

    user = User.objects.first()
    assert user.check_password(user_password)


@pytest.mark.django_db
def test_register_bad_repeat_email(client, form_data):
    email = form_data["email"]
    baker.make(User, email=email)
    url = reverse("account_signup")

    assert User.objects.count() == 1

    response = client.post(url, form_data)
    assert response.status_code == HTTPStatus.OK
    assert User.objects.count() == 1

    form_data["email"] = email.upper()
    response = client.post(url, form_data)
    assert response.status_code == HTTPStatus.OK
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_register_bad_repeat_pass1(client, form_data):
    form_data["password1"] = "oh no, oh no"

    response = client.post(reverse("account_signup"), form_data)
    assert response.status_code == HTTPStatus.OK
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_bad_repeat_pass2(client, form_data):
    form_data["password2"] = "oh no, oh no"

    response = client.post(reverse("account_signup"), form_data)
    assert response.status_code == HTTPStatus.OK
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_no_repeat_pass(client, form_data):
    del form_data["password2"]

    response = client.post(reverse("account_signup"), form_data)
    assert response.status_code == HTTPStatus.OK
    assert User.objects.count() == 0


@pytest.mark.integration
def test_register_live(page: Page, live_server, form_data):
    header = page.locator("h2")

    page.goto(f"{live_server.url}{reverse('account_signup')}")
    expect(header).to_have_text("Register")

    page.fill('input[name="email"]', form_data["email"])

    page.fill('input[placeholder="E-mail address confirmation"]', form_data["email2"])
    page.fill('input[placeholder="First Name"]', form_data["first_name"])
    page.fill('input[placeholder="Last Name"]', form_data["last_name"])
    page.fill('input[placeholder="Password"]', form_data["password1"])
    page.fill('input[placeholder="Password (again)"]', form_data["password2"])
    page.click("text=Create Account")

    expect(page).to_have_url(f"{live_server.url}/")


@pytest.mark.integration
def test_register_bad_repeat_email_live(page: Page, live_server, form_data):
    header = page.locator("h2")

    page.goto(f"{live_server.url}{reverse('account_signup')}")
    expect(header).to_have_text("Register")

    page.fill('input[name="email"]', form_data["email"])

    page.fill('input[placeholder="E-mail address confirmation"]', "email@bademail.com")
    page.fill('input[placeholder="First Name"]', form_data["first_name"])
    page.fill('input[placeholder="Last Name"]', form_data["last_name"])
    page.fill('input[placeholder="Password"]', form_data["password1"])
    page.fill('input[placeholder="Password (again)"]', form_data["password2"])
    page.click("text=Create Account")

    expect(page.locator(".errorlist")).to_contain_text(
        "You must type the same email each time.",
    )


@pytest.mark.integration
def test_register_bad_repeat_pass1_live(page: Page, live_server, form_data):
    header = page.locator("h2")

    page.goto(f"{live_server.url}{reverse('account_signup')}")
    expect(header).to_have_text("Register")

    page.fill('input[name="email"]', form_data["email"])
    page.fill('input[placeholder="E-mail address confirmation"]', form_data["email2"])
    page.fill('input[placeholder="First Name"]', form_data["first_name"])
    page.fill('input[placeholder="Last Name"]', form_data["last_name"])
    page.fill('input[placeholder="Password"]', form_data["password1"])
    page.fill('input[placeholder="Password (again)"]', "somethingwronggarbage")
    page.click("text=Create Account")

    expect(page.locator(".errorlist")).to_contain_text(
        "You must type the same password each time.",
    )


@pytest.mark.django_db
def test_user_admin_list(client, super_user, password):
    client.login(
        username=super_user.email,
        password=password,
    )

    response = client.get(reverse("admin:user_user_changelist"))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_user_admin_detail(client, super_user, password):
    client.login(
        username=super_user.email,
        password=password,
    )

    response = client.get(reverse("admin:user_user_change", args=[super_user.id]))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_user_admin_add(client, super_user, password):
    client.login(
        username=super_user.email,
        password=password,
    )

    email = "robertcop@ocp.com"
    actual = client.post(
        reverse("admin:user_user_add"),
        {
            "email": email,
            "password1": "deadoraliveyourecomingwithme",
            "password2": "deadoraliveyourecomingwithme",
        },
    )

    new_user = User.objects.latest("created")
    assert new_user.email == email

    expected = reverse("admin:user_user_change", args=[new_user.id])
    assertRedirects(actual, expected)


@pytest.mark.django_db
def test_user_admin_add_different_passwords(client, super_user, password):
    client.login(
        username=super_user.email,
        password=password,
    )

    response = client.post(
        reverse("admin:user_user_add"),
        {
            "email": "robertcop@ocp.com",
            "password1": "deadoraliveyourecomingwithme",
            "password2": "freezecreep",
        },
    )

    expected = {"password2": ["The two password fields didn’t match."]}
    assert response.context["adminform"].form.errors == expected


@pytest.mark.django_db
def test_user_admin_change(client, super_user, password):
    client.login(
        username=super_user.email,
        password=password,
    )

    actual = client.post(
        reverse("admin:user_user_change", args=[super_user.id]),
        {
            "email": "ben@coolguy.com",
            "last_login_0": "2015-05-20",
            "last_login_1": "03:38:28",
        },
    )
    expected = reverse("admin:user_user_changelist")
    assertRedirects(actual, expected, target_status_code=HTTPStatus.FOUND)
