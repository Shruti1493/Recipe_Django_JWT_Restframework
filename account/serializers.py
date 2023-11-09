from rest_framework import serializers

from account.models import User,Recipe

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']  
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2', None)

        if password != password2:
            raise serializers.ValidationError("Password and confirm password do not match")

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email', 'password']  
      

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','name',]


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"