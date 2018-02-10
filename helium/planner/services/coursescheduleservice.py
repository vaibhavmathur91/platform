import datetime
import logging

import pytz
from django.utils.timezone import make_aware

from helium.common import enums
from helium.planner.models import Event

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.3.1'

logger = logging.getLogger(__name__)


def __get_start_time_for_weekday(course_schedule, weekday):
    if weekday == 0:
        return course_schedule.sun_start_time
    elif weekday == 1:
        return course_schedule.mon_start_time
    elif weekday == 2:
        return course_schedule.tue_start_time
    elif weekday == 3:
        return course_schedule.wed_start_time
    elif weekday == 4:
        return course_schedule.thu_start_time
    elif weekday == 5:
        return course_schedule.fri_start_time
    elif weekday == 6:
        return course_schedule.sat_start_time


def __get_end_time_for_weekday(course_schedule, weekday):
    if weekday == 0:
        return course_schedule.sun_end_time
    elif weekday == 1:
        return course_schedule.mon_end_time
    elif weekday == 2:
        return course_schedule.tue_end_time
    elif weekday == 3:
        return course_schedule.wed_end_time
    elif weekday == 4:
        return course_schedule.thu_end_time
    elif weekday == 5:
        return course_schedule.fri_end_time
    elif weekday == 6:
        return course_schedule.sat_end_time


def course_schedules_to_events(course, course_schedules):
    """
    For the given course schedule model, generate an event for each class time within the courses's start/end window.

    :param course: The course with a start/end date range to iterate over.
    :param course_schedules: A list of course schedules to generate the events for.
    :return: A list of event resources.
    """
    events = []

    # TODO: responses should, in the future, be cached for at least a few minutes
    day = course.start_date
    while day <= course.end_date:
        for course_schedule in course_schedules.iterator():
            if course_schedule.days_of_week[enums.PYTHON_TO_HELIUM_DAY_OF_WEEK[day.weekday()]] == "1":
                start_time = __get_start_time_for_weekday(course_schedule, day.weekday())
                end_time = __get_end_time_for_weekday(course_schedule, day.weekday())

                event = Event(id=len(events),
                              title=course.title,
                              all_day=False,
                              show_end_time=True,
                              start=make_aware(datetime.datetime.combine(day, start_time),
                                               pytz.timezone(course.get_user().settings.time_zone)).astimezone(
                                  pytz.utc),
                              end=make_aware(datetime.datetime.combine(day, end_time),
                                             pytz.timezone(course.get_user().settings.time_zone)).astimezone(pytz.utc),
                              owner_id=course.pk,
                              user=course.get_user(),
                              calendar_item_type=enums.COURSE)
                events.append(event)

                break

        day += datetime.timedelta(days=1)

    return events