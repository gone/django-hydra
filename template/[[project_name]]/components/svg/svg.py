from django_components import Component, register


@register("svg")
class Svg(Component):
    def get_template_name(self, context):
        return f"svg/{context['name']}.svg"

    def get_context_data(self, name, size="5"):
        return {
            "name": name.lower(),
            "size": size,
        }
