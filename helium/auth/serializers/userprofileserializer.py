import logging
import re

from rest_framework import serializers

from helium.auth.models import UserProfile
from helium.auth.utils.userutils import generate_phone_verification_code
from helium.common.tasks import send_text

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.0.0'

logger = logging.getLogger(__name__)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'phone', 'phone_changing', 'phone_verification_code', 'phone_verified', 'user')
        read_only_fields = ('phone_changing', 'phone_verified', 'user',)
        extra_kwargs = {
            'phone_verification_code': {'write_only': True},
        }

    def validate_phone(self, phone):
        """
        Cleanup the phone number. This currently does no validation, just ensures the stored value is numeric.

        :param phone: the phone number being saved
        :return:
        """
        return re.sub("[^0-9]", "", phone)

    def validate_phone_verification_code(self, phone_verification_code):
        """
        Ensure the email the user isn't already taken by another user.

        :param phone_verification_code: the new email address
        """
        if phone_verification_code != self.instance.phone_verification_code:
            raise serializers.ValidationError("The verification code does not match our records")

        return phone_verification_code

    def update(self, instance, validated_data):
        # Manually process fields that require shuffling before relying on the serializer's internals to save the rest
        if 'phone_verification_code' in validated_data and validated_data.get('phone_verification_code'):
            self.__process_phone_verification_code(instance, validated_data)
        elif 'phone' in validated_data and not validated_data.get('phone'):
            self.__clear_phone_fields(instance, validated_data)
        else:
            self.__process_phone_changing(instance, validated_data)

        super(UserProfileSerializer, self).update(instance, validated_data)

        return instance

    def __process_phone_verification_code(self, instance, validated_data):
        if instance.phone_changing:
            instance.phone = instance.phone_changing
            instance.phone_changing = None

        instance.phone_verified = True

        validated_data.pop('phone', None)

    def __clear_phone_fields(self, instance, validated_data):
        instance.phone = None
        instance.phone_changing = None
        instance.phone_verified = False

        validated_data.pop('phone', None)

    def __process_phone_changing(self, instance, validated_data):
        phone = instance.phone

        if 'phone' in validated_data and instance.phone != validated_data.get('phone'):
            instance.phone_changing = validated_data.pop('phone')
            phone = instance.phone_changing

        if instance.phone != phone and phone:
            instance.phone_verification_code = generate_phone_verification_code()

            send_text.delay(phone, 'Enter this verification code on Helium\'s "Settings" page: {}'.format(
                instance.phone_verification_code))
