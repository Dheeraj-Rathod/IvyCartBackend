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
from apps.users.models import UserProfile
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

class GetUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
        ]
        read_only_fields = fields

class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "phone",
            "address",
            "city",
            "state",
            "pincode",
        ]
        read_only_fields = ["id", "user"]

    def validate(self, attrs):
        # 1. Grab the request from the serializer context
        request = self.context.get('request')
        
        if request and hasattr(request, 'user'):
            current_user = request.user
            
            # 2. Check if a profile record already exists for this specific user
            if UserProfile.objects.filter(user=current_user).exists():
                # 3. Stop the execution and return a clean HTTP 400 Bad Request
                raise serializers.ValidationError(
                    {"detail": "A profile already exists for this user account."}
                )
                
        return attrs

class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
            model = UserProfile
            fields = [
                "phone",
                "address",
                "city",
                "state",
                "pincode",
            ]
            read_only_fields = ["id"]