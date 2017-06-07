import requests


class spider:
    'a spider'
    def __init__(self):
        pass

    def url(self):
        pass

    def handle(self, text):
        pass

    def run(self):
        text = []
        for url in self.url():
            text.append(requests.get(url).text)
        res = self.handle(text)
        return res


def main():
    bs = spider()
    print(bs.run())


if __name__ == '__main__':
    from gevent import monkey
    monkey.patch_socket()
    main()
