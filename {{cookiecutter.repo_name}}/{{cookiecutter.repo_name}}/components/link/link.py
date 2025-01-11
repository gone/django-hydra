from django_components import Component, register

@register("link")
class Button(Component):
    """
    Link component

    """

    template_name = "link.html"


    def get_context_data(
            self,
            text: str,
            url: str,
            attrs: dict[str, str] | None = None,
    ):
        if attrs is None:
            attrs = {}

        # Build base classes
        classes = [
            "text-blue-500",
            "hover:text-blue-700",
            "underline",
        ]

        attrs['class'] = f"{' '.join(classes)} {attrs.get('class', '')}".strip()

        # Check for HTMX usage
        is_htmx = any(k.startswith('hx-') for k in attrs.keys())


        return {
            'text': text,
            'url': url,
            'attrs': attrs,
        }
