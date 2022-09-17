from msilib.schema import SelfReg
from random import randrange
from rest_framework.test import APIClient
from rest_framework import status
from custom_auth.models import *
import pytest

def rand_username():
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


@pytest.mark.django_db
class TestCreation:    
    def test_is_member_created_all_values(self):
        client = APIClient()
        req_body = {
            "username": rand_username(),
            **member_body
        }
        res = client.post("/auth/register/", req_body)
        print(res)
        assert res.status_code == status.HTTP_201_CREATED
        assert Member.objects.filter(user__pk=res.data['id']).exists()
        assert Librarian.objects.filter(user__pk=res.data['id']).exists() == False
        
    def test_is_librarian_created_all_values(self):
        client = APIClient()
        
        req_body = {
            'username': rand_username(),
            **librarian_body
        }        
        res = client.post("/auth/register/", req_body)
        assert res.status_code == status.HTTP_201_CREATED
        assert Librarian.objects.filter(user__pk=res.data['id']).exists()
        assert Member.objects.filter(user__pk=res.data['id']).exists() == False

    def test_member_with_existing_user(self):
        client = APIClient()
        req_body = {
            "username": rand_username(),
            **member_body
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
            "username": rand_username(),
            **librarian_body
        }
        res1 = client.post("/auth/register/", req_body)
        res2 = client.post("/auth/register/", req_body)
        assert res1.status_code == status.HTTP_201_CREATED
        assert res2.status_code == status.HTTP_400_BAD_REQUEST
        assert Librarian.objects.filter(user__pk=res1.data['id']).exists()
        assert Member.objects.filter(user__pk=res1.data['id']).exists() == False
    
    def test_user_without_username(self):
        client = APIClient()
        res = client.post("/auth/register/", member_body)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_user_without_password(self):
        client = APIClient()
        req_body = {
            'username': rand_username(),
            **member_body
        }
        req_body.pop('password')
        res = client.post("/auth/register/", req_body)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_password_not_matching(self):
        client = APIClient()
        req_body = {
            'username': rand_username(),
            **member_body
        }
        req_body['confirm_password'] = '123456789'
        res = client.post("/auth/register/", req_body)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_user_with_wrong_email(self):
        client = APIClient()
        req_body = {
            'username': rand_username(),
            **member_body
        }
        req_body['email'] = 'abc'
        res = client.post("/auth/register/", req_body)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        

@pytest.mark.django_db
class TestLibrarien:
    client = APIClient()
    def test_librarien_retrieved_without_credentials_return_401(self):
        res = self.client.get("/auth/librarien/")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_librarien_with_member_cred_returns_401(self):
        client = APIClient()
        req_body = {
            "username": rand_username(),
            **member_body
        }
        client.post("/auth/register/", req_body)
        access = client.post("/auth/login", {'username': req_body['username'], 'password': req_body['password']})
        access = access.data['access']
        client.credentials(HTTP_AUTHORIZATION='JWT ' + access)
        res = client.get("/auth/librarien/")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_librarien_with_librarien_cred_returns_200(self):
        client = APIClient()
        req_body = {
            "username": rand_username(),
            **librarian_body
        }
        print(req_body)
        client.post("/auth/register/", req_body)
        access = client.post("/auth/login", {'username': req_body['username'], 'password': req_body['password']})
        access = access.data.get('access')
        client.credentials(HTTP_AUTHORIZATION='JWT ' + access)
        res = client.get("/auth/librarien/")
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 1
                