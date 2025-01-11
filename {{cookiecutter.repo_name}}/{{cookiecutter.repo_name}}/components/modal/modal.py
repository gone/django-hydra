from django_components import Component, register

@register("modal")
class Modal(Component):
    template_name = "modal.html"

    def get_context_data(self, open=False):
        return {
            "open": open
        }