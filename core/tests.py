from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Employee

class AttendanceTests(APITestCase):
    def setUp(self):
        # This runs before every test to "set the stage"
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.employee = Employee.objects.create(user=self.user, name="Test Bob", employee_id="101")
        self.url = reverse('attendance-list-create') # Matches the name in urls.py

    def test_unauthenticated_user_fails(self):
        """
        Real-world principle: Ensure our security actually blocks people.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_list_attendance(self):
        """
        Verify that once logged in, we get a 200 OK and a paginated list.
        """
        # 1. Get the token
        login_url = reverse('token_obtain_pair')
        login_res = self.client.post(login_url, {'username': 'testuser', 'password': 'password123'})
        token = login_res.data['access']

        # 2. Use the token to hit the attendance endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if pagination is working (look for 'results' key)
        self.assertIn('results', response.data)