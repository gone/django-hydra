from django_components import Component, register


@register("profile-popover")
class ProfilePopover(Component):
    """
    Profile-specific popover component extending the base popover functionality.

    Template slots:
        - menu_items: Menu items to be displayed in the popover

    Context variables:
        - avatar_url: URL for the user's avatar image
        - user_name: User's display name
        - user_email: User's email address
        - show_chevron: Whether to show the dropdown chevron (default: True)
        - show_profile: Whether to show the profile header section (default: True)
    """

    template_name = "profile-popover.html"

    def get_context_data(self, **kwargs):
        return kwargs
