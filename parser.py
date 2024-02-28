import asyncio

from deepdiff import DeepDiff

from chatgpt_translation import ChatGPTTranslator
from config import bot_token, channel_name, chrome_driver_path
from telegram_bot import NovncyBot
from requests.exceptions import RequestException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from colorama import Fore, Style


class Parser:
    def __init__(self, url, interval, latest=None):
        self.__counter = 0
        self._interval = interval
        self._url = url
        self._wait = 20
        self._latest = latest
        self._curr_soup = None
        self._prev_soup = None
        self._curr_list = None
        self._prev_list = None
        # initializing the chrome driver
        # Chrome options to run in headless mode
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')  # Necessary for running in a Docker container, for example
        chrome_options.add_argument(
            '--disable-dev-shm-usage')  # Necessary for running in a Docker container, for example
        self._chrome = webdriver.Chrome(options=chrome_options)
        self._chrome.get("https://www.google.com/")
        self._chrome.execute_cdp_cmd('Network.setCacheDisabled', {'cacheDisabled': True})
        # starting the bot and getting the first result
        self._bot = NovncyBot(token=bot_token)
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

    def __find_diff(self) -> dict:
        isupdated = False
        if not isinstance(self._curr_list, list) or not isinstance(self._prev_list, list):
            raise TypeError(f"{Fore.RED}either current or previous arguments is not list{Style.RESET_ALL}")

        if self._curr_list == self._prev_list:
            result = self._curr_list
        else:
            result = DeepDiff(self._curr_list, self._prev_list)
            isupdated = True
            # here make sure to construct the list desired

        # format both side of conditional to be the same for return
        returnee = {"isupdated": isupdated, "diff": result}
        return returnee

    async def __poster(self, index: int, raw_post: dict) -> None:
        formatted_post = (f"<b>{raw_post['title_text']}</b>"
                          f"\n⏰ {raw_post['time']}"
                          f"\n\n{raw_post['overview']}"
                          f"\n💰 source: {raw_post['source']}"
                          f"\n🔬 <a href='https://coinmarketcap.com/headlines/news/{raw_post['title_url']}'>read more...</a>"
                          f"\n ___________________"
                          f"\n🇮🇷 @novncy")

        translator = ChatGPTTranslator()
        translated_post = translator.translate(text=formatted_post)

        if raw_post["image"] is not None:
            await self._bot.send_image(channel_name=channel_name, image_url=raw_post['image'], message=translated_post)
        else:
            await self._bot.send_message(channel_name=channel_name, message=translated_post)

    async def __compose(self):
        result = self._curr_list
        if self._latest is not None:
            result = result[-self._latest:]
        # if time of the last post was the same don't post it
        # find the last post's time
        if result[-1]['time'] == self._prev_list[-1]['time']:
            return

        for key, value in enumerate(result):
            await self.__poster(index=key, raw_post=value)

    @staticmethod
    async def timer(duration, func, *args, **kwargs):
        await func(*args, **kwargs)
        await asyncio.sleep(duration)

    async def get_update(self):
        if self._interval <= 0:
            return None

        while True:
            self._prev_soup = self._curr_soup
            self._curr_soup = self.__initialize_soup()
            self._prev_list = self._curr_list
            self._curr_list = self.__coinmarketcap_stripper(self._curr_soup)
            await self.timer(self._interval, self.__compose)
