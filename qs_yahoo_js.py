import requests
import re
import json

INDEXES_SUPPORTED = True

QUOTE_ERR = (0.0, 0.0, 0.0)

def quote(symbol):
    """
    Return quote for ticker as pair of floats (last, change), QUOTE_ERR on failure.
    """
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

    try:
        for line in page.splitlines():
            m = re.match(r'^root.App.main = (.*);$', line)
            if m:
                j = json.loads(m.group(1))
                qdata = j['context']['dispatcher']['stores']['StreamDataStore']['quoteData'][symbol]
                print(qdata)
                price_usd = qdata['regularMarketPrice']['raw']
                change_usd = qdata['regularMarketChange']['raw']
                prevclose_usd = qdata['regularMarketPreviousClose']['raw']
                change_pct = change_usd * 100 / prevclose_usd
                return price_usd, change_usd, change_pct
    except:
        return QUOTE_ERR
