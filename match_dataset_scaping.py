import requests
from lxml import html


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

    def save_data(self):
        raise NotImplementedError()

    @staticmethod
    def query_url(url, queries):
        return "{}?{}".format(url, ";".join("{}={}".format(k, v) for k, v in queries.items()))


class ESPNScrum(IDataScrapper):

    def __init__(self):
        super().__init__()
        self.ESPN_SCRUM_URL = "http://stats.espnscrum.com/statsguru/rugby/stats/index.html"

    def collect_headers(self):
        r = requests.get(self.query_url(self.ESPN_SCRUM_URL, self._page_number_query()))
        tree = html.fromstring(r.content)
        headers_str = "//div[@id='scrumArticlesBoxContent']/table[@class='engineTable']/*/tr[@class='headlinks']"
        *front, last = tree.xpath("{}/th/a/text()".format(headers_str))
        middle = tree.xpath("{}/th/text()".format(headers_str))
        return tuple((*front, *middle, last))

    def collect_data(self):
        self.data = self._pages_rows()

    def save_data(self):
        # TODO implement saving method
        pass

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
        r = requests.get(self.query_url(self.ESPN_SCRUM_URL, self._page_number_query(page)))
        tree = html.fromstring(r.content)
        table_rows_str = "//div[@id='scrumArticlesBoxContent']/table[@class='engineTable']/*/tr"
        rows = []
        for i in range(1, len(tree.xpath(table_rows_str))):
            first, lower_middle = tree.xpath("{}[{}]/td/a/text()".format(table_rows_str, i))
            *upper_middle, last = tree.xpath("{}[{}]/td/text()".format(table_rows_str, i))
            rows.append(list((first, *upper_middle, lower_middle, last)))
        return rows

    def _pages_rows(self, first_page=1, last_page=None):
        if last_page is None:
            last_page = self._page_limit()
        rows = []
        for i in range(first_page, last_page):
            rs = self._page_rows(i)
            if len(rs) == 0:
                break
            rows.extend(rs)
        return rows

    @staticmethod
    def _page_limit():
        # TODO implement page limit search
        return 382
