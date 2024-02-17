import asyncio

from deepdiff import DeepDiff

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from colorama import Fore, Style


class Parser:
    def __init__(self, url, interval):
        self._interval = interval
        self._url = url
        self._soup = None
        self._curr_soup = None
        self._prev_soup = None
        self._curr_list = None
        self._prev_list = None
        # the init
        self._curr_soup = self.initialize_soup()
        self._curr_list = self.coinmarket_cap_stripper(self._curr_soup)
        self.get_update(self._interval)

    def initialize_soup(self):
        try:
            # Send a GET request to the URL
            response = requests.get(self._url)

            # Check if the request was successful (status code 200)
            response.raise_for_status()

            # Parse the HTML using BeautifulSoup
            return BeautifulSoup(response.text, 'html.parser')
        except RequestException as e:
            # If an error occurs during the request, print the error message
            raise RuntimeError(f"{Fore.RED}Failed to fetch the page: {e}{Style.RESET_ALL}")

    def coinmarket_cap_stripper(self, soup_instance: BeautifulSoup):
        # all the news items have parent div with class of uikit-row
        if soup_instance is None:
            raise TypeError(f"{Fore.RED}Error: soup instance is None{Style.RESET_ALL}")

        self._curr_soup = self.initialize_soup()
        soup_instance = self._curr_soup
        all_news = []
        all_sections = soup_instance.find_all('div', class_="uikit-row")
        if isinstance(all_sections, list):
            all_sections.pop(0)
        else:
            raise TypeError("the type of all_sections is not a list")

        for index, section in enumerate(all_sections):
            try:
                time = section.find('p', class_="bAeTER").text
                image = section.find("img", class_="fYMOUg").get('src')
                anchor = section.find("a", class_="imWlwI")
                title_url = anchor.get('href')
                title_text = anchor.text
                overview = section.find('p', class_="hLvDsV").text

                # extra part has 2 divs
                # first one includes source of the news
                # second one indicates affected crypto assets
                extra = section.find('div', class_="kfmhgr")
                extra_children = list(extra.find_all('div'))
                # first extra includes source of the news
                source = extra_children[0].find('span').text
                # second part includes an img tag and a span with the name of asset
                second_extra = extra_children[1].find_all('div', 'ikUdED')

                assets = []
                for asset in second_extra:
                    asset_img = asset.find('img').get('src')
                    asset_text = asset.find('span').text
                    assets.append({'img': asset_img, 'text': asset_text})

                all_news.append(
                    {'time': time,
                     'image': image,
                     'title_url': title_url,
                     'title_text': title_text,
                     'overview': overview,
                     'source': source,
                     'assets': assets})

            except (AttributeError, KeyError) as e:
                # Handle the exception (e.g., print a message, log, or ignore)
                print(f"{Fore.RED}error processing news sections {index}: {e}{Style.RESET_ALL}")
        return all_news

    @staticmethod
    def find_diff(current_news: list, previous_news: list) -> dict:
        isupdate = False
        final = None
        if not isinstance(current_news, list) or not isinstance(previous_news, list):
            raise TypeError(f"{Fore.RED}either current or previous arguments is not list{Style.RESET_ALL}")

        if current_news == previous_news:
            final = current_news
        else:
            final = DeepDiff(current_news, previous_news)
            isupdate = True
            # here make sure to construct the list desired

        # format both side of conditional to be the same for return
        return {'isupdate': isupdate, 'diff': final}

    @staticmethod
    async def timer(duration, func, *args, **kwargs):
        await asyncio.sleep(duration)
        await func(*args, **kwargs)

    async def get_update(self):
        if self._interval <= 0:
            return None

        self._prev_soup = self._curr_soup
        self._curr_soup = self.initialize_soup()
        self._prev_list = self._curr_list
        self._curr_list = self.coinmarket_cap_stripper(self._curr_soup)
        await self.timer(self._interval, self.find_diff, self._curr_list, self._prev_list)
