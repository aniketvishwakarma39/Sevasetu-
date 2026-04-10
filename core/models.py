from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('volunteer', 'Volunteer'),
        ('creator', 'Event Creator'),
        ('sponsor', 'Sponsor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_set',   # 🔥 FIX
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_permissions_set',  # 🔥 FIX
        blank=True,
    )

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    normalized_location = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.normalized_location = self.location.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title