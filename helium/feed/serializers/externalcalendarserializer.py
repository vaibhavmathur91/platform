"""
ExternalCalendar serializer.
"""
from future.standard_library import install_aliases

install_aliases()
import logging
from urllib.request import urlopen
from rest_framework import serializers

from helium.feed.models import ExternalCalendar

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2015, Helium Edu'
__version__ = '1.0.0'

logger = logging.getLogger(__name__)


class ExternalCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalCalendar
        fields = ('id', 'title', 'url', 'color', 'shown_on_calendar', 'user',)
        read_only_fields = ('user',)

    def validate_url(self, url):
        """
        Ensure a valid Google Calendar URL is given.

        :param url: the URL to validate
        :return: the validated URL
        """
        if urlopen(url).getcode() != 200:
            serializers.ValidationError("The URL is not reachable.")
        elif 'google.com/calendar/ical' not in url and '/private' not in url:
            serializers.ValidationError("This does not appear to be a valid, private Google Calendar ICAL feed URL.")

        return url

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        return super(ExternalCalendarSerializer, self).create(validated_data)