import zoneinfo

from django.contrib.messages import get_messages
from django.template.loader import render_to_string
from django.utils import timezone


def attach_messages(response):
    if not (req_messages := get_messages(response._request)).used:
        messages = render_to_string(
            "messages.html",
            {"messages": req_messages},  # NOQA
        )
        response.content = response.content + messages.encode(response.charset)
    return response


class HTMXMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        if request.htmx and not request.htmx.boosted:
            response.add_post_render_callback(attach_messages)
        return response


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.headers.get("X-Timezone", None)
        if tzname:
            timezone.activate(zoneinfo.ZoneInfo(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
