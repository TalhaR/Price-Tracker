import requests
import lxml
from bs4 import BeautifulSoup

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari',
            'Accept-Language': 'en-US, en;q=0.5'})


def request():
    url = 'https://www.amazon.com/Razer-Ultimate-Hyperspeed-Lightest-Wireless/dp/B07YPC3BQC/'
    url = 'https://talhar.github.io/'
    res = requests.get(url, headers=HEADERS)
    return BeautifulSoup(res.text, 'lxml')


def save_request(soup):
    with open('test.html', 'w') as file:
        file.write(soup.prettify())


def check_price(soup):
    price_elem = soup.find(id='priceblock_ourprice')
    title_elem = soup.find(id='dfsafdasf')

    if not price_elem or not title_elem:
        return False
   
    numeric_price = str_price = price_elem.get_text().strip()

    for c in ('$', ',', ' '):
        numeric_price = numeric_price.replace(c, '')

    numeric_price = float(numeric_price)

    with open('price.txt', 'w') as file:
        file.write(title_elem.get_text().strip() + '\n')
        file.write(str_price + '\n')
        file.write(str(numeric_price))

    return False


def main():
    # soup = request()
    with open('test.html', 'r') as file:
        contents = file.read()
        soup = BeautifulSoup(contents, 'lxml')
    if check_price(soup):
        pass
    else:
        print("error")


if __name__ == '__main__':
    main()
