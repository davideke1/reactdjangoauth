# import re
#
# from django.contrib.auth.hashers import make_password
# from rest_framework import serializers
# from .models import UserProfile
#
#
# class UserRegisterSerializer(serializers.ModelSerializer):
#     confirm_password = serializers.CharField(write_only=True)
#     class Meta:
#         model = UserProfile
#         fields = ['id','username', 'first_name', 'last_name', 'gender', 'email', 'mobile_number', 'password', 'confirm_password']
#
#
#         def validate_username(self, value):
#             if UserProfile.objects.filter(username=value).exists():
#                 raise serializers.ValidationError('This username is already taken.')
#             return value
#
#         def validate_email(self, value):
#             if UserProfile.objects.filter(email=value).exists():
#                 raise serializers.ValidationError('This email is already registered.')
#             return value
#
#     def validate_first_name(self, value):
#
#         if not value.isalpha():
#             raise serializers.ValidationError('First name should contain only alphabetic characters.')
#         return value
#
#     def validate_last_name(self, value):
#
#         if not value.isalpha():
#             raise serializers.ValidationError('Last name should contain only alphabetic characters.')
#         return value
#
#     def validate_mobile_number(self, value):
#
#         if not value.isdigit():
#             raise serializers.ValidationError('Mobile number should contain only digits.')
#         if not re.match(r'^[6-9]\d{9}$', value):
#             raise serializers.ValidationError('Mobile number is not in a valid Indian format.')
#         if UserProfile.objects.filter(mobile_number=value).exists():
#             raise serializers.ValidationError('This mobile number is already registered.')
#
#         return value
#
#     def validate_password(self, value):
#
#         if len(value) < 8:
#             raise serializers.ValidationError('Password should be at least 8 characters long.')
#         if not any(char.isupper() for char in value):
#             raise serializers.ValidationError('Password should contain at least one uppercase letter.')
#         if not any(char.islower() for char in value):
#             raise serializers.ValidationError('Password should contain at least one lowercase letter.')
#         if not any(char.isdigit() for char in value):
#             raise serializers.ValidationError('Password should contain at least one numeric digit.')
#         if not any(char in '!@#$%^&*()' for char in value):
#             raise serializers.ValidationError('Password should contain at least one special character.')
#         return value
#
#     def validate_confirm_password(self, value):
#         password = self.initial_data.get('password')
#         if password and password != value:
#             raise serializers.ValidationError("Passwords do not match.")
#         return value
#
#     def create(self, validated_data):
#         validated_data.pop('confirm_password')
#         validated_data['password'] = make_password(validated_data['password'])
#         user = UserProfile.objects.create(**validated_data)
#         return user
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation.pop('password', None)
#         return representation
#
# # class UserLoginSerializer(serializers):
# #     pass
# #
# # class UserSerializer(serializers):
# #     pass
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'password']
#
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'username': {'validators': []},  # Skip default username validators
#         }
#
#     def validate_first_name(self, value):
#         # Add your validation logic for the first_name field here
#         return value
#
#     def validate_last_name(self, value):
#         # Add your validation logic for the last_name field here
#         return value
#
#     def validate_username(self, value):
#         # Add your validation logic for the username field here
#         return value
#
#     def validate_password(self, value):
#         # Add your validation logic for the password field here
#         return value
#
#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user
#
#
# class UserSerializer(serializers.ModelSerializer):
#     user_profile = UserProfileSerializer()
#
#     class Meta:
#         model = UserProfile
#         fields = ['user_profile', 'gender', 'mobile_number']
#
#     def validate_gender(self, value):
#         # Add your validation logic for the gender field here
#         return value
#
#     def validate_mobile_number(self, value):
#         # Add your validation logic for the mobile_number field here
#         return value
#
#     def create(self, validated_data):
#         user_profile_data = validated_data.pop('user_profile')
#         user = UserSerializer().create(validated_data)
#         UserProfile.objects.create(user=user, **user_profile_data)
#         return user
# class UserSerializer(serializers.ModelSerializer):
#     username = serializers.CharField()
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     gender = serializers.ChoiceField(choices=UserProfile.GENDER_CHOICES)
#     phone_number = serializers.CharField(source='user_profile.mobile_number')
#     password = serializers.CharField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'gender', 'phone_number', 'password', 'confirm_password']
#
#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         confirm_password = validated_data.pop('confirm_password')
#
#         if password != confirm_password:
#             raise serializers.ValidationError("Passwords do not match.")
#
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#
#         return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['gender', 'mobile_number']


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'confirm_password', 'user_profile']

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password', None)

        if confirm_password and confirm_password != validated_data['password']:
            raise serializers.ValidationError("Passwords do not match.")

        user_profile_data = validated_data.pop('user_profile')

        # Create User instance
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        # Create UserProfile instance
        user_profile = UserProfile.objects.create(
            user=user,
            **user_profile_data
        )

        return user
