from bs4 import BeautifulSoup
import requests
import re

import sys


class GetURLS:
    def process(url):

        d = 0
        try:

            print("in process", url)
            # kwd= "python java"
            html = ""
            text = ""
            try:
                html = requests.get(url).content
                # 1 Recoding
                unicode_str = html.decode("utf8")
                encoded_str = unicode_str.encode("ascii", 'ignore')
                news_soup = BeautifulSoup(encoded_str, "html.parser")
                a_text = news_soup.find_all('p')
                # 2 Removing
                y = [re.sub(r'<.+?>', r'', str(a)) for a in a_text]
                html = y
            except:
                pass
            for h in html:
                text = text + " " + h

            print(text)
            return text
        except:
            return ''
if __name__ == '__main__':
    GetURLS.process("https://en.wikipedia.org/wiki/Cloud_computing")