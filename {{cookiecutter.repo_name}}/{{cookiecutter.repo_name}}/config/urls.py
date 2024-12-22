# flake8: noqa: F811
from django.conf import settings
from django.conf.urls import handler400, handler403, handler404, handler500
from django.contrib import admin
from django.urls import include, path, re_path

from {{cookiecutter.repo_name}}.home.views import FourHundy, FourOhFour, FourOhThree, WorkedLocally

handler400 = FourHundy
handler403 = FourOhThree
handler404 = FourOhFour
handler500 = WorkedLocally


urlpatterns = []

if "silk" in settings.INSTALLED_APPS:
    urlpatterns += [path("silk", include("silk.urls", namespace="silk"))]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            handler400,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            handler403,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            handler404,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", handler500),
    ]

    if "robots" in settings.INSTALLED_APPS:
        urlpatterns.append(
            re_path(r"^robots\.txt", include("robots.urls")),
        )

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns


urlpatterns += [
    path("account/", include("{{cookiecutter.repo_name}}.user.urls", namespace="user")),
    path("account/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("hijack/", include("hijack.urls")),
    path("", include("{{cookiecutter.repo_name}}.home.urls")),
    path("", include("django_components.urls")),
]
