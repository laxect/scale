from gevent import monkey
from gevent.queue import Empty
from modules import bangumi_bilibili
from modules import bilibili_spider
monkey.patch_all(aggressive=True)
div_line = '=================='
div_line2 = '------------------'


class test_mail_service():
    def __init__(self, contents=None):
        self.count = 0
        if contents:
            self.contents = contents
            self.count = len(self.contents)

    def get(self, block=True, timeout=False):
        self.count -= 1
        if self.count < 0:
            raise Empty
        msg_pack = {
            'msg': self.contents[self.count]
        }
        return msg_pack

    def put(self, item):
        print(div_line + div_line)
        for key in item:
            print(div_line2 + div_line2)
            print('    ' + str(key) + ' :')
            print(item[key])
            print(div_line2 + div_line2)
        print(div_line + div_line)


def bangumi_bilibili_test():
    print(f'\ntask: bangumi_bilibili\n{div_line}')
    targets = ['laxect_cn']
    test_task = bangumi_bilibili.mod_init()
    test_task.run(test_mail_service(), targets, debug=True)


def bilibili_spider_test():
    print(f'\ntask: bilibili_spider\n{div_line}')
    targets = ['6330']
    test_task = bilibili_spider.mod_init(targets)
    test_task.run(test_mail_service(), targets, debug=True)
    test_task.run(
        test_mail_service(), targets,
        inbox=test_mail_service(['1057']), debug=True
    )


def test_task():
    bangumi_bilibili_test()
    bilibili_spider_test()


if __name__ == '__main__':
    test_task()
