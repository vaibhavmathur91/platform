import datetime

import mock
import pytz
from django.test import TestCase

from helium.auth.tests.helpers import userhelper
from helium.common import enums
from helium.planner.models import Reminder
from helium.planner.services import reminderservice
from helium.planner.tests.helpers import coursegrouphelper, coursehelper, homeworkhelper, eventhelper, reminderhelper

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2017, Helium Edu'
__version__ = '1.0.0'


class TestCaseReminderService(TestCase):
    @mock.patch('helium.planner.tasks.remindertasks.commonutils.send_multipart_email')
    def test_process_email_reminders(self, send_multipart_email):
        # GIVEN
        user = userhelper.given_a_user_exists()
        course_group = coursegrouphelper.given_course_group_exists(user)
        course = coursehelper.given_course_exists(course_group)
        homework = homeworkhelper.given_homework_exists(course)
        event1 = eventhelper.given_event_exists(user)
        event2 = eventhelper.given_event_exists(user,
                                                start=datetime.datetime.now().replace(
                                                    tzinfo=pytz.timezone(user.settings.time_zone)) + datetime.timedelta(
                                                    days=1),
                                                end=datetime.datetime.now().replace(
                                                    tzinfo=pytz.timezone(user.settings.time_zone)) + datetime.timedelta(
                                                    days=1, hours=1))
        reminder1 = reminderhelper.given_reminder_exists(user, type=enums.EMAIL, event=event1)
        reminder2 = reminderhelper.given_reminder_exists(user, type=enums.EMAIL, homework=homework)
        # This reminder is ignored, as we're not yet in its send window
        reminder3 = reminderhelper.given_reminder_exists(user, type=enums.EMAIL, event=event2)
        # Sent reminders are ignored
        reminder4 = reminderhelper.given_reminder_exists(user, type=enums.EMAIL, sent=True, event=event1)

        # WHEN
        reminderservice.process_email_reminders()

        # THEN
        self.assertEqual(send_multipart_email.call_count, 2)
        self.assertTrue(Reminder.objects.get(pk=reminder1.pk).sent)
        self.assertTrue(Reminder.objects.get(pk=reminder2.pk).sent)
        self.assertFalse(Reminder.objects.get(pk=reminder3.pk).sent)

    @mock.patch('helium.common.tasks.send_mail')
    def test_process_text_reminders(self, send_mail):
        # GIVEN
        user = userhelper.given_a_user_exists()
        user.profile.phone = '555-5555'
        user.profile.phone_carrier = enums.PHONE_CARRIER_CHOICES[0][0]
        user.profile.phone_verified = True
        user.profile.save()
        course_group = coursegrouphelper.given_course_group_exists(user)
        course = coursehelper.given_course_exists(course_group)
        homework = homeworkhelper.given_homework_exists(course)
        event1 = eventhelper.given_event_exists(user)
        event2 = eventhelper.given_event_exists(user,
                                                start=datetime.datetime.now().replace(
                                                    tzinfo=pytz.timezone(user.settings.time_zone)) + datetime.timedelta(
                                                    days=1),
                                                end=datetime.datetime.now().replace(
                                                    tzinfo=pytz.timezone(user.settings.time_zone)) + datetime.timedelta(
                                                    days=1, hours=1))
        reminder1 = reminderhelper.given_reminder_exists(user, event=event1)
        reminder2 = reminderhelper.given_reminder_exists(user, homework=homework)
        # This reminder is ignored, as we're not yet in its send window
        reminder3 = reminderhelper.given_reminder_exists(user, type=enums.EMAIL, event=event2)
        # Sent reminders are ignored
        reminder4 = reminderhelper.given_reminder_exists(user, sent=True, event=event1)

        # WHEN
        reminderservice.process_text_reminders()

        # THEN
        self.assertEqual(send_mail.call_count, 2)
        self.assertTrue(Reminder.objects.get(pk=reminder1.pk).sent)
        self.assertTrue(Reminder.objects.get(pk=reminder2.pk).sent)
        self.assertFalse(Reminder.objects.get(pk=reminder3.pk).sent)
