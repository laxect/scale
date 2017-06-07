import re
import json
# my module
try:
    from spider import spider
except ImportError:
    from modules.spider import spider


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
        title = dica['result']['bangumi_title']
        eps = dica['result']['episodes']
        res = (
            title,
            eps[0]['index'],
            eps[0]['index_title'],
            eps[0]['webplay_url'])
        fres = "%s 更新了第%s集 %s\n%s" % res  # format string
        if self.tmpfile != res:
            self.tmpfile = res
            return fres


def mod_init(aim=5998):
    return bilibili_spider(aim=aim)


if __name__ == '__main__':
    class test_queue:
        def put(self, obj):
            print(obj)

    mod_init().run(test_queue())
