from random import randrange
from rest_framework import status
from rest_framework.test import APIClient
from library.models import *
import pytest

@pytest.mark.django_db
class TestCategory:
    body = {
        'category': "Tech",
        'description': "About Technology",
        'stack_placed': 'A10',
    }
    
    def rand_username(self):
        tmp = [ascii(ord('a')+i) for i in range(26)]
        username = "".join([tmp[randrange(0, 26)] for i in range(8)])
        return username

    librarian_body = {
            "password": "1234567890",
            "confirm_password": "1234567890",
            "first_name": "Henish",
            "last_name": "Patel",
            "email": "ompatle@gml.com",
            "sign_up_as": "Librarian",
            "phone_number": "7990577979",
            "address": "Vadnagar",
            "pin_code": "384355"
    }
    
    member_body = {
        **librarian_body,
        "aadhaar_card_id": "91596453245",
        "date_of_birth": "2002-09-05",
        "sign_up_as": "Member",
    }
    
    
    def test_category_without_access_token_returns_401(self):
        client = APIClient()
        res = client.post("/category/", self.body)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_category_create_by_member_return_401(self):
        client = APIClient()
        member = {
            'username': self.rand_username(),
            **self.member_body
        }
        res1 = client.post("/auth/register/", member)
        auth = {
            'username': member.get("username"),
            "password": member.get("password")
        }
        jwt = client.post("/auth/login", auth)
        client.credentials(HTTP_AUTHORIZATION='JWT ' + jwt.data.get("access"))
        res = client.post("/category/", self.body)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        res = client.post("/book/", {})
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        
        