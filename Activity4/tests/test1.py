import pytest
import requests

def test_mytest():
    r = requests.get("http://127.0.0.1:80")
    assert "Hello World" in r.text
