from django_components import Component, register

@register("button")
class Button(Component):
    """
    Button component with HTMX support.

    Colors:
        - primary: Main action color
        - secondary: Less prominent actions
    Sizes:
        - sm: Small buttons (px-3 py-1.5 text-sm)
        - md: Medium buttons (px-4 py-2 text-base) [default]
        - lg: Large buttons (px-5 py-2.5 text-lg)
    Variants:
        - normal: Solid background color [default]
        - outline: Bordered with transparent background
    Slots:
        - content (required): Main button text
        - loading: Custom loading indicator for HTMX requests

    Usage:
        Basic:
        {% component "button" %}
            Click Me
        {% endcomponent %}

        With Icons:
        {% component "button" color="secondary" %}
            {% heroicon_mini "user" %}
            Profile
            {% heroicon_mini "arrow-right" %}
        {% endcomponent %}

        Outline Variant:
        {% component "button" variant="outline" %}
            Secondary Action
        {% endcomponent %}

        HTMX Integration:
        {% component "button"
            attrs:hx-post="{% url 'save'%}"
            attrs:hx-target="#result"
        %}
            Save
        {% endcomponent %}
    """

    template_name = "button.html"



    def get_context_data(
        self,
        variant: str = "normal",
        color: str = "primary",
        size: str = "md",
        disabled: bool = False,
        attrs: dict[str, str] | None = None,
        link: str = "",
        target: str = "",
    ):
        if attrs is None:
            attrs = {}

        # Build base classes
        classes = [
            "btn",
            f"btn-{size}",
            f"btn-{color}",
        ]

        if variant == "outline":
            classes.append("btn-outline")

        attrs.setdefault("class", " ".join(classes))

        # Check for HTMX usage
        is_htmx = any(k.startswith('hx-') for k in attrs.keys())

        # Handle disabled state
        if disabled:
            attrs["disabled"] = True
            attrs["aria-disabled"] = "true"
            attrs["class"] += " disabled"


        return {
            'attrs': attrs,
            'is_htmx': is_htmx,
        }
