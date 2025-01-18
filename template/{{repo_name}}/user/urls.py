from django.urls import path

from .views import user_redirect_view

app_name = "user"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
]
