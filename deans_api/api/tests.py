from django.test import TestCase
from django.contrib.auth.models import User
from .models import Crisis, CrisisAssistance, CrisisType, SiteSettings, EmergencyAgencies

class CrisisModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        crisis_type = CrisisType.objects.create(name="Fire")
        crisis_assistance = CrisisAssistance.objects.create(name="Fire Brigade")
        cls.crisis = Crisis.objects.create(
            your_name="Test User",
            mobile_number="123456789",
            crisis_description="Test Crisis Description",
            crisis_status="AC",
            crisis_location1="Location 1",
            crisis_location2="Location 2"
        )
        cls.crisis.crisis_type.add(crisis_type)
        cls.crisis.crisis_assistance.add(crisis_assistance)

    def test_crisis_name_max_length(self):
        crisis = Crisis.objects.get(id=self.crisis.id)
        max_length = crisis._meta.get_field('your_name').max_length
        self.assertEquals(max_length, 255)

    def test_crisis_type_relationship(self):
        crisis = Crisis.objects.get(id=self.crisis.id)
        self.assertEqual(crisis.crisis_type.first().name, "Fire")

    def test_crisis_assistance_relationship(self):
        crisis = Crisis.objects.get(id=self.crisis.id)
        self.assertEqual(crisis.crisis_assistance.first().name, "Fire Brigade")

class EmergencyAgenciesModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.agency = EmergencyAgencies.objects.create(
            agency="Test Agency",
            phone_number="987654321"
        )

    def test_agency_name_max_length(self):
        agency = EmergencyAgencies.objects.get(id=self.agency.id)
        max_length = agency._meta.get_field('agency').max_length
        self.assertEquals(max_length, 255)

class SiteSettingsModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.settings = SiteSettings.objects.create(
            facebook_account="test_facebook",
            facebook_password="password123",
            twitter_account="test_twitter",
            twitter_password="password456",
            summary_reporting_email="test@example.com"
        )

    def test_email_format(self):
        settings = SiteSettings.objects.get(id=self.settings.id)
        self.assertIn("@", settings.summary_reporting_email)

class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="password123",
            is_staff=True
        )

    def test_user_creation(self):
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.is_staff)

class CrisisSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.crisis_type = CrisisType.objects.create(name="Flood")
        cls.crisis_assistance = CrisisAssistance.objects.create(name="Rescue Team")
        cls.crisis = Crisis.objects.create(
            your_name="Jane Doe",
            mobile_number="111222333",
            crisis_description="Test flood crisis",
            crisis_status="AC",
            crisis_location1="Area 1",
            crisis_location2="Area 2"
        )
        cls.crisis.crisis_type.add(cls.crisis_type)
        cls.crisis.crisis_assistance.add(cls.crisis_assistance)

    def test_serializer_data(self):
        from .serializer import CrisisSerializer
        serializer = CrisisSerializer(instance=self.crisis)
        self.assertEqual(serializer.data['your_name'], "Jane Doe")
        self.assertEqual(serializer.data['crisis_type'], [self.crisis_type.id])
        self.assertEqual(serializer.data['crisis_assistance'], [self.crisis_assistance.id])
