from rest_framework import serializers
from .models import User
# from django.contrib.auth.password_validation import validate_password
# from django.core.exceptions import ValidationError


# class UserIdentitySerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'password', 'role']

#     def validate_password(self, value):
#         try:
#             validate_password(value)
#         except ValidationError as e:
#             raise serializers.ValidationError(e.messages)
#         return value
    
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username = validated_data.get('username'),
#             password = validated_data.get('password'),
#         )
#         return user
    

class UserIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'token', 'mastery']