import requests
from lxml import html
import datetime
import csv
import tqdm


class IDataScrapper:
    def __init__(self):
        self.headers = None
        self.data = None

    def collect_data(self):
        raise NotImplementedError()

    def collect_headers(self):
        raise NotImplementedError()

    def get_data_headers(self):
        if self.headers is None:
            self.headers = self.collect_headers()
        return self.headers

    def get_data(self):
        if self.data is None:
            self.data = self.collect_data()
        return self.headers

    def save_data(self, file):
        with open(file, 'w') as f:
            w = csv.writer(f)
            w.writerow(self.headers)
            for row in self.data:
                w.writerow(row)

    @staticmethod
    def query_url(url, queries):
        return "{}?{}".format(url, ";".join("{}={}".format(k, v) for k, v in queries.items()))


class ESPNScrum(IDataScrapper):

    def __init__(self):
        super().__init__()
        self.URL = "http://stats.espnscrum.com/statsguru/rugby/stats/index.html"

    def collect_headers(self):
        r = requests.get(self.query_url(self.URL, self._page_number_query()))
        tree = html.fromstring(r.content)
        headers_str = "//div[@id='scrumArticlesBoxContent']/table[@class='engineTable']/*/tr[@class='headlinks']"
        *front, last = tree.xpath("{}/th/a/text()".format(headers_str))
        middle = tree.xpath("{}/th/text()".format(headers_str))
        return tuple((*front, *middle, last))

    def collect_data(self):
        self.data = self._pages_rows()

    @staticmethod
    def _page_number_query(page=1):
        return {
            "class": 1,
            "page": page,
            "template": "results",
            "type": "team",
            "view": "match"
        }

    def _page_rows(self, page):
        r = requests.get(self.query_url(self.URL, self._page_number_query(page)))
        tree = html.fromstring(r.content)
        table_rows_str = "//div[@id='scrumArticlesBoxContent']/table[@class='engineTable']/*/tr"
        rows = []
        for i in range(1, len(tree.xpath(table_rows_str))):
            first, lower_middle = tree.xpath("{}[{}]/td/a/text()".format(table_rows_str, i))
            *upper_middle, last = tree.xpath("{}[{}]/td/text()".format(table_rows_str, i))
            row = [str(r) for r in (first, *upper_middle, lower_middle, last)]
            rows.append(row)
        return rows

    def _pages_rows(self, first_page=1, last_page=None):
        if last_page is None:
            last_page = self._page_limit()
        rows = []
        for i in tqdm.tqdm(range(first_page, last_page)):
            rs = self._page_rows(i)
            if len(rs) == 0:
                break
            rows.extend(rs)
        return rows

    def _page_limit(self):
        r = requests.get(self.query_url(self.URL, self._page_number_query()))
        tree = html.fromstring(r.content)
        max_page_number_str = "//div[@id='scrumArticlesBoxContent']" \
                              "/table/tr/td/table[@class='engineTable']" \
                              "/tr/td[@style = 'text-align: left;  padding-top: 3px;']/text()"
        return int(str(tree.xpath(max_page_number_str)[0])[-4:-1])


class PickAndGo(IDataScrapper):
    def __init__(self):
        super().__init__()
        self.URL = "http://www.lassen.co.nz/pickandgo.php"

    def collect_headers(self):
        r = requests.post(self.URL, data=self._post_params())
        tree = html.fromstring(r.content)
        table_rows_str = '//table[@style="border: 1px solid #000;"]/tr/th/text()'
        return tree.xpath(table_rows_str)

    def collect_data(self):
        r = requests.post(self.URL, data=self._post_params())
        tree = html.fromstring(r.content)
        table_rows_str = '//table[@style="border: 1px solid #000;"]/tr'
        rows = []

        for i in tqdm.tqdm(range(2, len(tree.xpath(table_rows_str)))):
            row = tree.xpath("{}[{}]/td/text()".format(table_rows_str, i))
            row = [str(r) for r in row]
            match_str = row[2]
            if len(match_str) == 6:
                opposition = str(tree.xpath("{}[{}]/td/font/text()".format(table_rows_str, i))[0])
                if match_str.find("v") == 1:
                    row[2] = opposition + match_str
                else:
                    row[2] = match_str + opposition
            rows.append(row)
        return rows

    @staticmethod
    def _post_params():
        return {
            "txtfyear": 1870,
            "txttyear": datetime.datetime.now().year + 1,
            "Submit": "and Go!"
        }


# es = ESPNScrum()
# es.collect_data()
# es.save_data("espn_scrum_data.csv")
#
# pg = PickAndGo()
# pg.collect_data()
# pg.save_data("pick_and_go_data.csv")
