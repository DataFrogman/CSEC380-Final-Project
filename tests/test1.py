import pytest
import requests

def test_mytest():
    r = requests.get("http://127.0.0.1:8080")
    assert "Tiger Advanced" in r.text

def AuthTest():
    data = {'username': 'test', 'password': 'test'}
    r = requests.get("http://127.0.0.1:8080", data=data)
    print("Authentication tests----------------")
    assert 'Welcome' in r.text
    print("Correct authentication: passed")

    data = {'username': 'testwrong', 'password': 'test'}
    r = requests.get("http://127.0.0.1:8080", data=data)
    assert 'Invalid' in r.text
    print("Wrong username authentication: passed")

     data = {'username': 'test', 'password': 'testwrong'}
    r = requests.get("http://127.0.0.1:8080", data=data)
    assert 'Invalid' in r.text
    print("Wrong password authentication: passed")

