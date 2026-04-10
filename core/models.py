from django.contrib.auth.models import AbstractUser
from django.db import models

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


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    normalized_location = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)   # 🔥 NEW
    end_date = models.DateField(null=True, blank=True)     # 🔥 NEW

    def save(self, *args, **kwargs):
        self.normalized_location = self.location.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} joined {self.event}"
    
class Sponsorship(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.sponsor} sponsored {self.event}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    badge = models.CharField(max_length=50, default="Beginner")

    def __str__(self):
        return self.user.username