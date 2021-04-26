from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

User = get_user_model()


class UserCreatorByEmailSerializer(serializers.ModelSerializer):
    """Serializer for create user by email and sent confirmation code."""

    class Meta():
        fields = ('email',)
        model = User


class JWTTokenSerializer(serializers.Serializer):
    """Custom JWT-token serializer."""

    class Meta():
        fields = ('email', 'confirmation_code')
        model = User

    def validate(self, attrs):
        """Check matching for email and confirmation code."""
        user = get_object_or_404(User, email=self.initial_data.get('email'))

        if not default_token_generator.check_token(user, self.initial_data.get(
                'confirmation_code')):
            raise ValidationError("Пользователь с такими данными не найден")
        return self.initial_data


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta():
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }
        model = User
