from django_components import Component, register


@register("footer_nav_link")
class FooterNavLink(Component):
    template_name = "footer_nav_link.html"

    def get_context_data(self, href, text):
        return {"href": href, "text": text}


@register("social_link")
class SocialLink(Component):
    template_name = "social_link.html"

    def get_context_data(self, name, href="#", icon_type=None, size="5"):
        return {
            "href": href,
            "name": name,
            "icon_type": icon_type or name.lower(),
            "size": size,
        }
