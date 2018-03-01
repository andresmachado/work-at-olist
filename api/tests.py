from datetime import datetime

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Call


# Create your tests here.


class CallTests(APITestCase):
    def setUp(self):
        self.call_data = {
            "source": '47987987987',
            "destination": '19123123123',
            "timestamp": "2018-02-27T20:57:13"
        }

        self.assert_keys = ['identifier', 'source', 'destination',
                            'call_start', 'duration', 'call_end', 'price']

    def test_api_should_allow_any(self):
        url = reverse('call-list')

        response = self.client.get(url)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
        self.assertEqual(call_object.starts_at.timestamp, datetime(2018, 2, 27, 20, 57, 13))
        self.assertEqual(call_object.has_ended, False)

    def test_end_call(self):
        url = reverse('call-list')

        started_call = self.client.post(url, self.call_data, format='json')
        identifier = started_call.data.get('identifier')

        end_call_url = '/api/v1/calls/{0}/end-call/'.format(identifier)

        end_call_data = {
            'identifier': identifier,
            'timestamp': "2018-02-27T21:03:23"
        }

        response = self.client.put(end_call_url, end_call_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.data.keys(), self.assert_keys)
        self.assertEqual(response.data['duration'], "0h6m10s")

    def test_call_should_not_end_in_past(self):
        url = reverse('call-list')

        started_call = self.client.post(url, self.call_data, format='json')
        identifier = started_call.data.get('identifier')

        end_call_url = '/api/v1/calls/{0}/end-call/'.format(identifier)

        end_call_data = {
            'identifier': identifier,
            'timestamp': "2018-02-27T20:03:23"
        }

        response = self.client.put(end_call_url, end_call_data, format='json')
        msg = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(msg, 'End call timestamp cannot be in the past.')

    def test_start_call_with_wrong_source_number_should_fail(self):
        url = reverse('call-list')

        self.call_data.update({'source': '90033399'})

        response = self.client.post(url, self.call_data, format='json')

        msg = response.data['source'][0]

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            msg, 'Phone numbers must have 8-9 digits and must be in format AAXXXXXXXXX.')

    def test_start_call_with_wrong_destination_number_should_fail(self):
        url = reverse('call-list')

        self.call_data.update({'destination': '90033399'})

        response = self.client.post(url, self.call_data, format='json')
        msg = response.data['destination'][0]

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            msg, 'Phone numbers must have 8-9 digits and must be in format AAXXXXXXXXX.')

    def test_start_call_with_same_numbers_should_fail(self):
        url = reverse('call-list')

        self.call_data.update({'destination': '47987987987'})

        response = self.client.post(url, self.call_data, format='json')
        msg = response.data['non_field_errors'][0]

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertCountEqual(response.data, ['non_field_errors'])
        self.assertEqual(msg, 'The phone numbers must be different.')
