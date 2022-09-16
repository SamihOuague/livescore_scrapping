#!/usr/bin/python3
from requests import get
from get_ct import get_cts
from json import dumps
from time import sleep

def get_url(buf):
    url_start = buf.find("/")
    url_end = buf.find("\" ")
    return buf[url_start:url_end]

def get_eq(buf):
    eq_start = buf.find("title=")
    eq_end = buf[eq_start:].find("\">") + eq_start
    spl_buf = buf[eq_start:eq_end].split(":") 
    if len(spl_buf) < 2:
        return ""
    return spl_buf[1].strip()

def get_score(buf):
    scr_start = buf.find("lm3_score")
    scr_start = buf[scr_start:].find(">") + scr_start + 1
    scr_end = buf[scr_start:].find("<") + scr_start
    return buf[scr_start:scr_end]

def get_data(date="04-09-2022"):
    req = get("https://www.matchendirect.fr/resultat-foot-"+date).content.decode()
    results = []
    result_start = 0
    count = 0
    print("getting data...")
    while result_start != -1:
        result_start = req.find('<td class=\"lm3\">')
        result_end = req[result_start:].find('</td>') + result_start + 5
        r = req[result_start:result_end]
        print(get_eq(r))
        print(get_score(r))
        print(get_url(r))
        result = {
            "eq": get_eq(r),
            "score": get_score(r),
            "cts": get_cts(get_url(r))
        }
        if len(result["cts"]) == 0:
            break
        print(result)
        if result["eq"] != '' and result["score"] != '':
            results.append(result)
        req = req[result_end:]
        count += 1
        if count > 20:
            break
    f = open(date+".json", "w")
    f.write(dumps(results))
    f.close()

i = 5
while i < 15:
    if i < 10:
        d = "0" + str(i)
    else:
        d = str(i)
    d = d + "-09-2022"
    get_data(d)
    sleep(1)
    i += 1
