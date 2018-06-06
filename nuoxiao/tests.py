from django.test import TestCase
from rest_framework.test import APIRequestFactory
import json


# Create your tests here.
factory = APIRequestFactory()
# request = factory.post('/tag/', {'name': 'new idea'})
request = factory.get('/tag/', {'name': 'new idea'}, format='json')

request = factory.post('/tag/', json.dumps({'name': 'new idea'}), content_type='application/json')