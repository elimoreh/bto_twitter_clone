from django.test import TestCase
from django.contrib.auth.models import User

from .models import Tweet

# Create your tests here.
# class TestTrendingView(TestCase):
#     def setUp(self):
        
#         Tweet.objects.create(name="lion", sound="roar")
#         Tweet.objects.create(name="cat", sound="meow")

#     def test_animals_can_speak(self):
#         """Animals that can speak are correctly identified"""
#         lion = Animal.objects.get(name="lion")
#         cat = Animal.objects.get(name="cat")
#         self.assertEqual(lion.speak(), 'The lion says "roar"')
#         self.assertEqual(cat.speak(), 'The cat says "meow"')