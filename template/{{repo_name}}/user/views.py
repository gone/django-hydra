from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from django_htmx.http import HttpResponseClientRedirect


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        if request.htmx:
            return HttpResponseClientRedirect(url)
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return "/"


user_redirect_view = UserRedirectView.as_view()
