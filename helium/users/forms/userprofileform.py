"""
Form for user's personal information modification.
"""

from helium.common.forms.base import BaseForm
from helium.users.models import UserSetting

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2017, Helium Edu'
__version__ = '1.0.0'


class UserProfileForm(BaseForm):
    class Meta:
        model = UserSetting
        fields = ('first_name', 'last_name', 'phone',)
