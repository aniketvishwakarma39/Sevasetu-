from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# ================= USER =================
class User(AbstractUser):
    ROLE_CHOICES = (
        ('volunteer', 'Volunteer'),
        ('creator', 'Event Creator'),
        ('sponsor', 'Sponsor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(blank=True)

    groups = models.ManyToManyField('auth.Group', related_name='core_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='core_user_permissions_set', blank=True)


# ================= EVENT =================
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    normalized_location = models.CharField(max_length=100)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.normalized_location = self.location.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ================= PARTICIPATION =================
class Participation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user} - {self.status}"


# ================= SPONSORSHIP =================
class Sponsorship(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    sponsor = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.IntegerField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.sponsor} - {self.amount} - {self.status}"


# ================= PROFILE =================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    badge = models.CharField(max_length=50, default="Beginner")

    def __str__(self):
        return self.user.username


# ================= SIGNAL =================
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)