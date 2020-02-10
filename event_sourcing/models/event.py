from django.db import models
from django.contrib.auth import get_user_model
from lib.framework.models.base_model import BaseModel
from django.contrib.postgres.fields import JSONField
from event_sourcing.models.event_store import EventStore

import datetime

User = get_user_model()


class Event(BaseModel):
    event_store = models.ForeignKey(EventStore, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.datetime.now())
    diff = JSONField(blank=True, null=True)
    state = JSONField(blank=True, null=True)
