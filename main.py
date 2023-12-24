# Crypto News Crawler
# this app is designed to crawl websites and extract
# crypto related information and rate them

from parser import extract_elements, fetch_and_parse
from menu import menu


def main():
    menu()
    url = 'https://example.com'

    # Fetch and parse the website
    soup = fetch_and_parse(url)

    # If parsing was successful, extract certain DOM elements
    if soup:
        extract_elements(soup)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
