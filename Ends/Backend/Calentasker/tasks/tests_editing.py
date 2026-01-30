from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from tasks.models import Task
from django.utils import timezone
from datetime import timedelta

class TaskEditingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(
            title='Old Title',
            description='Old Desc',
            priority='low',
            created_by_userid=self.user
        )

    def test_update_task_details(self):
        url = f'/api/tasks/{self.task.id}/'
        new_due = (timezone.now() + timedelta(days=5)).date()
        new_start = timezone.now().date()
        data = {
            'title': 'New Title',
            'description': 'New Desc',
            'priority': 'high',
            'due_date': new_due.isoformat(),
            'start_date': new_start.isoformat()
        }
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'New Title')
        self.assertEqual(self.task.description, 'New Desc')
        self.assertEqual(self.task.priority, 'high')
        self.assertEqual(self.task.due_date, new_due)
        self.assertEqual(self.task.start_date, new_start)

    def test_update_task_clear_dates(self):
        url = f'/api/tasks/{self.task.id}/'
        # Set dates first
        self.task.due_date = timezone.now().date()
        self.task.save()
        
        data = {
            'due_date': None,
            'start_date': None
        }
        response = self.client.patch(url, data, format='json') # json format needed for null
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.task.refresh_from_db()
        self.assertIsNone(self.task.due_date)
        self.assertIsNone(self.task.start_date)

    def test_update_task_partial(self):
        url = f'/api/tasks/{self.task.id}/'
        data = {'title': 'Only Title Changed'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Only Title Changed')
        self.assertEqual(self.task.description, 'Old Desc')
