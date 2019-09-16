import pytest
import requests

def test_mytest():
    r = requests.get(‘webserver:80’)
    assert "Hello" in r.text
