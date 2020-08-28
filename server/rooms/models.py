import os
import uuid
from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model


def photo_file_path(instance, filename):
    """Generate uuid extension and file path"""
    extension = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join('uploads/room/%Y/%m/%d/', filename)


class TimeStampModel(models.Model):
    """Time stamp model for models"""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractItem(models.Model):
    """Abstract item"""
    name = models.CharField(max_length=80)
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    """Room type for a room"""
    class Meta:
        verbose_name = 'Room type'


class Amenity(AbstractItem):
    """Amenities for a room"""
    class Meta:
        verbose_name_plural = 'Amenities'


class Service(AbstractItem):
    """Services for a room"""
    class Meta:
        verbose_name_plural = 'Services'


class HouseRule(AbstractItem):
    """House rules for a room"""
    class Meta:
        verbose_name = 'House Rule'


class Room(TimeStampModel):
    """Room Model"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=100)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    user = models.ForeignKey(get_user_model(),
                            on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType,
                                on_delete=models.SET_NULL,
                                null=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    services = models.ManyToManyField(Service, blank=True)
    house_rules = models.ManyToManyField(HouseRule, blank=True)
    
    def __str__(self):
        return self.name


class Photo(TimeStampModel):
    """Photo Model for a Room"""
    caption = models.CharField(max_length=50)
    file = models.ImageField(upload_to=photo_file_path)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption