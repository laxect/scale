import re
import sys
import json
import requests


class bilibili_spider:
    'a spider espeacially design for bilibili bangumi'
    def __init__(self):
        'aim in stand of which bangumi you want to watch'
        self.aim = []
        with open(sys.path[0]+'/bilibili_spider_config', 'r') as config:
            # read aims from file
            for line in config:
                if line:
                    self.aim.append(int(line))

    def url(self, Bangumino):
        'return the url that spider need.'
        url = 'http://bangumi.bilibili.com/jsonp/seasoninfo/%s\
.ver?callback=seasonListCallback' % str(Bangumino)
        return url

    def _hash(self, content, aim):
        'check if the content is new'
        import sys
        try:
            tmp = open(sys.path[0]+'/bilibili_spider_store', 'r+')
        except FileNotFoundError as err:
            tmp = open(sys.path[0]+'/bilibili_spider_store', 'w+')
        # read from file. and if the file is not exist, touch it
        try:
            data = json.loads(tmp.read())
        except json.decoder.JSONDecodeError:
            data = {}
        # prevent if the file is new up and was empty
        tmp.close()
        if data.get(str(aim)) == content:
            res = False
        else:
            data[str(aim)] = content
            res = True
        with open(sys.path[0]+'/bilibili_spider_store', 'w+') as tmp:
            # write the date back
            tmp.write(json.dumps(data))
        return res

    def handle(self, text, aim):
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
        if self._hash(res[1], aim):
            return fres
        return None

    def run(self):
        text = []
        for aim in self.aim:
            res = self.handle(requests.get(self.url(aim)).text, aim)
            if res:
                text.append(res)
        return text


def mod_init():
    return bilibili_spider()


if __name__ == '__main__':
    from scales_bot import A_test_from_bot
    bs = mod_init()
    text = bs.run()
    if text:
        for item in text:
            print(item)
            A_test_from_bot(item)
