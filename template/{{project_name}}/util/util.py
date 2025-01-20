import datetime
import re
import time

from django.utils.deconstruct import deconstructible


@deconstructible
class file_url:  # NOQA
    path = "uploads/{0}/{1.year:04}/{1.month:02}/{1.day:02}/{2}/{3}"  # NOQA

    def __init__(self, category):
        self.category = category

    def __call__(self, instance, filename):
        r = re.compile(r"[^\S]")
        filename = r.sub("", filename)
        now = datetime.datetime.now()
        timestamp = int(time.time())
        return self.path.format(self.category, now, timestamp, filename)
