from django.db import models
from django.utils import timezone


class Sensor(models.Model):
    owner = models.ForeignKey('auth.User', related_name='sensors', on_delete=models.CASCADE)
    display_name = models.CharField(max_length=200)
    created_date = models.DateTimeField( blank=True, default=timezone.now)
    last_seen = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.display_name + " (" + str(self.id) + ")"

class Movement(models.Model):
    owner = models.ForeignKey('auth.User', related_name='movements', on_delete=models.CASCADE)
    sensor = models.ForeignKey('Sensor', related_name='movements', on_delete=models.CASCADE)
    direction = models.CharField(max_length=200,
            choices=[("IN", "Entrance"),("OUT", "Exit")])
    received_date = models.DateTimeField(default=timezone.now)
    occurrence_date = models.DateTimeField()

    def __str__(self):
        return self.direction + " @ " + str(self.sensor_id)
