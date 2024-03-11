import asyncio
import os
import platform
from deepdiff import DeepDiff, DeepHash
from tqdm import tqdm

from chatgpt_translation import ChatGPTTranslator
from telegram_bot import NovncyBot
from requests.exceptions import RequestException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from colorama import Fore, Style


class Parser:
    def __init__(self, url, interval, latest=None):
        self._counter = 0
        self._interval = interval
        self._url = url
        self._wait = 20
        self._latest = latest
        self._curr_soup = None
        self._prev_soup = None
        self._curr_list = None
        self._prev_list = None
        self._translator = ChatGPTTranslator()
        # initializing the chrome driver
        # Chrome options to run in headless mode
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')  # Necessary for running in a Docker container, for example
        chrome_options.add_argument(
            '--disable-dev-shm-usage')  # Necessary for running in a Docker container, for example
        if platform.system() == 'Windows':
            service = Service(os.getenv("CHROME_DRIVER_WINDOWS"))
        else:
            service = Service(os.getenv("CHROME_DRIVER_LINUX_MAC"))
        self._chrome = webdriver.Chrome(service=service, options=chrome_options)
        # self._chrome.get("https://www.google.com/")
        self._chrome.execute_cdp_cmd('Network.setCacheDisabled', {'cacheDisabled': True})
        # starting the bot and getting the first result
        self._bot = NovncyBot()
        self._curr_soup = self.__initialize_soup()
        self._curr_list = self.__coinmarketcap_stripper(self._curr_soup)

    def __initialize_soup(self):
        try:

            self._chrome.get(self._url)
            # Wait for JavaScript to render the page content
            # You might need to adjust the waiting time according to the page's loading speed
            self._chrome.implicitly_wait(self._wait)

            # Get page source after JavaScript rendering
            page_source = self._chrome.page_source

            # Parse the HTML using BeautifulSoup
            return BeautifulSoup(page_source, 'html.parser')
        except RequestException as e:
            # If an error occurs during the request, print the error message
            raise RuntimeError(f"{Fore.RED}Failed to fetch the page: {e}{Style.RESET_ALL}")

    @staticmethod
    def __coinmarketcap_stripper(soup_instance: BeautifulSoup):
        # all the news items have parent div with class of uikit-row
        if soup_instance is None:
            raise TypeError(f"{Fore.RED}Error: soup instance is None{Style.RESET_ALL}")

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
        all_news.reverse()
        return all_news

    def __find_diff(self) -> list:
        current_list = self._curr_list[-self._latest:]
        previous_list = self._prev_list[-self._latest:]

        diff = DeepDiff(current_list, previous_list, ignore_order=True)
        new_posts = []

        if 'iterable_item_added' in diff:
            for added_item in diff['iterable_item_added']:
                new_posts.append(added_item)

            if not new_posts:
                print(f"{Fore.YELLOW}no new posts{Style.RESET_ALL}")
        return new_posts

    async def __poster(self, index: int, raw_post: dict, rtl=True) -> None:
        # determine rtl here to avoid duplications
        # also
        # you can add the unicode to each part here also
        # if rtl:
        print(f"{Fore.YELLOW}translating post :{index}{Style.RESET_ALL}")
        response_dict = self._translator.translate(caption=raw_post['title_text'], body=raw_post['overview'])

        if 'main_body' and 'caption' in response_dict:
            title, body = response_dict
        else:
            print(f"{Fore.YELLOW}response_dict: {response_dict}{Style.RESET_ALL}")
            return

        if rtl:
            formatted_post = (f"<b>{'\u200F' + response_dict[title]}</b>"
                              f"\n⏰ {raw_post['time']}"
                              f"\n\n{'\u200F' + response_dict[body]}"
                              f"\n💰 منبع: {raw_post['source']}"
                              f"\n🔬 <a href='https://coinmarketcap.com/headlines/news/{raw_post['title_url']}'>مطالعه بیشتر...</a>"
                              f"\n"
                              f"\n🇮🇷 @NOVNCY")
        else:
            formatted_post = (f"<b>{response_dict[title]}</b>"
                              f"\n⏰ {raw_post['time']}"
                              f"\n\n{response_dict[body]}"
                              f"\n💰 source: {raw_post['source']}"
                              f"\n🔬 <a href='https://coinmarketcap.com/headlines/news/{raw_post['title_url']}'>read more...</a>"
                              f"\n ___________________"
                              f"\n🇮🇷 @NOVNCY")

        if raw_post["image"] is not None:
            await self._bot.send_image(channel_name=os.getenv("CHANNEL_NAME"), image_url=raw_post['image'],
                                       message=formatted_post)
        else:
            await self._bot.send_message(channel_name=os.getenv("CHANNEL_NAME"), message=formatted_post)
        print(f"{Fore.GREEN}* * * * * * * * * *{Style.RESET_ALL}")

    async def __compose(self):
        new_posts = []
        # if current list not empty, continue
        if not self._curr_list:
            print(f"{Fore.RED}empty list, debugging info: {self._curr_list}{Style.RESET_ALL}")
            return

        print(f"{Fore.YELLOW}{self._counter} iteration{Style.RESET_ALL}")
        if self._counter != 0:
            new_posts = self.__find_diff()
            # if self._curr_list[-1]['time'] == self._prev_list[-1]['time']:
            #     return
        else:
            new_posts = self._curr_list[-self._latest:]
        self._counter += 1

        # post the result
        if new_posts:
            for key, value in enumerate(new_posts):
                await self.__poster(index=key, raw_post=value)

    @staticmethod
    async def timer(duration, func, *args, **kwargs):
        await func(*args, **kwargs)
        # timer here
        while duration > 0:
            for i in tqdm(range(duration), desc="countdown", unit="second"):
                await asyncio.sleep(1)
                duration -= 1

    async def get_update(self):
        if self._interval <= 0:
            return None

        while True:
            print(f"{Fore.CYAN}- - - - - - - - - -{Style.RESET_ALL}")
            print(f"{Fore.CYAN}-fetching new list{Style.RESET_ALL}")
            self._prev_soup = self._curr_soup
            self._curr_soup = self.__initialize_soup()
            self._prev_list = self._curr_list
            self._curr_list = self.__coinmarketcap_stripper(self._curr_soup)
            print(f"{Fore.GREEN}+fetching done{Style.RESET_ALL}")
            await self.timer(self._interval, self.__compose)
            print(f"{Fore.CYAN}- - - - - - - - - -{Style.RESET_ALL}")
