# Retrieve stock quote by scraping Yahoo user interface page.
# Amazingly, this fragile method has held up since 2016 (as of 2020-03-20).
# Update: broke in July 2020 due to minor formatting change.

from bs4 import BeautifulSoup

import requests
import re

INDEXES_SUPPORTED = True

QUOTE_ERR = (0.0, 0.0, 0.0)

TEST = False
TEST_VAL = (19173.98, -913.21, -4.7)

def quote(symbol):
    """
    Return quote for ticker as triple of floats (last, change, pct),
    QUOTE_ERR on failure.
    """
    if TEST:
        return TEST_VAL

    try:
        response = requests.get('https://finance.yahoo.com/quote/%s?p=%s' % (symbol, symbol))
        if not response:
            return QUOTE_ERR
        if response.status_code != 200:
            print('Request bad status code %d' % response.status_code)
            return QUOTE_ERR
        page = response.text
    except Exception as e:
        print('Request exception: %s' % e)
        return QUOTE_ERR

    soup = BeautifulSoup(page, 'html.parser')

    try:
        header_info = soup.select('div[id="quote-header-info"]')[0]
        divs = header_info.findAll('div', recursive=False)
        block = divs[2]
        divs = block.findAll('div', recursive=False)
        block = divs[0]
        divs = block.findAll('div', recursive=False)
        block = divs[0]
        spans = block.findAll('span', recursive=False)
        quote = re.sub(r',', r'', spans[0].text)
        price_usd = float(quote.replace(',', ''))
        change_str = spans[1].text.replace(',', '').replace('+', '')
        m = re.match(r'([-.0-9]+) \(([-.0-9]+)%\)', change_str)
        change_usd, change_pct = float(m.group(1)), float(m.group(2))
    except Exception as e:
        print('Parse exception: %s' % e)
        return QUOTE_ERR

    return price_usd, change_usd, change_pct
