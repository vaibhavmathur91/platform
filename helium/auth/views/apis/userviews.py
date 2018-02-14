import logging

from django.contrib.auth import update_session_auth_hash, get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from helium.auth.forms.userdeleteform import UserDeleteForm
from helium.auth.forms.userpasswordchangeform import UserPasswordChangeForm
from helium.auth.serializers.userserializer import UserSerializer
from helium.auth.tasks import delete_user
from helium.common.permissions import IsOwner
from helium.common.utils import metricutils

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.3.5'

logger = logging.getLogger(__name__)


class UserApiDetailView(GenericAPIView, RetrieveModelMixin):
    """
    get:
    Return the authenticated user instance, including profile and settings details.

    put:
    Update the authenticated user instance.

    delete:
    Delete the authenticated user instance.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        # Process password change (if present) first, as we're going to use a form-based mechanism to do (this allows us
        # to use Django's built-in auth functionality for this, and we obviously never want to serializer passwords)
        response_data = {}
        errors = {}
        if 'old_password' in request.data or 'new_password1' in request.data or 'new_password2' in request.data:
            form = UserPasswordChangeForm(user=request.user, data=request.data)

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)

                logger.info('Password updated for {}'.format(request.user.get_username()))
            else:
                errors.update(list(form.errors.items()))

        # Process remaining attributes (if any) using serializers
        if 'username' in request.data and 'email' in request.data:
            serializer = self.get_serializer(request.user, data=request.data, context={'request': request})

            if serializer.is_valid():
                serializer.save()

                logger.info('Details updated for user {}'.format(request.user.get_username()))

                response_data.update(serializer.data)
            else:
                errors.update(serializer.errors)

        if len(errors) > 0:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        elif len(response_data) > 0:
            metricutils.increment('action.user.updated', request)

            return Response(response_data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        form = UserDeleteForm(user=request.user, data=request.data)

        if form.is_valid():
            logger.info('User {} deleted'.format(request.user.get_username()))

            metricutils.increment('action.user.deleted', request)

            delete_user.delay(form.user.pk)

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(dict(list(form.errors.items())), status=status.HTTP_400_BAD_REQUEST)
