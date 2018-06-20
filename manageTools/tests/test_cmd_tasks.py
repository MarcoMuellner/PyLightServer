import pytest
import os

from django.test import Client
from django.urls import reverse

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

@pytest.fixture(scope='module')
def moduleSetup(request):
    return Client()

def test_signup(moduleSetup : Client):
    response = moduleSetup.post(reverse("PyLightCommon.cmdHandler:commandHandler"),
                               data={"commando": "Signup||123456||127.0.0.1||0x.0x.0x.0x||True||True"})
    assert response.status_code == 200
    assert response.content.decode() == "Ok"

def test_alive(moduleSetup : Client):
    response = moduleSetup.post(reverse("PyLightCommon.cmdHandler:commandHandler"),data={"commando":"Alive"})
    assert response.status_code == 200
    assert response.content.decode() == "Ok"