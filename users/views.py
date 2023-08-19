from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   extend_schema, extend_schema_view)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import (SMSCodeVerificationSerializer,
                          UserRegistrationSerializer, UserViewSerializer)


@extend_schema(
    summary='Enter a mobile phone number to register user',
    request=UserRegistrationSerializer,
    examples=[
        OpenApiExample(
            'Mobile phone example',
            description='Test example for the entering mobile phone',
            value={
                "phone_number": "+79888888888",
            },
            status_codes=[str(status.HTTP_200_OK)],
        ),
    ],
)
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = serializer.save()
        if created:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK
        user.send_confirmation()
        user.generate_referral_code()
        user.save()
        return Response({'detail': 'Verification code sent.',
                         'security_code': user.security_code}, status=status_code)


@extend_schema(
    summary='Verifying mobile phone by entering a sms-code',
    request=SMSCodeVerificationSerializer,
    examples=[
        OpenApiExample(
            'Mobile phone and sms-code example',
            description='Test example for the entering mobile phone',
            value={
                "phone_number": "+79888888888",
                "security_code": "1111",
            },
            status_codes=[str(status.HTTP_200_OK)],
        ),
    ],
)
class SMSCodeVerificationView(APIView):
    def post(self, request):
        serializer = SMSCodeVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        security_code = serializer.validated_data['security_code']
        user = CustomUser.objects.get(phone_number=phone_number)
        if user.check_verification(security_code):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'detail': 'Invalid SMS code.'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(
        summary='Get a user profile',
        description='Get a detail profile information such as phone_number, referral code, '
                    'mobile phones of users who entered this user referral code'
    ),
    put=extend_schema(
        summary='Update user profile with an entering a referral code',
        request=UserViewSerializer,
        parameters=[
            OpenApiParameter(
                name='invited_by_code',
                location=OpenApiParameter.HEADER,
                description='another user referral code',
                required=False,
                type=str
            )],
        examples=[OpenApiExample('Mobile phone and sms-code example',
                                 description='Test example for the entering mobile phone',
                                 value={
                                     "phone_number": "+79888888888",
                                     "invited_by_code": "c24b4a",
                                 },
                                 )]
    ))
class UserAPIView(APIView):

    def get(self, request, phone_number):
        object = CustomUser.objects.get(phone_number=phone_number)
        invitations_by_user = str([str(user.phone_number) for user in
                                   CustomUser.objects.filter(
                                       invited_by_code=object.invitation_code)])
        return Response({
            'phone_number': str(object.phone_number),
            'invitation_code': object.invitation_code,
            'invited_by': str(object.invited_by),
            'invitations_by_user': invitations_by_user,
        })

    def put(self, request, phone_number):
        user_object = CustomUser.objects.get(phone_number=phone_number)
        data = self.request.data
        referral_user = CustomUser.objects.get(invitation_code=data['invited_by_code'])
        serializer = UserViewSerializer(user_object, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if not user_object.invited_by_code:
            user_object.invited_by = referral_user
            user_object.save()
            return Response(serializer.data)
        else:
            return Response({'detail': 'Invitation code has already activated.'},
                            status=status.HTTP_400_BAD_REQUEST
                            )
