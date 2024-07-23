from django.db import models

from config.api.models import Helpers
from school.models import Seance


class Calendrier(Helpers):
    date_event = models.DateField()
    time_event = models.TimeField()
    seance = models.ForeignKey(
        Seance, on_delete=models.CASCADE, related_name='calendrier')
