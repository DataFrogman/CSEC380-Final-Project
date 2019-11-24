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

def test_uploadAndDeleteVid():
    sess = requests.session()
    data = {'username': 'test', 'password': 'test'}
    r = sess.post("http://127.0.0.1:8080/login", data=data)
    data = {'file': open('tests/Rick_Astley_Never_Gonna_Give_You_Up.mp4', 'rb')}
    r = sess.post("http://127.0.0.1:8080/manage", files=data)
    r = sess.get("http://127.0.0.1:8080/homepage")
    assert 'Rick_Astley_Never_Gonna_Give_You_Up.mp4' in r.content.decode('UTF-8')
    data = { 'videoid': '1'}
    r = sess.post("http://127.0.0.1:8080/delete", data=data)
    r = sess.get("http://127.0.0.1:8080/homepage")
    assert 'No Videos to Display!' in r.content.decode('UTF-8')

