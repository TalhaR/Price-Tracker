import request
from bs4 import BeautifulSoup


def main():
    url = "https://talhar.github.io/"
    page = request.GET(url)

    soup = BeautifulSoup(page.content, 'html.paser')


if __name__ == '__main__':
    main()
