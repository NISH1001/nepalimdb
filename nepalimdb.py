#!/usr/bin/env python3

import re
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

class NepaliImdbCrawler:
    def __init__(self, start_page=None, end_page=None):
        self.start_page = start_page
        self.end_page = end_page
        self.imdb_url = "https://www.imdb.com"
        self.base_url = "https://www.imdb.com/search/title?country_of_origin=NP"
        self.total_count = 0

    def crawl(self):
        """
            Directly get whole data in single call
        """
        data = []
        for d in self.crawl_lazily():
            data.append(d)
        return data

    def crawl_lazily_old(self):
        """
            The old function where page number was used to crawl
        """
        page = self.start_page if self.start_page else 1
        while True:
            # url = "{}&page={}".format(self.base_url, page)
            page_data = self.scrape_page(page)
            yield page_data
            if not page_data:
                break
            page += 1
            if self.end_page and (page > self.end_page):
                break

    def crawl_lazily(self):
        """
            The current implementation that makes use of reference count of item.
            And the next url
        """
        page = self.start_page if self.start_page else 1
        nexturl = self.base_url
        while nexturl:
            # url = "{}&page={}".format(self.base_url, page)
            page_data, nexturl = self.scrape_page(nexturl)
            self.total_count += len(page_data)
            print("Total data fetched so far :: {}".format(self.total_count))
            yield page_data

    def scrape_page_old(self, page_number):
        data = []
        url = "{}&page={}".format(self.base_url, page_number)
        print("Fetching {}".format(url))
        response = requests.get(url)
        if response.status_code !=200:
            return []
        soup = BeautifulSoup(response.content, 'html.parser')
        #divs = soup.find_all('div', {'class' : 'lister-item mode-advanced'})
        content_divs = soup.find_all('div', {'class' : 'lister-item-content'})
        for div in content_divs:
            info_map = self._get_single_movie(div)
            data.append(info_map)
        return data

    def scrape_page(self, url):
        data = []
        # url = "{}&page={}".format(self.base_url, page_number)
        print("Fetching {}".format(url))
        response = requests.get(url)
        if response.status_code !=200:
            return []
        soup = BeautifulSoup(response.content, 'html.parser')
        #divs = soup.find_all('div', {'class' : 'lister-item mode-advanced'})
        content_divs = soup.find_all('div', {'class' : 'lister-item-content'})
        for div in content_divs:
            info_map = self._get_single_movie(div)
            data.append(info_map)
        nextdiv = soup.find('a', {'class': 'lister-page-next next-page'})
        nexturl = '' if not nextdiv else urljoin(self.imdb_url, nextdiv['href'])
        return data, nexturl

    def _get_single_movie(self, div):
        types = ['runtime', 'genre']
        info_map = {}

        # scrape from header
        title_div = div.find('h3', {'class' : 'lister-item-header'})
        anchor = title_div.find('a')
        info_map['imdb_url'] = self.imdb_url + anchor['href']
        info_map['title'] = anchor.text

        year = title_div.find('span', {'class' : 'lister-item-year text-muted unbold'}).text.strip()
        if year:
            year = re.findall(r'\d+', year)
            year = None if not year else int(year[0])
        info_map['year'] = year

        muted_divs = div.find_all('p', {'class' : 'text-muted'})
        for t in types:
            d = muted_divs[0].find('span', {'class' : t})
            info_map[t] = d.text.strip() if d else None

        rating_div = div.find('div', {'class' : 'inline-block ratings-imdb-rating'})
        info_map['rating'] = None if not rating_div else float(rating_div.text.strip())
        info_map['plot'] = None if not muted_divs[1] else muted_divs[1].text.strip()

        vote_div = div.find('p', {'class' : 'sort-num_votes-visible'})
        info_map['votes'] = None if not vote_div else int(re.findall(r'\d+', vote_div.text.strip())[0])
        return info_map


def main():
    base_url = "https://www.imdb.com/search/title?country_of_origin=NP"
    nepcrawler = NepaliImdbCrawler(start_page=1, end_page=None)
    # data = nepcrawler.crawl()
    res = []
    for data in nepcrawler.crawl_lazily():
        res.extend(data)
        with open('data/nepali-movies.json', 'w') as f:
            print("Dumping {} movies".format(len(data)))
            json.dump(res, f, indent=4)


if __name__ == "__main__":
    main()

