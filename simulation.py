#!/usr/bin/python3
from json import loads

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
        

for p in pronos:
    w = wwin(p["score"])
    c = get_min_ct(p["cts"])
    if float(p["cts"][c]) >= 2:
        if (c == 0 and w == 1) or (c == 2 and w == 2) or (c == 1 and w == 0):
            print("\033[32m", p["eq"], p["cts"][c], "WIN!!\033[37m", p["score"])
        else:
            print("\033[31m", p["eq"], p["cts"][c], "LOSS!!\033[37m", p["score"])

