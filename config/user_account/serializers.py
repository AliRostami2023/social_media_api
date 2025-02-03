from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.core.mail import send_mail
from rest_framework import serializers
from datetime import datetime, timedelta
from .models import OtpCode, PasswordResetToken, ProfileUser
from .random_code import random_code_otp


User = get_user_model()


class CreateUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'username', 'password']


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        expired_date = datetime.now() + timedelta(minutes=2)
        OtpCode.objects.create(user=user, code=random_code_otp(), expired_date=expired_date)
        # todo : send sms
        print(f"otp code for {user.username}: {random_code_otp()}")
        return user



class VerifyCodeSerializers(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = ['code']
        read_only_fields = ['user', 'expired_date']
    

    def validate(self, attrs):
        phone_number = attrs.get('user__phone_number')
        code = attrs.get('code')

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('user not found'))
        
        otp = OtpCode.objects.filter(user=user, code=code).first()

        if not otp:
            raise serializers.ValidationError(_('Invalid otp code !'))
                
        if otp.expired_date_over:
            otp.delete_otp
            raise serializers.ValidationError(_('otp code has expired !'))
        
        user.is_active = True
        user.save()

        otp.delete()
        return attrs


class PasswordResetRequestSerializers(serializers.Serializer):
    email = serializers.EmailField()


    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('There are no user with this email !!!'))
        return value
    

    def create(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        reset_token = PasswordResetToken.objects.create(user=user)

        reset_link = f"{self.context['request'].build_absolute_uri(reverse_lazy('password-reset', kwargs={'token':str(reset_token.token)}))}"

        send_mail(
            subject= 'password reset request',
            message= f"click the link to reset password {reset_link}",
            from_email= 'example@gmail.com',
            recipient_list= [user.email],
            fail_silently= False
        )

        print(reset_link)
        return reset_token



class PasswordResetConfirmSerializers(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password1 = attrs['new_password']
        password2 = attrs['confirm_new_password']

        if password1 and password1 != password2:
            raise serializers.ValidationError(_('passwords must be match !!!'))
        elif len(password1) < 8:
            raise serializers.ValidationError(_('password must be more 8 char or numbers !!!'))
        return password1


    def validate_token(self, value):
        try:
            reset_token = PasswordResetToken.objects.get(is_used=False, token=value)
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError(_('invalid or expired token'))

        if not reset_token.is_valid():
            raise serializers.ValidationError(_('token has expired'))
        return value


    def save(self, **kwargs):
        reset_token = PasswordResetToken.objects.get(token=self.validated_data['token'])
        user = reset_token.user
        user.set_password(self.validated_data['new_password'])
        user.save()
        reset_token.is_used = True
        reset_token.save()


class ResendCodeSerializers(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=11)


    def validate_phone_number(self, value):
        try:
            User.objects.get(phone_number=value)
        except User.DoesNotExist:
            raise  serializers.ValidationError(_("User with this phone number does not exist !"))
        return value


    def create(self, validated_data):
        user = User.objects.get(phone_number=validated_data['phone_number'])

        otp_code = random_code_otp()
        expire_date = datetime.now() + timedelta(minutes=2)

        OtpCode.objects.update_or_create(user=user, defaults={'code': otp_code, 'expired_date': expire_date})

        print(f"Resend code for {user.phone_number} : {otp_code}")
        return user



class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = '__all__'

