# from django.contrib.auth.models import User
# from rest_framework import serializers


# class RegisterSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ["username", "email", "password"]

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data["username"],
#             email=validated_data["email"],
#             password=validated_data["password"]
#         )

#         return user
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']
    
    def validate_email(self, value):
        email = value.strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "This email is already registers."
            )
        return email
    
    def create(self, validated_user_data):

        user = User.objects.create_user(
            username=validated_user_data['username'],
            email=validated_user_data['email'],
            password=validated_user_data['password']
        )
        return user