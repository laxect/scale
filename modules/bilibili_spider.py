import re
import json
import requests
# my module


class tmpfile():
    'the class that save data'
    # will be mov to div file in the next releases.
    def __init__(self, id):
        import sys
        self.path = sys.path[0]+f'/{id}.tmp'
        print(self.path)

    def __enter__(self):
        # special design for with
        try:
            with open(self.path, 'r') as tmp_file:
                self.dict = json.loads(tmp_file.read())
        except FileNotFoundError:
            self.dict = {}
        return self

    def check_up_to_date(self, key, text):
        if self.dict.get(key) == text:
            return False
        else:
            self.dict[key] = text
            return True

    def __exit__(self, exc_ty, exc_val, tb):
        with open(self.path, 'w+') as tmp_file:
            tmp_file.write(json.dumps(self.dict))
        del self.dict


class bilibili_spider():
    'a spider espeacially design for bilibili bangumi'
    def __init__(self, aim):
        'aim in stand of which bangumi you want to watch'
        self._aim = aim
        self.id = f'laxect.bilibili_spider.{aim}'

    def _url(self):
        url = f'http://bangumi.bilibili.com/jsonp/seasoninfo/{self._aim}\
.ver?callback=seasonListCallback'
        return url

    def _handle(self, text):
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
        with tmpfile(self.id) as hash_map:
            if hash_map.check_up_to_date(self.id, str(res[1])):
                return (fres, self.id)
        return None

    def run(self, que):
        res = self._handle(requests.get(self._url()).text)
        if res:
            que.put(res[0])


def mod_init(aim):
    return bilibili_spider(aim=aim)


if __name__ == '__main__':
    class test_queue:
        def put(self, obj):
            print(obj)

    print(mod_init().run(test_queue()))
