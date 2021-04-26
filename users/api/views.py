"""Views for users app."""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from users.api.permissions import IsAdminOrSuperUser
from .paginators import SmallPagePagination
from .serializers import (
    UserCreatorByEmailSerializer,
    JWTTokenSerializer,
    UserSerializer
)

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_by_email(request):
    """Create user and send email."""
    serializer = UserCreatorByEmailSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']

    serializer.save(
        is_active=False,
    )

    user = User.objects.get_or_create(email=email)
    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        'Confirmation code',
        f'Your confirmation code: {confirmation_code}',
        settings.EMAIL_FROM,
        [email, ],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    """Generate JWT-token."""
    serializer = JWTTokenSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,
                             email=serializer.validated_data.get('email'))
    user.is_active = True
    user.save()
    token = AccessToken.for_user(user)
    return JsonResponse({'token': str(token)},
                        status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    """View for user model."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperUser]
    pagination_class = SmallPagePagination
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated, ], url_path='me',
            url_name='personal_data')
    def me(self, request):
        """Get and patch personal data."""
        user = request.user

        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)

        serializer = UserSerializer(user, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
