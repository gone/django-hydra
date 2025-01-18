import time
from datetime import datetime

import pytest
from django.conf import settings
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import TestFileModel
from .util import file_url


def test_file_url():
    file_url_obj = file_url("foo")
    assert file_url_obj.category == "foo"

    timestamp = int(time.time())
    actual = file_url_obj("trash", "some_filename")
    now = datetime.now()

    expected = f"uploads/foo/{now:%Y/%m/%d}/{timestamp}/some_filename"
    assert actual == expected


@pytest.mark.django_db
def test_file_upload():
    fake_file = SimpleUploadedFile("some_file.txt", b"asdf", content_type="text")
    now = datetime.now()
    timestamp = int(time.time())

    file_field_url = TestFileModel.objects.create(file_field=fake_file).file_field.url
    expected = f"{settings.MEDIA_URL}uploads/filez/{now:%Y/%m/%d}/{timestamp}/some_file.txt"
    assert file_field_url == expected


def test_send_email(mailoutbox):
    mail.send_mail("subject", "body", "from@lightmatter.com", ["to@lightmatter.com"])
    assert len(mailoutbox) == 1

    m = mailoutbox[0]
    assert m.subject == "subject"
    assert m.body == "body"
    assert m.from_email == "from@lightmatter.com"
    assert list(m.to) == ["to@lightmatter.com"]
