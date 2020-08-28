from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from ..models import Room, RoomType, HouseRule, Service, Amenity, photo_file_path


def sample_room_type():
    """Create and return Room type"""
    return RoomType.objects.create(name='Small')

def sample_aminitie():
    """Create and return Amenitie"""
    return Amenity.objects.create(name='Clean')

def sample_service():
    """Create and return a service"""
    return Service.objects.create(name='TV')

def sample_house_rule():
    """Create and return a house rule"""
    return HouseRule.objects.create(name='No pets')

def sample_user():
    """Create and return an user"""
    return get_user_model().objects.create(
        email = 'user@user.com',
        password = 'userpassword'
    )

def sample_room():
    """Create and retun a room"""
    now = timezone.now()
    room = Room.objects.create(
        name = 'Example room',
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
        user = sample_user(),
        room_type = sample_room_type()
    )
    room.amenities.add(sample_aminitie())
    room.house_rules.add(sample_house_rule())
    room.services.add(sample_service())

    return room


class RoomTests(TestCase):
    """Tests for Room model"""
    def test_amenitie_str(self):
        """Test the amenitie str representation"""
        amenitie = sample_aminitie()
        self.assertEqual(str(amenitie), amenitie.name)
    
    def test_room_type_str(self):
        """Test the Room Type str representation"""
        room_type = sample_room_type()
        self.assertEqual(str(room_type), room_type.name)
    
    def test_service_str(self):
        """Test the Service str representation"""
        service = sample_service()
        self.assertEqual(str(service), service.name)

    def test_house_rule_str(self):
        """Test the House rile str representation"""
        house_rule = sample_house_rule()
        self.assertEqual(str(house_rule), house_rule.name)

    @patch('uuid.uuid4')
    def test_photo_file_uuid(self, mock_uuid):
        """Test the photo is saved in the correct path"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = photo_file_path(None, 'photo.jpg')

        exp_path = f'uploads/room/%Y/%m/%d/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
        
