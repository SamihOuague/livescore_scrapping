#!/usr/bin/python3
from requests import get
from time import sleep

def extract_ct(buf):
    ct1_start = buf.find("class=\"c2\"") + 11
    ct1_end = buf[ct1_start:].find("<") + ct1_start
    return buf[ct1_start:ct1_end].strip()

def get_cts(url):
    req = get("https://www.matchendirect.fr" + url).content.decode()

    ct_start = req.find("class=\"ct\"")
    ct_end = req[ct_start:].find("</div>") + ct_start

    r = req[ct_start:ct_end]
    cts = []

    while r.find("class=\"c2\"") != -1:
        ct = extract_ct(r)
        pos = r.find(ct)
        print(r)
        r = r[pos:]
        cts.append(ct)
        sleep(1)
    sleep(2)
    
    return cts

get_cts("/live-score/chaves-rio-ave.html")

