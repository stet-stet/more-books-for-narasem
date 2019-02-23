import requests
from bs4 import BeautifulSoup
from time import sleep

def bookinfo_from_kyobo(isbn):
    r = requests.get("http://www.kyobobook.co.kr/product/detailViewKor.laf",
                     params={
                         "ejkGb": "KOR",
                         "mallGb": "KOR",
                         "barcode": isbn,
                         "orderClick": "LET",
                         "Kc": "",
                     },
                     headers={
                         'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
                         'Accept-Encoding': 'gzip, deflate',
                         'Accept-Language': 'en-US,en;q=0.5',
                         'Accept': "*/*",
                         'Connection': 'keep-alive',
                     })
    if len(r.text) < 10000:
        print("english.")
        sleep(1)
        r = requests.get("http://www.kyobobook.co.kr/product/detailViewEng.laf",
                         params={
                             "ejkGb": "BNT",
                             "mallGb": "ENG",
                             "barcode": isbn,
                             "orderClick": "LAG",
                             "Kc": "",
                         },
                         headers={
                             'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
                             'Accept-Encoding': 'gzip, deflate',
                             'Accept-Language': 'en-US,en;q=0.5',
                             'Accept': "*/*",
                             'Connection': 'keep-alive',
                         })
    if len(r.text)<10000:
        print("There is no such page")
        return None
    else:
        ret = {}
        try:
            bsObj = BeautifulSoup(r.text, 'html.parser')
            print(len(bsObj.get_text()))
            # isbn
            ret['isbn'] = isbn
            ret['price'] = bsObj.find_all("span", class_="org_price")[0].get_text().strip().strip('원')
            # title
            ret['title'] = bsObj.find_all("meta", property="og:title")[0]["content"]
            data_bundle = bsObj.find_all("div", class_="author")[0]
            ret['publisher']=data_bundle.find("span", class_="name", title="출판사").get_text().strip()
            ret['year'] = data_bundle.find("span", class_="date", title="출간일").get_text().strip().split(' ')[0]
            authorTemp = bsObj.find("div", class_="box_detail_point")
            temp = authorTemp.find("div", class_="author").find("span",class_="name").get_text().strip()
            if temp.find("작가상세정보") == -1:
                ret['author'] = temp
            else:
                ret['author'] = temp[:temp.find("작가상세정보")].strip()
        except IndexError:
            print("wrong index!")
        finally:
            print(ret)
            return ret
        # data: isbn, book title, author, publisher, year, price, (keyword)
        # the 갯수?

"""
from bfn.scraputil.Kyobo import bookinfo_from_kyobo
bookinfo_from_kyobo(9788968484698)
"""