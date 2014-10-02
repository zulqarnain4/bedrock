from django.db import models

from bedrock.events.countries import country_to_continent


class Event(models.Model):
    id = models.CharField(max_length=40, primary_key=True, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    sequence = models.SmallIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    url = models.URLField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    country_code = models.CharField(max_length=2)
    continent_code = models.CharField(max_length=2, null=True)

    field_to_ical = {
        'id': 'uid',
        'title': 'summary',
        'description': 'description',
        'location': 'location',
        'sequence': 'sequence',
        'start_time': 'dtstart',
        'end_time': 'dtend',
        'url': 'url',
        'latitude': 'x-coordinates-lat',
        'longitude': 'x-coordinates-lon',
        'country_code': 'x-country-code',
    }

    def update_from_ical(self, ical_event):
        for field, ical_prop in self.field_to_ical.iteritems():
            setattr(self, field, ical_event.decoded(ical_prop))

    def save(self, *args, **kwargs):
        self.country_code = self.country_code.upper()
        self.continent_code = country_to_continent.get(self.country_code, None)
        super(Event, self).save(*args, **kwargs)
