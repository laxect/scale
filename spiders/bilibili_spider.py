import re
import json
# my module
try:
    from spider import spider
except ModuleNotFoundError:
    from spiders.spider import spider


class bilibili_spider(spider):
    'a spider espeacially design for bilibili bangumi'
    def __init__(self, aim=5998):
        'aim in stand of which bangumi you want to watch'
        self.aim = aim
        self.tmpfile = ''

    def url(self):
        'return the url that spider need.'
        return self._url(self.aim)

    def _url(self, Bangumino):
        url = 'http://bangumi.bilibili.com/jsonp/seasoninfo/%s\
.ver?callback=seasonListCallback' % str(Bangumino)
        return url

    def handle(self, text):
        'the fun to handle the text spider return'
        dica = json.loads(re.findall('\w*\((.*)\);', text)[0])
        eps = dica['result']['episodes']
        res = (
            eps[0]['index'],
            eps[0]['index_title'],
            eps[0]['webplay_url'])
        if self.tmpfile != res:
            self.tmpfile = res
            return res


def mod_init(aim=5998):
    return bilibili_spider(aim=aim)


if __name__ == '__main__':
    class test_queue:
        def put(self, obj):
            print(obj)

    mod_init().run(test_queue())
