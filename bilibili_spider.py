import re
import json
# my module
from spider import spider


class bilibili_spider(spider):
    'a spider espeacially design for bilibili bangumi'
    def __init__(self):
        self.aim = [5998]

    def url(self):
        'return the url that spider need.'
        return [self._url(i) for i in self.aim]

    def _url(self, Bangumino):
        url = 'http://bangumi.bilibili.com/jsonp/seasoninfo/'
        url += str(Bangumino)
        url += '.ver?callback=seasonListCallback'
        return url

    def handle(self, text):
        'the fun to handle the text spider return'
        for item in text:
            dica = json.loads(re.findall('\w*\((.*)\);', item)[0])
            eps = dica['result']['episodes']
            res = (
                eps[0]['index'],
                eps[0]['index_title'],
                eps[0]['webplay_url'])
            return res


def main():
    bs = bilibili_spider()
    print(bs.run())


if __name__ == '__main__':
    main()
