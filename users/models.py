from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager


class CustomUser(AbstractUser):
    """Model CustomUser."""

    class RoleClassChoices(models.TextChoices):
        """Choices of user roles."""
        USER = 'user', 'user'
        MODERATOR = 'moderator', 'moderator'
        ADMIN = 'admin', 'admin'

    email = models.EmailField(
        unique=True,
        db_index=True,
        error_messages={
            'unique': "This email already registered.",
        },
        verbose_name='email address',
    )
    role = models.CharField(
        max_length=10,
        choices=RoleClassChoices.choices,
        default=RoleClassChoices.USER,
        verbose_name='user role',
    )
    bio = models.TextField(blank=True, verbose_name='biography', )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        ordering = ['username']

    def save(self, *args, **kwargs):
        """Set email to username if username is empty."""
        self.username = self.username or self.email
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == self.RoleClassChoices.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.RoleClassChoices.MODERATOR
