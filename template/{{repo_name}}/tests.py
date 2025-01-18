import pytest
from django.core import management


@pytest.mark.django_db
def test_no_migrations(capsys):
    management.call_command("makemigrations", dry_run=True)

    captured = capsys.readouterr()
    assert "No changes detected" in captured.out
