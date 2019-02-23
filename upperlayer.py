import requests
from bs4 import BeautifulSoup
from time import sleep
import check_for_crit
import csv

def get_page(pn,q):
    r = requests.get(url="http://lib1.kostat.go.kr/search/tot/result",
                 params={
                     "pn": pn,
                     "q": q,
                     "st": "KWRD",
                     "si": "TOTAL",
                 })
    if r.text.find("검색 결과가 없습니다.") > -1:
        return None
    else:
        return r


def gather_book_links(keyword):
    ret=[]
    for i in range(1,1000):
        r = get_page(pn=i,q=keyword)
        sleep(1)
        if r is None:
            break
        b = BeautifulSoup(r.text,'html.parser')
        c = b.find("table",id="briefTable")
        ret.extend(["http://lib1.kostat.go.kr"+i["href"] for i in c.find_all("a")])
    print(len(ret))
    return ret


def filter(l):
    ret=[]
    for url in l:
        r = requests.get(url)
        if r.text.find("나라셈도서관/") == -1 and (r.text.find("통계도서관/")>-1 or r.text.find("통계교육원도서관/")>-1):
            ret.append(r)
    return ret


def extract_info_from_each(r):
    dict_list=[]
    for i in r:
        ret = check_for_crit.parse(i)
        if ret is not None:
            dict_list.append(ret)
    return dict_list


def save_as_csv(dict_list,filename):
    fields=list(dict_list[0].keys())
    with open(filename+".csv", 'w+', newline='') as csvfile:
        w = csv.writer(csvfile)
        w.writerow(fields)
        for entry in dict_list:
            row=[]
            for field in fields:
                row.append(entry[field])
            w.writerow(row)


def run():
    r = []
    r.extend(gather_book_links("310.111"))
    r.extend(gather_book_links("310.112"))
    r.extend(gather_book_links("310.113"))
    return r


def run2(l):
    return extract_info_from_each(l)


def run3(dl):
    save_as_csv(dl,"results")


def runny():
    l = run()
    print(len(l))
    ll = filter(l)
    print(len(ll))
    lll = run2(ll)
    print(len(lll))
    run3(lll)
    with open("fulllist.txt","w+") as f:
        for i in ll:
            f.write(i.url+"\n")