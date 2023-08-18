from rest_framework import serializers

from users.models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('phone_number',)
        extra_kwargs = {'phone_number': {'validators': []}}

    def save(self):
        if self.instance is None:
            phone_number = self.validated_data['phone_number']
            user_obj = CustomUser.objects\
                .get_or_create(phone_number=phone_number)
            return user_obj


class SMSCodeVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'security_code')
        extra_kwargs = {'phone_number': {'validators': []}}


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'invitation_code', 'invited_by_code', 'invitations_by_user')
