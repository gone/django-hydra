from django_components import Component, register


@register("popover")
class Popover(Component):
    """
    Base popover component using Alpine.js UI.

    Template slots:
        - trigger: Content for the button that triggers the popover
        - content: Content displayed in the popover panel

    Context variables:
        - wrapper_class: Classes for the wrapper div (default: 'relative')
        - button_class: Classes for the trigger button
        - panel_class: Classes for the popover panel
    """

    template_name = "popover.html"

    def get_context_data(self, **kwargs):
        return kwargs
