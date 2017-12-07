"""
Authenticated views for ExternalCalendar interaction.
"""

import logging

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticated

from helium.feed.models import ExternalCalendar
from helium.feed.permissions import IsOwner
from helium.feed.serializers.externalcalendarserializer import ExternalCalendarSerializer

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2017, Helium Edu'
__version__ = '1.0.0'

logger = logging.getLogger(__name__)


class ExternalCalendarsApiLCView(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = ExternalCalendarSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.external_calendars.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExternalCalendarsApiDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = ExternalCalendar.objects.all()
    serializer_class = ExternalCalendarSerializer
    permission_classes = (IsAuthenticated, IsOwner,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
