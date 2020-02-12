from django.db import models
from .base_model import BaseModel


class EventStore(BaseModel):
    module = models.CharField(max_length=100)
    signature = models.CharField(max_length=100)
    tracked_object_id = models.PositiveIntegerField()

    def events(self):
        return self.event_set.all()
