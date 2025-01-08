from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from .models import (
    Crisis,
    CrisisAssistance,
    CrisisType,
    SiteSettings,
    EmergencyAgencies
)

class CrisisModelTest(TestCase):
    @classmethod
    @patch('requests.post')
    def setUpTestData(cls, mock_post):
         # Arrange: Mock the POST request to return a status code of 200
        mock_post.return_value.status_code = 200

        # Create a CrisisType and CrisisAssistance instance to use for the tests
        cls.crisis_type = CrisisType.objects.create(name="Flood")
        cls.crisis_assistance = CrisisAssistance.objects.create(name="Medical Assistance")
        cls.user = User.objects.create_user(username="operator", password="password123")
        
        # Create a Crisis instance
        cls.crisis = Crisis.objects.create(
            your_name="Yuance",
            mobile_number="83496888",
            crisis_description="Help, there is a flood!",
            crisis_location1="Riverbank",
            visible=True
        )

        # assert called to notification
        mock_post.assert_called()

        # Assign many-to-many relations using .set()
        cls.crisis.crisis_type.set([cls.crisis_type])
        cls.crisis.crisis_assistance.set([cls.crisis_assistance])
        
        # Assign the owner using .set()
        cls.crisis.owner.set([cls.user])

    def test_model_crisis_name_max_length(self):
        yuance = Crisis.objects.get(your_name="Yuance")
        max_length = yuance._meta.get_field('your_name').max_length
        self.assertEqual(max_length, 255)

	# Test if the default values are correctly set for different fields
    def test_default_values(self):
        yuance = Crisis.objects.get(your_name="Yuance")
        self.assertEqual(yuance.crisis_status, 'PD')  # Default 'Pending' status
        self.assertEqual(yuance.visible, True)  # Default visible should be True
        self.assertEqual(yuance.dispatch_trigger, False)  # Default dispatch_trigger should be False


    #Test the functionality of the many-to-many relationship with CrisisType model
    def test_crisis_type_relation(self):
        yuance = Crisis.objects.get(your_name="Yuance")
        self.assertIn(self.crisis_type, yuance.crisis_type.all())  # Check if the type is added correctly


    #Test the many-to-many relationship with CrisisAssistance
    def test_crisis_assistance_relation(self):
        yuance = Crisis.objects.get(your_name="Yuance")
        self.assertIn(self.crisis_assistance, yuance.crisis_assistance.all())  # Check if the assistance is added


    # Test if the __str__ method for the Crisis model returns the expected string format (crisis_id)
    def test_str_method(self):
        yuance = Crisis.objects.get(your_name="Yuance")
        self.assertEqual(str(yuance), str(yuance.crisis_id))  # Should return the crisis ID as string


    # Test the many-to-many relationship with User (owner)
    def test_owner_relation(self):
        yuance = Crisis.objects.get(your_name="Yuance")
        yuance.owner.add(self.user)
        yuance.save()

        yuance = Crisis.objects.get(your_name="Yuance")
        self.assertIn(self.user, yuance.owner.all())  # Ensure the user is added as an owner


    # Test the visible field behaves correctly, especially in terms of its default value and change
    def test_visibility(self):
        yuance = Crisis.objects.get(your_name="Yuance")
        self.assertTrue(yuance.visible)  # By default, it should be True
        
        yuance.visible = False
        yuance.save()

        yuance.refresh_from_db()  # Refresh the instance
        self.assertFalse(yuance.visible)  # Ensure it has been updated to False


    # Test the `dispatch_trigger` field and its behavior
    def test_dispatch_trigger(self):
        yuance = Crisis.objects.get(your_name="Yuance")
        yuance.dispatch_trigger = True
        yuance.save()

        yuance.refresh_from_db()  # Refresh the instance
        self.assertTrue(yuance.dispatch_trigger)  # Ensure dispatch_trigger is set to True


    # Test the `phone_number_to_notify` field.
    def test_phone_number_to_notify(self):
        yuance = Crisis.objects.get(your_name="Yuance")
        yuance.phone_number_to_notify = '["98765432", "91234567"]'
        yuance.save()

        yuance.refresh_from_db()
        self.assertEqual(yuance.phone_number_to_notify, '["98765432", "91234567"]')  # Check if value is saved correctly

