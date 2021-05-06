from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from djongo import models
from rest_framework.authtoken.models import Token

from parents_guide import settings


# Create your models here.
# Create your models here.

class Bus(models.Model):
    _id = models.ObjectIdField()
    bus_number = models.CharField(max_length=15)
    number_of_places = models.IntegerField()
    reserved_places = models.IntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        unique_together = ['bus_number']
        ordering = ['bus_number']
        db_table = "buses"

    def __str__(self):
        return self.bus_number


class Parent(AbstractUser):
    _id = models.ObjectIdField()
    phone_number = models.CharField(max_length=30, blank=False, null=False)
    profession = models.CharField(max_length=50, blank=False, null=False)
    picture = models.ImageField(blank=True, null=True, upload_to='users/')
    bus_number = models.ForeignKey(to=Bus, on_delete=models.DO_NOTHING)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        unique_together = ["email"]
        ordering = ["email"]
        db_table = "parents"

    def __str__(self):
        return self.email


class Driver(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.FloatField(max_length=13, blank=True, null=True)
    matricule = models.CharField(max_length=10, blank=False, null=False)
    bus_number = models.ForeignKey(to=Bus, on_delete=models.DO_NOTHING)
    phone_number = models.CharField(max_length=30, blank=False, null=False)

    class Meta:
        # unique_together = ["email"]
        # ordering = ["email"]
        db_table = "drivers"

    def __str__(self):
        return self.matricule


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
