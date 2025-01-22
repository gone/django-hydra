from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django_components import Component, register


@register("form")
class FormComponent(Component):
    """Base form component that provides form context to child components"""

    template_name = "form.html"

    def get_context_data(self, form, **kwargs):
        return form.get_context()


@register("field")
class Field(Component):
    default_classes = " relative h-full w-full"

    def get_template_name(self, context):
        field = context.get("field")
        if not field:
            raise RuntimeError(f"Component '{self.name}' must be used with a field")
        elif field.widget_type == "toggle":
            return "form/toggle.html"
        elif field.widget_type == "checkbox":
            return "form/checkbox.html"
        elif field.widget_type in ["radioselect", "checkboxselectmultiple"]:
            return "form/radio.html"

        return "form/input.html"

    def get_context_data(self, field, attrs=None):
        form_ctx = self.inject("form_context")
        if not form_ctx:
            raise RuntimeError("Field component must be used within a form component")

        attrs = attrs or {}
        # defauts overridden by user passed attrs
        attrs["class"] = f"{self.default_classes} {field.css_classes(extra_classes=attrs.get('class', ''))}".strip()
        # checkbox is a little bit of a special snowflake
        if field.widget_type == "checkbox":
            attrs["class"] += " flex items-start"

        if field.widget_type in ["radioselect", "checkboxselectmultiple"]:
            attrs["class"] += " py-4"

        return {
            "form": form_ctx.form,
            "field": field,
            "attrs": attrs,
        }


@register("label")
class Label(Component):
    """
    Label component

    Usage:
    {% component "label" field=field %}
        Label Text
    {% endcomponent %}

    Or with custom classes:
    {% component "label" field=field attrs:class="custom-class" %}
        Label Text
    {% endcomponent %}
    """

    template_name = "form/label.html"

    default_disabled_classes = "translate-y-2 cursor-not-allowed"
    default_readonly_classes = "-translate-y-2 translate-x-2 text-xs bg-white px-1 cursor-not-allowed"
    default_classes = "cursor-text transition"

    def get_context_data(self, field, attrs=None):
        if attrs is None:
            attrs = {}

        # Base classes for different states
        if field.field.disabled:
            classes = self.default_disabled_classes
        elif field.field.widget.attrs.get("readonly"):
            classes = self.default_readonly_classes
        else:
            classes = self.default_classes


        attrs["class"] = f"{classes} {attrs.get('class', '')}".strip()

        attrs["for"] = field.id_for_label

        return {
            "field": field,
            "attrs": attrs,
        }


@register("checkbox_label")
class CheckboxLabel(Label):
    """
    Label component specifically for checkboxes and toggles with different default styling.
    """

    default_disabled_classes = "cursor-not-allowed"
    default_readonly_classes = "cursor-not-allowed"
    default_classes = "text-sm font-medium text-gray-700 leading-none -mt-1"


@register("widget")
class Widget(Component):
    """Renders a widget within a form field context"""

    template = "{{field}}"

    def get_widget_template_name(self, context):
        field = context.get("field")
        if not field:
            raise RuntimeError("Widget component must be used with a field")

        widget = field.field.widget
        template_name = widget.template_name.replace("django/forms/widgets/", "form/widgets/")
        try:
            get_template(template_name)
            return template_name
        except TemplateDoesNotExist:
            return "form/widgets/input.html"

    def get_context_data(self, field, attrs=None, **kwargs):
        # Get the parent form context
        form_ctx = self.inject("form_context")
        if not form_ctx:
            raise RuntimeError("Widget component must be used within a form component")

        context = {
            "field": field,
            **kwargs,
        }
        field.field.widget.template_name = self.get_widget_template_name(context)

        return context


@register("toggle")
class Toggle(Component):
    """
    Toggle switch component using Alpine.js.

    Props:
        name: Input name
        value: Initial toggle state (boolean)
        label: Label text
        disabled: Whether toggle is disabled
        readonly: Whether toggle is readonly
        attrs: Additional HTML attributes
    """

    template_name = "toggle.html"

    # Default classes that can be overridden by subclasses
    default_wrapper_class = "flex items-center justify-center"
    default_label_class = "text-gray-900 font-medium"
    default_switch_wrapper_class = "relative ml-4 inline-flex w-14 rounded-full py-1 transition"
    default_switch_active_color = "bg-slate-400"
    default_switch_inactive_color = "bg-slate-300"
    default_switch_inner_class = "bg-white h-6 w-6 rounded-full transition shadow-md"
    default_inner_active_class = "translate-x-7"
    default_inner_inactive_class = "translate-x-1"

    def get_context_data(
        self,
        name="",
        value=False,
        label="",
        disabled=False,
        readonly=False,
        attrs=None,
    ):
        attrs = attrs or {}
        attrs["class"] = f"{self.default_switch_wrapper_class} {attrs.get('class', '')}".strip()

        return {
            "name": name,
            "value": "true" if value else "false",
            "label": label,
            "label_class": self.default_label_class,
            "switch_wrapper_class": self.default_switch_wrapper_class,
            "switch_active_color": self.default_switch_active_color,
            "switch_inactive_color": self.default_switch_inactive_color,
            "switch_inner_class": self.default_switch_inner_class,
            "inner_active_class": self.default_inner_active_class,
            "inner_inactive_class": self.default_inner_inactive_class,
            "disabled": disabled,
            "readonly": readonly,
            "noedit": disabled or readonly,
            "attrs": attrs,
        }


@register("flatpickr")
class Flatpickr(Component):
    """
    Flatpickr date/time picker component.

    Usage:
        {% component "flatpickr" type="date" name="my_date" value=value %}{% endcomponent %}
        {% component "flatpickr" type="datetime" name="my_datetime" value=value %}{% endcomponent %}

    Props:
        type: "date" or "datetime" (default: "date")
        name: field name
        value: initial value
        attrs: additional HTML attributes
        disabled: whether the field is disabled
        readonly: whether the field is readonly
    """

    template_name = "flatpickr.html"
    default_wrapper_classes = "w-full input"
    default_input_classes = "w-full rounded-md border border-gray-200 px-3 py-2.5"

    def get_context_data(self, type="date", value=None, id=None, attrs=None, input=None):
        if attrs is None:
            attrs = {}
        if input is None:
            input = {}

        enable_time = type == "datetime"
        if enable_time:
            input["x-mask"] = "99/99/9999 99:99"
            input.setdefault("placeholder", "MM/DD/YYYY HH:ii")
        else:
            input["x-mask"] = "99/99/9999"
            input.setdefault("placeholder", "MM/DD/YYYY")

        attrs["class"] = f"{self.default_wrapper_classes} {attrs.get('class', '')}".strip()
        if value:
            attrs["class"] += " has-focus"

        input["value"] = value
        input["class"] = f"{self.default_input_classes} {input.get('class', '')}".strip()

        event_name = f"update-{id.replace('_', '-')}" if id else ""
        return {
            "type": type,
            "value": value,
            "attrs": attrs,
            "input": input,
            "enable_time": enable_time,
            "event_name": event_name,
        }
