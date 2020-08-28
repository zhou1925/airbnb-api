from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from ..models import Amenity, Room, RoomType, Service, HouseRule
from ..serializers import AmenitySerializer


AMENITY_URL = reverse('rooms:amenity-list')


def sample_room_type():
    """Create and return Room type"""
    return RoomType.objects.create(name='Small')

def sample_aminitie(name):
    """Create and return Amenitie"""
    return Amenity.objects.create(name=name)

def sample_service():
    """Create and return a service"""
    return Service.objects.create(name='TV')

def sample_house_rule():
    """Create and return a house rule"""
    return HouseRule.objects.create(name='No pets')

def sample_user(email, password):
    """Create and return an user"""
    return get_user_model().objects.create_user(
        email = email,
        password = password
    )

def sample_room(user, name='default room name'):
    """Create and retun a room"""
    now = timezone.now()
    room = Room.objects.create(
        name = name,
        description = 'Room description',
        country = 'AS',
        city = 'Room city',
        price = 100,
        address = 'Room address',
        guests = 2,
        beds = 2,
        bedrooms = 3,
        baths = 3,
        check_in = now.day,
        check_out = now.day + 1,
        user = user,
        room_type = sample_room_type()
    )

    return room


class PublicAmenityTests(TestCase):
    """Test the public available Amenities API"""
    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        """Test that Login is required for retrieving amenities"""
        res = self.client.get(AMENITY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateAmenityTests(TestCase):
    """Test the authorized user Amenities API"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@user.com',
            'userpassword'
        )
        self.client.force_authenticate(self.user)
    
    def test_retrieve_amenities(self):
        """Test retrieving Amenities"""
        Amenity.objects.create(name='Internet')
        Amenity.objects.create(name='Tv')

        res = self.client.get(AMENITY_URL)

        amenities = Amenity.objects.all().order_by('-name')
        serializer = AmenitySerializer(amenities, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_amenities_belongs_to_room(self):
        """Test that amenities returned belongs to room"""
        user2 = sample_user(
            email='diffuser@diff.com', 
            password='diffuserpassword')
        room = sample_room(user=user2, name='Different room')
        room.amenities.add(sample_aminitie(name='Tv'))
        
        other_room = sample_room(user=self.user, name="palace room")
        other_room.amenities.add(sample_aminitie(name='Internet'))

        res = self.client.get(AMENITY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], room.name)


