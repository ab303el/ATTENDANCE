from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Employee

class AttendanceTests(APITestCase):

    def setUp(self):
        # 1. This triggers the signal which creates an Employee automatically
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # 2. Fetch the automatically created employee and update the fields
        self.employee = self.user.employee 
        self.employee.first_name = "Test Bob"
        self.employee.last_name = "Test jack"
        self.employee.email = "abc@gmail.com"
        self.employee.employee_id = "101"
        self.employee.save()
        
        self.url = reverse('attendance-list-create')


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
        login_url = reverse('token_obbtain_pair')
        login_res = self.client.post(login_url, {'username': 'testuser', 'password': 'password123'})
        token = login_res.data['access']

        # 2. Use the token to hit the attendance endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if pagination is working (look for 'results' key)
        self.assertIn('results', response.data)