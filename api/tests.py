from datetime import datetime

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Call
from .serializers import CallSerializer


# Create your tests here.


class CallTests(APITestCase):
    def setUp(self):
        self.call_data = {
            "source": '47987987987',
            "destination": '19123123123',
            "timestamp": "2018-02-27T22:57:13"
        }

    def test_list_calls(self):
        url = reverse('call-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_call_record(self):
        url = reverse('call-list')

        response = self.client.post(url, self.call_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Call.objects.count(), 1)

    def test_call_should_not_has_ended(self):
        url = reverse('call-list')

        response = self.client.post(url, self.call_data, format='json')
        identifier = response.data.get('identifier')

        call_object = Call.objects.get(identifier=identifier)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(call_object.starts_at.timestamp, datetime(2018, 2, 27, 22, 57, 13))
        self.assertEqual(call_object.has_ended, False)