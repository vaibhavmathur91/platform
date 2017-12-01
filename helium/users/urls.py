"""
Users URLs.
"""

from django.conf.urls import url

from helium.users.views.accountviews import *
from helium.users.views.apis.externalcalendarview import ExternalCalendarApiListView, ExternalCalendarApiDetailView
from helium.users.views.apis.userprofileview import UserProfileApiView
from helium.users.views.apis.usersettingsview import UserSettingsApiView
from helium.users.views.apis.userview import UserApiView
from helium.users.views.authenticationviews import *

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2017, Helium Edu'
__version__ = '1.0.0'

urlpatterns = [
    # Authentication URLs
    url(r'^register$', register, name='register'),
    url(r'^verify$', verify, name='verify'),
    url(r'^login$', login, name='login'),
    url(r'^logout', logout, name='logout'),
    url(r'^forgot', forgot, name='forgot'),

    # Account URLs
    url(r'^settings', settings, name='settings'),

    # API URLs
    url(r'^api/user', UserApiView.as_view(), name='api_user'),
    url(r'^api/user/profile', UserProfileApiView.as_view(), name='api_user_profile'),
    url(r'^api/user/settings', UserSettingsApiView.as_view(), name='api_user_settings'),
    url(r'^api/user/externalcalendars/$', ExternalCalendarApiListView.as_view(), name='api_user_externalcalendar_list'),
    url(r'^api/user/externalcalendar/(?P<pk>[0-9]+)/$', ExternalCalendarApiDetailView.as_view(),
        name='api_user_externalcalendar_detail')
]
