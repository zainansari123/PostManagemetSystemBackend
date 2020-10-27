from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from rest_framework.serializers import *
from ..models import *
# from admin_panel.models import *
from rest_framework.exceptions import APIException
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
import random
from datetime import date, datetime

# import logging
# accounts_serializer = logging.getLogger('accounts')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields='__all__'


class UserLoginSerializer(Serializer):
    usertype = CharField(error_messages={"required":"usertype key is required","blank":"usertype is required"})
    username = CharField(error_messages={"required":"username key is required","blank":"username is required"})
    password = CharField(write_only=True,error_messages={"required":"password key is required","blank":"password is required"})
    token= CharField(read_only=True)
    first_name= CharField(read_only=True)
    last_name= CharField(read_only=True)
    email= CharField(read_only=True)
    country_code= CharField(read_only=True)
    mobile= CharField(read_only=True)
    gender= CharField(read_only=True)
    profile_img= CharField(read_only=True)

    def validate(self, data):
        usertype = data['usertype']
        username = data['username']
        password = data['password']
        qs=''
        if usertype not in ('1','2'):
            raise ValidationError('please Enter Valid User type')
        if username:
            if usertype=='1':
                qs = User.objects.filter(username=username,is_superuser=True)
            if usertype=='2':
                qs = User.objects.filter(username=username)
            if qs.exists():
                user = qs.first()
                if not user.check_password(password):
                    raise ValidationError("Invalid credentials")

                payload = jwt_payload_handler(user)
                token = 'JWT ' + jwt_encode_handler(payload)
                data['first_name'] = user.first_name
                data['last_name'] = user.last_name
                data['country_code'] = user.country_code
                data['mobile'] = user.mobile
                data['gender'] = user.gender
                data['profile_img'] = user.profile_img.url if user.profile_img else user.profile_img
                data['token'] = token
                request = self.context.get('request')
                request.session.create()
                data['session_id'] = request.session.session_key
                user_logged_in.send(sender=request.user.__class__, user=user, request=request)
            else:
                raise ValidationError("User does not exist")
        return data


class UpdateUserSerializer(ModelSerializer):
    username = CharField(error_messages={"required":"username key is required","blank":"username is required"})
    password = CharField(error_messages={"required":"password key is required","blank":"password is required"})
    first_name = CharField(error_messages={"required":"first_name key is required","blank":"first_name is required"})
    last_name = CharField(error_messages={"required":"last_name key is required","blank":"last_name is required"})
    email = CharField(error_messages={"required":"email key is required","blank":"email is required"})
    country_code = CharField(error_messages={"required":"country_code key is required","blank":"country_code is required"})
    mobile = CharField(error_messages={"required":"mobile key is required","blank":"mobile is required"})
    gender = CharField(error_messages={"required":"gender key is required","blank":"gender is required"})
    profile_img = ImageField(error_messages={"required":"profile_img key is required","blank":"please upload profile image"})

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.country_code = validated_data.get('country_code', instance.country_code)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.profile_img = validated_data.get('profile_img', instance.profile_img)

        instance.save()
        return instance

    class Meta:
        model = User
        fields = '__all__'


class CreateUserSerializer(Serializer):
    username = CharField(error_messages={"required": "username key is required", "blank": "username is required"})
    password = CharField(error_messages={"required": "password key is required", "blank": "password is required"})
    first_name = CharField(error_messages={"required": "first_name key is required", "blank": "first_name is required"})
    last_name = CharField(error_messages={"required": "last_name key is required", "blank": "last_name is required"})
    email = CharField(error_messages={"required": "email key is required", "blank": "email is required"})
    country_code = CharField(
        error_messages={"required": "country_code key is required", "blank": "country_code is required"})
    mobile = CharField(error_messages={"required": "mobile key is required", "blank": "mobile is required"})
    gender = CharField(error_messages={"required": "gender key is required", "blank": "gender is required"})
    profile_img = ImageField(error_messages={"required": "profile_img key is required", "blank": "please upload profile image"})
    token=CharField(read_only=True)

    def validate(self, data):
        username=data['username']
        if username:
            qs = User.objects.filter(username=username)
            if qs.exists():
                raise ValidationError("Username Already Exists")
        return data

    def create(self, validated_data):
        username = validated_data['username']
        if username:
            user = User(username=username,first_name=validated_data['first_name'],last_name=validated_data['last_name'],
                        email=validated_data['email'],country_code=validated_data['country_code'],
                        mobile=validated_data['mobile'],gender=validated_data['gender'],profile_img=validated_data.get('profile_img'))
            user.set_password(validated_data['password'])
            user.save()
            payload = jwt_payload_handler(user)
            token = 'JWT ' + jwt_encode_handler(payload)
            validated_data['token']=token

        return validated_data
