from django_components import Component, register


@register("alert")
class Alert(Component):
    """An alert component that works with Django's messages framework.

    Usage:
    {% component "alert" message=message %}{% endcomponent %}
    """

    template_name = "alert.html"

    level_icons = {
        "error": "exclamation-circle",
        "warning": "exclamation-triangle",
        "success": "check-circle",
        "info": "information-circle",
        "debug": "information-circle",
    }

    level_classes = {
        "debug": "bg-info/5 text-info border border-info/10 ring-1 ring-info/10",
        "info": "bg-info/5 text-info border border-info/10 ring-1 ring-info/10",
        "success": "bg-success/5 text-success border border-success/10 ring-1 ring-success/10",
        "warning": "bg-warning/5 text-warning border border-warning/10 ring-1 ring-warning/10",
        "error": "bg-error/5 text-error border border-error/10 ring-1 ring-error/10",
    }

    def get_context_data(self, message):
        level_tag = message.level_tag
        level_class = self.level_classes.get(level_tag, self.level_classes["info"])
        icon = self.level_icons.get(level_tag, self.level_icons["info"])

        return {
            "message": message,
            "icon": icon,
            "level_class": level_class,
            "timeout": 9000,
        }
