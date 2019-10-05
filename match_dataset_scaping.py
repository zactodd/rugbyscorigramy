import requests
from lxml import html

ESPN_SCRUM = "http://stats.espnscrum.com/statsguru/rugby/stats/index.html"


def query_url(url, queries):
    return "{}?{}".format(url, ";".join("{}={}".format(k, v) for k, v in queries.items()))


def espnscrum_query(page=1):
    return {
        "class": 1,
        "page": page,
        "template": "results",
        "type": "team",
        "view": "match"
    }


def page_rows(page):
    r = requests.get(query_url(ESPN_SCRUM, espnscrum_query(page)))
    tree = html.fromstring(r.content)
    table_rows_str = "//div[@id='scrumArticlesBoxContent']/table[@class='engineTable']/*/tr"
    rows = []
    for i in range(1, len(tree.xpath(table_rows_str))):
        first, lower_middle = tree.xpath("{}[{}]/td/a/text()".format(table_rows_str, i))
        *upper_middle, last = tree.xpath("{}[{}]/td/text()".format(table_rows_str, i))
        rows.append(list((first, *upper_middle, lower_middle, last)))
    return rows


def pages_range(start, finish):
    rows = []
    for i in range(start, finish):
        rs = page_rows(i)
        if len(rs) == 0:
            break
        rows.extend(rs)
    return rows


def page_range(finish):
    return pages_range(1, finish)


def headers():
    r = requests.get(query_url(ESPN_SCRUM, espnscrum_query()))
    tree = html.fromstring(r.content)
    headers_str = "//div[@id='scrumArticlesBoxContent']/table[@class='engineTable']/*/tr[@class='headlinks']"
    *front, last = tree.xpath("{}/th/a/text()".format(headers_str))
    middle = tree.xpath("{}/th/text()".format(headers_str))
    return tuple((*front, *middle, last))


HEADERS = headers()

