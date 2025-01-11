from django_components import Component, register


@register("field")
class Field(Component):
    def get_template_name(self, context):
        field = context.get("field")
        if not field:
            raise RuntimeError(f"Component '{self.name}' must be used with a field")
        elif field.widget_type == "checkbox":
            return "form/checkbox.html"
        elif field.widget_type in ["radioselect", "checkboxselectmultiple"]:
            return "form/radio.html"

        return "form/input.html"

    def get_context_data(self, field, attrs=None):
        attrs = attrs or {}
        # defauts overridden by user passed attrs
        attrs["class"] = f"relative h-full {field.css_classes(extra_classes=attrs.get('class', ''))}".strip()
        # checkbox is a little bit of a special snowflakex
        if field.widget_type == "checkbox":
            attrs["class"] += " flex items-start"

        return {
            "field": field,
            "attrs": attrs,
        }
