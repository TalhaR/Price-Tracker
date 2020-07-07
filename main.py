import requests
import lxml
from bs4 import BeautifulSoup
import csv, smtplib, ssl
import config
import os

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari',
            'Accept-Language': 'en-US, en;q=0.5'})


def request(url: str):
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return BeautifulSoup(res.text, 'lxml')


def sendEmail(title: str, url: str, price: str):
    cont = ssl.create_default_context()

    message = f"""Subject: Amazon Item Pricedrop\nPrice Tracker
        \rA product on your Amazon wishlist is within your target price
        \rProduct: {title}
        \rPrice: ${price}
        \rURL: {url}
    """

    with smtplib.SMTP_SSL('smtp.gmail.com', port=465, context=cont) as server:
        server.login(config.bot_email, config.bot_password)
        server.sendmail(config.bot_email, config.recipient, message)


def check_price(soup, target_price: float) -> float:
    price_elem = soup.find(id='priceblock_ourprice')

    if not price_elem:
        if soup.find(id='productTitle') is None:
            print('Error: Either URL or Target_Price incorrect')
        else:
            print('Item Out of Stock')
        return -1

    price = price_elem.get_text().strip()

    for c in ('$', ','):
        price = price.replace(c, '')

    price = float(price)

    if (price < target_price):
        print('passes')
        return price
    else:
        print('does not pass')
    return -1


def create_wishlist():
    with open('wishlist.csv', 'w') as file:
        file.write("URL, TARGET_PRICE\n")


def process_wishlist():
    try:
        with open('wishlist.csv') as csv_file:
            reader = csv.reader(csv_file)

            if (os.path.getsize('wishlist.csv') < 19):
                print('Wishlist.csv is empty. Please add items')

            next(reader)
            for url, target_price in reader:
                soup = request(url)
                price = check_price(soup, float(target_price))
                if price != -1:
                    title = soup.find(id='productTitle').get_text().strip()
                    sendEmail(title, url, price)
    except FileNotFoundError:
        create_wishlist()
        print("""Error: Wishlist.csv file couldn't be accessed
        \rNew wishlist.csv file created.
        Please update it before running this script again""")
    except ValueError:
        print('Wishlist.csv file not filled or formatted correctly')
    except Exception as e:
        print(e)


def main():
    if not os.path.exists('wishlist.csv'):
        create_wishlist()
        print('Please update wishlist.csv before running this script again')
    else:
        process_wishlist()


if __name__ == '__main__':
    main()
