import pytest
import requests
from bs4 import BeautifulSoup
from subprocess import Popen,PIPE,STDOUT,call

def test_exe():
    r = requests.post("http://localhost:8080/login", {"username": "admin", "password": "admin"}).text
    r = requests.post("http://localhost:8080/homepage", {"username": "admin", "file": "test.mp4 && rm requirements.txt"})

    proc=Popen('sudo docker container exec -it webserver ls', shell=True, stdout=PIPE, )
    output=proc.communicate()[0]
    print(output)
    output = output.decode("utf-8")
    assert "requirements.txt" not in output

if __name__ == "__main__":
    test_exe()
