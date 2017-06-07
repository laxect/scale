import re
import json
import requests
# my module


class bilibili_spider():
    'a spider espeacially design for bilibili bangumi'
    def __init__(self, aim):
        'aim in stand of which bangumi you want to watch'
        self.aim = aim

    def url(self):
        url = f'http://bangumi.bilibili.com/jsonp/seasoninfo/{self.aim}\
.ver?callback=seasonListCallback'
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
        return (fres, res[1], 'bilibili_spider.'+str(self.aim))

    def run(self, que):
        res = self.handle(requests.get(self.url()).text)
        que.put(res[0])


def mod_init(aim):
    return bilibili_spider(aim=aim)


if __name__ == '__main__':
    class test_queue:
        def put(self, obj):
            print(obj)

    print(mod_init().run(test_queue()))
