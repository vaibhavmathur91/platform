"""
Permissions for interacting with the REST API.
"""
import logging

from rest_framework import permissions

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2017, Helium Edu'
__version__ = '1.0.0'

logger = logging.getLogger(__name__)


class IsOwner(permissions.BasePermission):
    """
    This permission can be used if "user" is a base element of this object.
    """

    def has_object_permission(self, request, view, obj):
        return obj.get_user() == request.user
