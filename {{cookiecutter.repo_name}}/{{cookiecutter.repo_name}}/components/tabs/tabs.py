from django.utils.safestring import mark_safe
from django_components import Component, register
# shamelessly stolen from https://github.com/EmilStenstrom/django-components/discussions/540

@register("_tabs_impl")
class TabsImpl(Component):
    """Internal implementation component that handles the actual rendering of tabs."""
    template_name = "tabs.html"

    # Default classes that can be overridden by subclasses
    default_container_class = 'relative mx-auto max-w-3xl w-full'
    default_labels_class = '-mb-px flex items-stretch'
    default_panels_class = 'rounded-b-md border border-gray-200 bg-white'
    default_selected_class = 'border-gray-200 bg-white'
    default_panel_class = 'p-4'

    def get_context_data(
        self,
        tabs,  # List of tab entries from parent
        tabs_attrs=None,
        labels_list_attrs=None,
        panels_list_attrs=None,
        selected_class=None,
        panel_class=None,
        name=None
    ):
        tabs_attrs = tabs_attrs or {}
        labels_list_attrs = labels_list_attrs or {}
        panels_list_attrs = panels_list_attrs or {}

        tabs_attrs.setdefault('class', self.default_container_class)
        labels_list_attrs.setdefault('class', self.default_labels_class)
        panels_list_attrs.setdefault('class', self.default_panels_class)

        return {
            "tabs": tabs,
            "tabs_attrs": tabs_attrs,
            "labels_list_attrs": labels_list_attrs,
            "panels_list_attrs": panels_list_attrs,
            "selected_class": selected_class or self.default_selected_class,
            "panel_class": panel_class or self.default_panel_class,
            "tabs_data": {"name": name} if name else {},
        }

@register("tabs")
class Tabs(Component):
    """Main tabs component - processes nested tab_items and delegates to TabsImpl."""
    template = """
        {% provide "_tab" tabs=tabs enabled=True %}
            {% slot "content" default %}{% endslot %}
        {% endprovide %}
    """

    def get_context_data(
        self,
        tabs_attrs=None,
        labels_list_attrs=None,
        panels_list_attrs=None,
        selected_class=None,
        panel_class=None,
        name=None
    ):
        return {
            "tabs": [],  # Will be populated by tab_items
            "tabs_attrs": tabs_attrs,
            "labels_list_attrs": labels_list_attrs,
            "panels_list_attrs": panels_list_attrs,
            "selected_class": selected_class,
            "panel_class": panel_class,
            "name": name,
        }

    def on_render_after(self, context, template, content):
        """After all tab_items are processed, render using the implementation component."""
        return TabsImpl.render(
            kwargs={
                "tabs": context["tabs"],
                "tabs_attrs": context["tabs_attrs"],
                "labels_list_attrs": context["labels_list_attrs"],
                "panels_list_attrs": context["panels_list_attrs"],
                "selected_class": context["selected_class"],
                "panel_class": context["panel_class"],
                "name": context["name"],
            }
        )


@register("tab_item")
class TabItem(Component):
    """Individual tab item that adds itself to parent tabs list."""
    template = """
        {% provide "_tab" tabs=empty_tabs enabled=False %}
            {% slot "content" default %}{% endslot %}
        {% endprovide %}
    """

    # Default class that can be overridden by subclasses
    default_tab_class = 'inline-flex rounded-t-md border-t border-l border-r px-5 py-2.5'

    def get_context_data(
        self,
        header,
        disabled=False,
        attrs=None,
    ):
        # Get the parent tabs context - will raise if not nested in Tabs
        tab_ctx = self.inject("_tab")

        if not tab_ctx.enabled:
            raise RuntimeError(
                f"Component '{self.name}' must be used within a Tabs component"
            )

        attrs = attrs or {}
        attrs.setdefault('class', self.default_tab_class)

        return {
            "empty_tabs": [],
            "parent_tabs": tab_ctx.tabs,
            "header": header,
            "disabled": disabled,
            "attrs": attrs,
        }

    def on_render_after(self, context, template, content):
        # Add this tab's data to the parent tabs list
        context["parent_tabs"].append({
            "header": context["header"],
            "disabled": context["disabled"],
            "attrs": context["attrs"],
            "content": mark_safe(content.strip())
        })
