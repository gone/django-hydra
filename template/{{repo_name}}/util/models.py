from django.db import models
from django.utils.translation import gettext_lazy as _

from .util import file_url


class TestFileModel(models.Model):
    file_field = models.ImageField(_("foo"), upload_to=file_url("filez"))

    class Meta:
        verbose_name = _("test")
        verbose_name_plural = _("tests")

    def __str__(self):
        return f"Test Model: {self.file_field}"
