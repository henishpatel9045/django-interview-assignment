from msilib.schema import SelfReg
from random import randrange
from rest_framework.test import APIClient
from rest_framework import status
from custom_auth.models import *
import pytest

@pytest.mark.django_db
class TestCreation:
    def rand_username(self):
        tmp = [ascii(ord('a')+i) for i in range(26)]
        username = "".join([tmp[randrange(0, 26)] for i in range(8)])
        return username

    librarian_body = {
            "password": "1234567890",
            "confirm_password": "1234567890",
            "first_name": "Henish",
            "last_name": "Patel",
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
    
    def test_is_member_created_all_values(self):
        client = APIClient()
        req_body = {
            "username": self.rand_username(),
            **self.member_body
        }
        res = client.post("/auth/register/", req_body)
        print(res)
        assert res.status_code == status.HTTP_201_CREATED
        assert Member.objects.filter(user__pk=res.data['id']).exists()
        assert Librarian.objects.filter(user__pk=res.data['id']).exists() == False
        
    def test_is_librarian_created_all_values(self):
        client = APIClient()
        
        req_body = {
            'username': self.rand_username(),
            **self.librarian_body
        }        
        res = client.post("/auth/register/", req_body)
        assert res.status_code == status.HTTP_201_CREATED
        assert Librarian.objects.filter(user__pk=res.data['id']).exists()
        assert Member.objects.filter(user__pk=res.data['id']).exists() == False

    def test_member_with_existing_user(self):
        client = APIClient()
        req_body = {
            "username": self.rand_username(),
            **self.member_body
        }
        res1 = client.post("/auth/register/", req_body)
        res2 = client.post("/auth/register/", req_body)
        assert res1.status_code == status.HTTP_201_CREATED
        assert res2.status_code == status.HTTP_400_BAD_REQUEST
        assert Member.objects.filter(user__pk=res1.data['id']).exists()
        assert Librarian.objects.filter(user__pk=res1.data['id']).exists() == False
    
    def test_librarian_with_existing_user(self):
        client = APIClient()
        
        req_body = {
            "username": self.rand_username(),
            **self.librarian_body
        }
        res1 = client.post("/auth/register/", req_body)
        res2 = client.post("/auth/register/", req_body)
        assert res1.status_code == status.HTTP_201_CREATED
        assert res2.status_code == status.HTTP_400_BAD_REQUEST
        assert Librarian.objects.filter(user__pk=res1.data['id']).exists()
        assert Member.objects.filter(user__pk=res1.data['id']).exists() == False
    
    def test_user_without_username(self):
        client = APIClient()
        res = client.post("/auth/register/", self.member_body)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_user_without_password(self):
        client = APIClient()
        req_body = {
            'username': self.rand_username(),
            **self.member_body
        }
        req_body.pop('password')
        res = client.post("/auth/register/", req_body)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_password_not_matching(self):
        client = APIClient()
        req_body = {
            'username': self.rand_username(),
            **self.member_body
        }
        req_body['confirm_password'] = '123456789'
        res = client.post("/auth/register/", req_body)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_user_with_wrong_email(self):
        client = APIClient()
        req_body = {
            'username': self.rand_username(),
            **self.member_body
        }
        req_body['email'] = 'abc'
        res = client.post("/auth/register/", req_body)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        
    