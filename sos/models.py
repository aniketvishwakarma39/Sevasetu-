from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SOS(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class SOSJoin(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    sos = models.ForeignKey(SOS, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.volunteer} - {self.status}"