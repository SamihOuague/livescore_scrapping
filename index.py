#!/usr/bin/python3
from requests import get
from bs4 import BeautifulSoup
from time import sleep

def get_min_ct(cts):
    cts = [float(x) for x in cts]
    ct_index = 0
    ct_v = cts[0]
    for i in range(1, len(cts)):
        if ct_v > cts[i]:
            ct_index = i
    return ct_index

def wwin(score):
    score = [int(x.strip()) for x in score.split("-")]
    who_win = 0
    if score[0] > score[1]:
        who_win = 1
    elif score[0] < score[1]:
        who_win = 2
    return who_win

html_doc = get("https://www.pronosoft.com/fr/parions_sport/resultats-parions-sport-plein-ecran.htm").content
soup = BeautifulSoup(html_doc, 'html.parser')
nb_win = 0
nb_trade = 0
wallet = 50
risk = 1
for tag in soup.find_all('tr'):
    if tag.has_attr('class') and 'm-s-0' in tag['class']:
        t = tag.a
        r = tag.find("td", {"class": "res"}).contents
        if len(t.contents) >= 2 and len(r) > 0:
            score = r[0]
            equipe = t.contents[1]
            ct_tds = tag.find_all("td")
            cts = [ct_tds[5].get_text(), ct_tds[6].get_text(), ct_tds[7].get_text()];
            try:
                cts = [float(x.replace(",", ".")) for x in cts]
                min_ct = get_min_ct(cts)
                if min_ct == 0 and cts[min_ct] >= 2:
                    nb_trade += 1
                    if wwin(score) == 1:
                        print("\033[32m", equipe, cts[min_ct], "WIN!!\033[37m", score, risk)
                        wallet = wallet + (risk * cts[min_ct]) - risk
                        nb_win += 1
                        risk = 1
                    else:
                        print("\033[31m", equipe, cts[min_ct], "LOSS!!\033[37m", score, risk)
                        wallet = wallet - risk
                        risk = risk * 2
                    if risk > wallet:
                        print("You've lost : {}$".format(round(wallet)))
                        break
                    print("Profit : {}$".format(round(wallet)))
                    sleep(1)
            except:
                pass

winRate = round((nb_win/nb_trade)*100)
print("Taux de reussite : {}%".format(winRate))
print("Nombre de trade : {}".format(nb_trade))
print("Profit : {}$".format(round(wallet)))
