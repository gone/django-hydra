from django_components import Component, register

@register("field")
class Field(Component):
    def get_template_name(self, context):
        field = context.get('field')
        if not field:
            raise RuntimeError(
                f"Component '{self.name}' must be used with a field"
            )
        if field.widget_type == "toggle":
            return "form/toggle.html"
        elif field.widget_type == "checkbox":
            return "form/checkbox.html"
        elif field.widget_type in ["radioselect", "checkboxselectmultiple"]:
            return "form/radio.html"
        elif "file" in field.widget_type:
            return "form/file.html"

        return "form/input.html"

    def get_context_data(self, field, attrs=None):
        attrs = attrs or {}
        attrs['class'] = f"h-full {field.css_classes(extra_classes=attrs.get('class', ''))}".strip() #h-full overridden by user passed attrs


        return {
            'field': field,
            'attrs': attrs,
        }
