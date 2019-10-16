import datetime

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline

from match_data import BASE_MATCHES_DATA, TIME_CONCAT, TIME_FORMAT, ZERO_DATE, SECONDS_PER_DAY

RANKINGS = """1,(2),NEW ZEALAND,89.40,
2,(4),IRELAND,88.86,
3,(3),ENGLAND,88.13,
4,(1),WALES,87.92,
5,(5),SOUTH AFRICA,86.83,
6,(6),AUSTRALIA,84.05,
7,(7),SCOTLAND,81.00,
8,(8),FRANCE,79.72,
9,(10),FIJI,77.43,
10,(9),JAPAN,77.21,
11,(11),ARGENTINA,76.29,
12,(12),GEORGIA,73.29,
13,(13),ITALY,72.04,
14,(14),UNITED STATES,71.93,
15,(15),TONGA,71.04,
16,(16),SAMOA,69.08,
19,(19),URUGUAY,65.18,
20,(20),RUSSIA,64.81,
21,(21),CANADA,61.36,
23,(23),NAMIBIA,61.01"""

RANKINGS_DICT = {}
for r in RANKINGS.split(",\n"):
    rank, _, country, points = r.split(",")
    RANKINGS_DICT.update({country: (int(rank), float(points))})


def rel_data(data):
    new_data = []
    for r in data:
        t1, t2 = r["teams"].split(" vs. ")
        t1, t2 = t1.upper(), t2.upper()
        rd = RANKINGS_DICT[t1][0] - RANKINGS_DICT[t2][0]
        pd = RANKINGS_DICT[t1][1] - RANKINGS_DICT[t2][1]

        new_row = {
            "teams": (t1, t2),
            "rd": (rd, -rd),
            "pd": (-pd, pd),
            "rel_date": time_from_zero(r["date"], r["time"])
        }
        new_data.append(new_row)
    return new_data


def time_from_zero(date_str, time_str):
    full_str = TIME_CONCAT.format(date_str, time_str)
    date = datetime.datetime.strptime(full_str, TIME_FORMAT)
    return date - ZERO_DATE


def team_curve(data, team, par="rd"):
    team = team.upper()
    points = [(0, 0)]
    for d in data:
        if team not in d["teams"]:
            continue
        i = d["teams"].index(team)
        days = d["rel_date"].days + d["rel_date"].seconds / SECONDS_PER_DAY
        points.append((d[par][i], days))
    return points


def cuveify(x, y, p=50):
    new_x = np.linspace(min(x), max(x), p)
    new_y = spline(x, y, new_x)
    return new_x, new_y


for c in RANKINGS_DICT:
    rds, time = zip(*team_curve(rel_data(BASE_MATCHES_DATA), c, "rd"))
    if all(r >= 0 for r in rds):
        print(c)
        x, y = cuveify(time, rds)

        plt.plot(x, y)

plt.show()
