import pytest
import requests
import time

def test_mytest():
    r = requests.get("http://localhost:8080")
    assert "Tiger Advanced" in r.text

def test_AuthTest():
    data = {'username': 'test', 'password': 'test'}
    r = requests.post("http://127.0.0.1:8080/login", data=data)
    print("Authentication tests----------------")
    assert 'Welcome' in r.text
    print("Correct authentication: passed")
    time.sleep(0.01)

    data = {'username': 'testwrong', 'password': 'test'}
    r = requests.post("http://127.0.0.1:8080/login", data=data)
    assert 'Invalid' in r.content.decode('UTF-8')
    print("Wrong username authentication: passed")
    time.sleep(0.01)

    data = {'username': 'test', 'password': 'testwrong'}
    r = requests.post("http://127.0.0.1:8080/login", data=data)
    assert 'Invalid' in r.content.decode('UTF-8')
    print("Wrong password authentication: passed")

def test_uploadVid():
    data = {'username': 'test', 'password': 'test'}
    r = requests.post("http://127.0.0.1:8080/login", data=data)
    