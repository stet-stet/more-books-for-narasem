import requests
from bs4 import BeautifulSoup
import re
from Kyobo import bookinfo_from_kyobo


def get_isbn(r):
    crit = re.compile("[0-9]{10,15}")
    return int(crit.findall(r.get_text())[0])


def parse(response):
    b = BeautifulSoup(response.text,'html.parser')
    try:
        r = b.find("table",class_="profiletable").tbody
    except AttributeError:
        print()
        return None
    if response.text.find("ISBN") == -1:
        return None
    else:
        try:
            return bookinfo_from_kyobo(get_isbn(r))
        except IndexError:
            return None