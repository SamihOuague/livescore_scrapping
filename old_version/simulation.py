#!/usr/bin/python3
from json import loads
from time import sleep

pronos = loads(open("04-09-2022.json", "r").read())

def wwin(score):
    score = [int(x.strip()) for x in score.split("-")]
    who_win = 0
    if score[0] > score[1]:
        who_win = 1
    elif score[0] < score[1]:
        who_win = 2
    return who_win

def get_min_ct(cts):
    cts = [float(x) for x in cts]
    ct_index = 0
    ct_v = cts[0]
    for i in range(1, len(cts)):
        if ct_v > cts[i]:
            ct_index = i
    return ct_index
        
i = 3
nb_trade = 0
nb_win = 0
wallet = 10
init_risk = 1
risk = init_risk
ct_min = 1.5
while i < 15:
    if i < 10:
        d = "0" + str(i)
    else:
        d = str(i)
    d = d + "-09-2022.json"
    pronos = loads(open(d, "r").read())
    c = 0
    for p in pronos:
        w = wwin(p["score"])
        c = get_min_ct(p["cts"])
        if float(p["cts"][c]) >= ct_min and c == 0:
            nb_trade += 1
            if (c == 0 and w == 1) or (c == 2 and w == 2) or (c == 1 and w == 0):
                print("\033[32m", p["eq"], p["cts"][c], "WIN!!\033[37m", p["score"])
                wallet += (float(p["cts"][c]) * risk) - risk
                nb_win += 1
                c += 1
                risk = init_risk
                print(wallet)
                sleep(0.5)
                #if c == 1:
                #    break
            else:
                print("\033[31m", p["eq"], p["cts"][c], "LOSS!!\033[37m", p["score"])
                wallet -= risk
                c += 1
                risk = risk * 2
                print(wallet)
                sleep(0.5)
                #if c == 1 or risk > wallet:
                #    break
    if risk > wallet:
        break
    i += 1

print("win = {} /".format(nb_win), "trades = {} /".format(nb_trade), "win rate = {}%".format(round((nb_win/nb_trade)*100)))
print(wallet)
