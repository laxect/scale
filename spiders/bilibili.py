import re
import json


def url():
    aim = [5998]
    return [_url(i) for i in aim]


def _url(Bangumino):
    url = 'http://bangumi.bilibili.com/jsonp/seasoninfo/'
    url += str(Bangumino)
    url += '.ver?callback=seasonListCallback'
    return url


def handle(text):
    for item in text:
        dica = json.loads(re.findall('\w*\((.*)\);', item)[0])
        eps = dica['result']['episodes']
        res = eps['0']['index'] + eps['0']['index_title']
        print(res)
        return dica['result']['newest_ep_index']
