import requests


class spider:
    'a spider'
    def __init__(self):
        pass

    def url(self):
        return []

    def handle(self, text):
        return []

    def run(self):
        text = [requests.get(url).text for url in self.url()]
        return self.handle(text)


def main():
    bs = spider()
    print(bs.run())


if __name__ == '__main__':
    main()
