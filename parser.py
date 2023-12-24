import requests
from bs4 import BeautifulSoup


def fetch_and_parse(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        # If the request was not successful, print an error message
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return None


def extract_elements(soup):
    # Example: Extracting all <a> (anchor) tags from the page
    links = soup.find_all('a')

    # You can perform additional processing based on your specific needs
    for link in links:
        print(link['href'])
