import sys

from django.conf import settings

import cronjobs
import requests
from icalendar import Calendar

from bedrock.events.models import Event


@cronjobs.register
def update_reps_ical():
    resp = requests.get(settings.REPS_ICAL_FEED)
    cal = Calendar.from_ical(resp.text)
    current_uids = Event.objects.all().values_list('id', flat=True)
    new_uids = []
    for event in cal.walk('vevent'):
        uid = event.decoded('uid')
        sequence = event.decoded('sequence')
        new_uids.append(uid)
        try:
            event_obj = Event.objects.get(id=uid)
        except Event.DoesNotExist:
            event_obj = None

        if event_obj and event_obj.sequence == sequence:
            continue

        if event_obj is None:
            event_obj = Event()

        event_obj.update_from_ical(event)
        event_obj.save()
        sys.stdout.write('.')
        sys.stdout.flush()

    to_delete = set(current_uids) - set(new_uids)
    Event.objects.filter(id__in=list(to_delete)).delete()
