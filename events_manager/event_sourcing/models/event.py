from django.db import models
import datetime
from .base_model import BaseModel
from django.db.models import JSONField
from events_manager.event_sourcing.models.event_store import EventStore
from django.contrib.auth.models import User  


class Event(BaseModel):
    event_store = models.ForeignKey(EventStore, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.datetime.now())
    diff = JSONField(blank=True, null=True)
    state = JSONField(blank=True, null=True)
