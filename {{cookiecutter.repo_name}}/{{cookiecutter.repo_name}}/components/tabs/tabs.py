from django_components import Component, register

@register("tabs")
class Tabs(Component):
    template_name = "tabs.html"

    def get_context_data(self, tabs=None, tabs_style="mx-auto max-w-3xl w-full", labels_list_style="-mb-px flex items-stretch",
                        panels_list_style="rounded-b-md border border-gray-200 bg-white", tabs_attrs=None,
                        labels_list_attrs=None, panels_list_attrs=None):
        if tabs is None:
            tabs = []
        return {
            "tabs": tabs,
            "tabs_style": tabs_style,
            "labels_list_style": labels_list_style,
            "panels_list_style": panels_list_style,
            "tabs_attrs": tabs_attrs or {},
            "labels_list_attrs": labels_list_attrs or {},
            "panels_list_attrs": panels_list_attrs or {}
        }
