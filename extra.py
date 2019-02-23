import requests
from bs4 import BeautifulSoup


escapechar = "\r\n"

def readurls():
    urls = []
    with open("fulllist.txt", "r") as f:
        for i in f.readlines():
            urls.append(i.strip())
    return urls


def readdata(url):
    r = requests.get(url)
    b = BeautifulSoup(r.text, 'html.parser')
    return b.find("table", class_="profiletable").get_text()

def run():
    ret = []
    l = readurls()
    for url in l:
        ret.append(readdata(url))
    with open("otherlist.txt", "w+") as f:
        for i in ret:
            f.write(i.replace('\n', '\r\n'))
            f.write("\r\n---------------------------\r\n")
