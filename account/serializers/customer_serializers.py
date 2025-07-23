import re
from rest_framework import serializers
from account.models import Customer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:

        model = Customer
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2', 'address', 'phone','role')

    def validate_first_name(self, value):

        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError({'first_name': 'the first name must be alphanumeric'})
        return value

    def validate_last_name(self, value):

        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError({'last_name': 'the last name must be alphanumeric'})
        return value

    def validate_email(self, value):

        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError({'email': 'you should use a google account'})

        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password did\'t match'})
        try:
            validate_password(attrs['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": e.message})
        return attrs

    def validate_phone(self, value):

        if not value:
            return value

        if not re.fullmatch(r'^[0-9+]+$', value):
            raise serializers.ValidationError({'phone': 'the phone number is invalid'})

        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = Customer(**validated_data)
        user.set_password(password)
        user.save()

        return user
