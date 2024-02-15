import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from colorama import Fore, Style


class Parser:
    def __init__(self, url):
        try:
            # Send a GET request to the URL
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            response.raise_for_status()

            # Parse the HTML using BeautifulSoup
            self._soup = BeautifulSoup(response.text, 'html.parser')
        except RequestException as e:
            # If an error occurs during the request, print the error message
            raise RuntimeError(f"{Fore.RED}Failed to fetch the page: {e}{Style.RESET_ALL}")

    def extract_elements(self, element_name, use_class=True, use_id=False):
        elements = None
        if use_class:
            elements = self._soup.find('div', class_=element_name)
        if use_id:
            elements = self._soup.find('div', id=element_name)
        return elements

    def coinmarket_cap_stripper(self):
        # all the news items have parent div with class of uikit-row
        all_news = []
        all_sections = self._soup.find_all('div', class_="uikit-row")
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
