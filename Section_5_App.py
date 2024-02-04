import requests
from bs4 import BeautifulSoup

URL = "https://catalog.data.gov/dataset"


def list_datasets(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = ""

    for dataset in soup.find_all('h3', class_='dataset-heading'):
        a_tag = dataset.find('a')
        title = a_tag.text.strip()
        link = a_tag['href']
        result = result + f"\nTitle: {title}\nLink: {link}\n"
    return result

print(list_datasets(URL))