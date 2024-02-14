import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style


def fetch_and_parse(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        # If the request was not successful, print an error message
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return None


def extract_elements(soup, element_name, use_class=True, use_id=False):
    elements = None
    if use_class:
        elements = soup.find('div', class_=element_name)
    if use_id:
        elements = soup.find('div', id=element_name)
    return elements


#
# def _extract_extra(elements):
#     if isinstance(elements, list):
#         for element in elements:
#             print(element)
#
#     else:
#         return None


def coinmarket_cap_stripper(parent):
    # all the news items have parent div with class of uikit-row
    all_news = []
    all_sections = parent.find_all('div', class_="uikit-row")
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

#
#
# soup = fetch_and_parse(url)
#
#     # If parsing was successful, extract certain DOM elements
#     if soup:
#         elements = extract_elements(soup, element_name="infinite-scroll-component", use_class=True)
#         all_parts = coinmarket_cap_stripper(parent=elements)
