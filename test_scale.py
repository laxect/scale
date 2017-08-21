from modules import bangumi_bilibili


class test_mail_service():
    def put(self, item):
        from pprint import pprint
        pprint(item)


def bangumi_bilibili_test():
    targets = ['laxect_cn']
    test_task = bangumi_bilibili.bangumi_spider()
    test_task.run(test_mail_service(), targets)


def test_task():
    bangumi_bilibili_test()


if __name__ == '__main__':
    test_task()
