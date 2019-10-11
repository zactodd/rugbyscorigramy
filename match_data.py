import datetime

MATCHES = """1,Friday,Sep. 20,A,Japan vs. Russia,19:45,Tokyo Stadium
2,Saturday,Sep. 21,D,Australia vs. Fiji,13:45,Sapporo Dome
3,Saturday,Sep. 21,C,France vs. Argentina,16:15,Tokyo Stadium
4,Saturday,Sep. 21,B,New Zealand vs. South Africa,18:45,International Stadium Yokohama
5,Sunday,Sep. 22,B,Italy vs. Namibia,14:15,Hanazono Rugby Stadium
6,Sunday,Sep. 22,A,Ireland vs. Scotland,16:45,International Stadium Yokohama
7,Sunday,Sep. 22,C,England vs. Tonga,19:15,Sapporo Dome
8,Monday,Sep. 23,D,Wales vs. Georgia,19:15,City of Toyota Stadium
9,Tuesday,Sep. 24,A,Russia vs. Samoa,19:15,Kumagaya Rugby Stadium
10,Wednesday,Sep. 25,D,Fiji vs. Uruguay,14:15,Kamaishi Recovery Memorial Stadium
11,Thursday,Sep. 26,B,Italy vs. Canada,16:45,Fukuoka Hakatanomori Stadium
12,Thursday,Sep. 26,C,England vs. United States,19:45,Kobe Misaki Stadium
13,Saturday,Sep. 28,C,Argentina vs. Tonga,13:45,Hanazono Rugby Stadium
14,Saturday,Sep. 28,A,Japan vs. Ireland,16:15,Shizuoka Stadium Ecopa
15,Saturday,Sep. 28,B,South Africa vs. Namibia,18:45,City of Toyota Stadium
16,Sunday,Sep. 29,D,Georgia vs. Uruguay,14:15,Kumagaya Rugby Stadium
17,Sunday,Sep. 29,D,Australia vs. Wales,16:45,Tokyo Stadium
18,Monday,Sep. 30,A,Scotland vs. Samoa,19:15,Kobe Misaki Stadium
19,Wednesday,Oct. 2,C,France vs. United States,16:45,Fukuoka Hakatanomori Stadium
20,Wednesday,Oct. 2,B,New Zealand vs. Canada,19:15,Oita Stadium
21,Thursday,Oct. 3,D,Georgia vs. Fiji,14:15,Hanazono Rugby Stadium
22,Thursday,Oct. 3,A,Ireland vs. Russia,19:15,Kobe Misaki Stadium
23,Friday,Oct. 4,B,South Africa vs. Italy,18:45,Shizuoka Stadium Ecopa
24,Saturday,Oct. 5,D,Australia vs. Uruguay,14:15,Oita Stadium
25,Saturday,Oct. 5,C,England vs. Argentina,17:00,Tokyo Stadium
26,Saturday,Oct. 5,A,Japan vs. Samoa,19:30,City of Toyota Stadium
27,Sunday,Oct. 6,B,New Zealand vs. Namibia,13:45,Tokyo Stadium
28,Sunday,Oct. 6,C,France vs. Tonga,16:45,Kumamoto Stadium
29,Tuesday,Oct. 8,B,South Africa vs. Canada,19:15,Kobe Misaki Stadium
30,Wednesday,Oct. 9,C,Argentina vs. United States,13:45,Kumagaya Rugby Stadium
31,Wednesday,Oct. 9,A,Scotland vs. Russia,16:15,Shizuoka Stadium Ecopa
32,Wednesday,Oct. 9,D,Wales vs. Fiji,18:45,Oita Stadium
33,Friday,Oct. 11,D,Australia vs. Georgia,19:15,Shizuoka Stadium Ecopa
34,Saturday,Oct. 12,B,New Zealand vs. Italy,13:45,City of Toyota Stadium
36,Saturday,Oct. 12,A,Ireland vs. Samoa,19:45,Fukuoka Hakatanomori Stadium
37,Sunday,Oct. 13,B,Namibia vs. Canada,12:15,Kamaishi Recovery Memorial Stadium
38,Sunday,Oct. 13,C,United States vs. Tonga,14:45,Hanazono Rugby Stadium
39,Sunday,Oct. 13,D,Wales vs. Uruguay,17:15,Kumamoto Stadium
40,Sunday,Oct. 13,A,Japan vs. Scotland,19:45,International Stadium Yokohama"""


# 35,Saturday,Oct. 12,C,England vs. France,17:15,International Stadium Yokohama

DAY_ZERO = "Sep. 20"
TIME_ZERO = "00:00"

TIME_CONCAT = "{} {} 2019"
TIME_FORMAT = "%b. %d %H:%M %Y"
ZERO_DATE = datetime.datetime.strptime(TIME_CONCAT.format(DAY_ZERO, TIME_ZERO), TIME_FORMAT)
SECONDS_PER_DAY = 86400

MATCH_HEADINGS = ["match no", "day", "date", "pool", "teams", "time", "stadium"]
BASE_MATCHES_DATA = [{h: d for h, d in zip(MATCH_HEADINGS, match.split(","))} for match in MATCHES.split("\n")]

DAY_ZERO = "Sep. 20"
TIME_ZERO = "00:00"

TIME_CONCAT = "{} {} 2019"
TIME_FORMAT = "%b. %d %H:%M %Y"


def remaining_matches(matches=BASE_MATCHES_DATA, date=datetime.datetime.now()):
    return [m for m in BASE_MATCHES_DATA if is_match_after(m, date)]


def is_match_after(match_data, date):
    full_str = TIME_CONCAT.format(match_data["date"], match_data["time"])
    match_date = datetime.datetime.strptime(full_str, TIME_FORMAT)
    return match_date - date > datetime.timedelta(0)


def matches_in_pool(matches_data, pool):
    return [m["teams"].split(" vs. ") for m in matches_data if m["pool"] == pool]