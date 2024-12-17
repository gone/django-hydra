from allauth.account.forms import LoginForm as AllAuthLoginForm
from allauth.account.forms import SignupForm as AllAuthSignupForm
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import User


class LoginForm(AllAuthLoginForm):
    template_name = "account/login_form.jinja"
    remember = forms.BooleanField(
        help_text=_("For 2 weeks"),
        label=_("Remember Me"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SignupForm(AllAuthSignupForm):
    first_name = forms.CharField(
        label=_("First Name"),
        min_length=1,
        max_length=User._meta.get_field("first_name").max_length,
        widget=forms.TextInput(
            attrs={"placeholder": _("First Name"), "autocomplete": "given-name"}
        ),
    )

    last_name = forms.CharField(
        label=_("Last Name"),
        min_length=1,
        max_length=User._meta.get_field("last_name").max_length,
        widget=forms.TextInput(
            attrs={"placeholder": _("Last Name"), "autocomplete": "family-name"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Email"
        self.fields["email2"].label = "Confirm Email"
        self.fields["password2"].label = "Confirm Password"
