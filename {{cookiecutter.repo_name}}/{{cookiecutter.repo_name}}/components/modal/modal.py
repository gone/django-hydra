from django_components import Component, register

@register("modal")
class Modal(Component):
    template_name = "modal.html"

    def get_context_data(self, button=None, width_class="max-w-xl", open=False):
        return {
            "button": button,
            "width_class": width_class,
            "open": open
        }
