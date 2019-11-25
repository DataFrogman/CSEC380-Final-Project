import pytest
import requests
from bs4 import BeautifulSoup
from subprocess import Popen,PIPE,STDOUT,call

def test_exe():
    r = requests.post("http://localhost:8080/login", {"username": "admin", "password": "admin"}).text
    r = requests.post("http://localhost:8080/downloadVideo/requirements.txt", {"username": "admin"})
    print(r.content.decode("UTF-8"))

    assert "flask" in r.content.decode("UTF-8")

if __name__ == "__main__":
    test_exe()
