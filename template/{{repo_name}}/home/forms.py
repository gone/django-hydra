from django import forms
from django.utils.translation import gettext_lazy as _

from {{cookiecutter.project_name}}.util.widgets import ToggleWidget

class TestForm(forms.Form):
    text_input = forms.CharField(
        label=_("Text Input"),
        help_text=_("This is a basic text input field"),
        required=False,
    )

    email_input = forms.EmailField(
        label=_("Email Input"),
        help_text=_("This is an email field"),
        required=False,
    )

    password_input = forms.CharField(
        label=_("Password Input"),
        widget=forms.PasswordInput,
        help_text=_("This is a password field"),
        required=False,
    )

    textarea = forms.CharField(
        label=_("Text Area"),
        widget=forms.Textarea,
        help_text=_("This is a textarea field"),
        required=False,
    )

    select = forms.ChoiceField(
        label=_("Select"),
        choices=[
            ('', 'Select an option'),
            ('1', 'Option 1'),
            ('2', 'Option 2'),
            ('3', 'Option 3'),
        ],
        help_text=_("This is a select field"),
        required=False,
    )

    radio = forms.ChoiceField(
        label=_("Radio"),
        widget=forms.RadioSelect,
        choices=[
            ('1', 'Radio 1'),
            ('2', 'Radio 2'),
            ('3', 'Radio 3'),
        ],
        help_text=_("This is a radio field")
    )

    checkbox = forms.BooleanField(
        label=_("Checkbox"),
        help_text=_("This is a checkbox field")
    )

    toggle = forms.BooleanField(
        label=_("Toggle"),
        required=False,
        widget=ToggleWidget,
        help_text=_("This is a toggle field")
    )

    date = forms.DateField(
        label=_("Date"),
        widget=forms.DateInput,
        help_text=_("This is a date field")
    )

    datetime = forms.DateTimeField(
        label=_("DateTime"),
        widget=forms.DateTimeInput,
        help_text=_("This is a datetime field")
    )
