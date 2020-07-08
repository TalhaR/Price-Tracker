import requests
import lxml
from bs4 import BeautifulSoup
from time import sleep
import csv, smtplib, ssl, config, os, random

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari',
            'Accept-Language': 'en-US, en;q=0.5'})


def request(url: str) -> BeautifulSoup:
    if ('amazon.com' not in url):
        raise Exception('Error: Only use Amazon URLs in wishlist.csv')
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return BeautifulSoup(res.text, 'lxml')


def sendEmail(title: str, url: str, price: float) -> None:
    cont = ssl.create_default_context()

    message = f"""Subject: Amazon Item Pricedrop\nPrice Tracker
        \rA product on your Amazon wishlist is within your target price
        \rProduct: {title}
        \rPrice: ${price}
        \rURL: {url}
    """

    with smtplib.SMTP_SSL('smtp.gmail.com', port=465, context=cont) as server:
        try:
            server.login(config.bot_email, config.bot_password)
            server.sendmail(config.bot_email, config.recipient, message)
        except Exception as e:
            print(e)
            print('Please update your config.py file to the correct information')
            exit(4)
        


def check_price(soup: BeautifulSoup, target_price: float) -> float:
    price_elem = soup.find(id='priceblock_ourprice')

    if not price_elem:
        print('Item Out of Stock')
        return -1
    elif target_price < 0:
        print('A Target_Price in wishlist.csv is negative. Consider updating to a positive integer')

    price = price_elem.get_text().strip()

    for c in ('$', ','):
        price = price.replace(c, '')

    price = float(price)

    if (price < target_price):
        print('An item met the criteria')
        return price
    else:
        print('An item does not meet the criteria')
    return -1


def create_wishlist() -> None:
    with open('wishlist.csv', 'w') as file:
        file.write("URL, TARGET_PRICE\n")


def process_wishlist() -> None:
    try:
        with open('wishlist.csv') as csv_file:
            reader = csv.reader(csv_file)

            # If file smaller than 19 Bytes then it was not updated
            if (os.path.getsize('wishlist.csv') < 19):
                raise Exception('Wishlist.csv is empty. Please add items to it before running again')

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
        exit(1)
    except ValueError:
        print('Error: Target_value in Wishlist.csv file not formatted correctly')
        exit(2)
    except Exception as e:
        print(e)
        exit(3)


def main():
    while (True):
        if not os.path.exists('wishlist.csv'):
            create_wishlist()
            print('Please update wishlist.csv before running this script again')
            break
        else:
            process_wishlist()
            # Delay checking to once every 25-45 mins 
            # Not recommended to lower below 900 to avoid Amazon blocking requests
            sleep(random.randint(1500, 2700))


if __name__ == '__main__':
    main()
