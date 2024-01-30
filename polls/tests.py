import json
from django.test import TestCase
from django.urls import reverse
from datetime import datetime
import re

class ViewTests(TestCase):

    
    def test_index_view(self):
        url = "http://127.0.0.1:8000/polls/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        


    def test_prowadzacy_view(self):
        url = "http://127.0.0.1:8000/polls/prow"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Odczytanie zawartości odpowiedzi jako JSON z uwzględnieniem kodowania UTF-8
        content = response.content.decode('utf-8')
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            self.fail("Odpowiedź nie jest poprawnym JSON-em")
        finally:
            print("URL prowadzący działa poprawnie")
    

    def test_plan_view(self):
        url = "http://127.0.0.1:8000/polls/plan/stud/js?grupa=WCY20IK1S0"
        print(url)
        response = self.client.get(url, data = {'grp':'WCY20IK1S0'})
        self.assertEqual(response.status_code, 200)
        
