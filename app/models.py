from django.db import models
from django.utils import timezone


class Sensor(models.Model):
    created_by = models.ForeignKey('auth.User')
    display_name = models.CharField(max_length=200)
    created_date = models.DateTimeField(
            default=timezone.now)
    last_seen = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return self.display_name + " (" + str(self.id) + ")"
