#!/usr/bin/python3.6
from gevent import monkey
from gevent.queue import Empty
# my modules need to test.
import scale_core
from modules import timer
from modules import bilibili_spider
from modules import bangumi_bilibili
monkey.patch_all(aggressive=True)
div_line = '=================='
div_line2 = '------------------'
test_date = {
    'bangumi_bilibili': (1500, ('laxect_cn',)),
    'bilibili_spider': (1200, ('1071',)),
    'lightnovel_spider': (1500, (
        '和ヶ原聡司', '久遠侑', '七沢またり', '白鸟士郎',
        '羊太郎', '入间人间', '十文字青', '葵せきな',
    )),
    'scales_bot': (0, (
        '268094147:AAHNDBMmFQQaUqVm6mfaCe0a9uFmXWIiVBk', 290809873
    )),
    'timer': (0, ())
}  # test date


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
        inbox=test_mail_service([['1057', '2809']]), debug=True
    )


def timer_test(cycle_time=10):
    print(f'\ntask: timer\n{div_line}')
    test_task = timer.mod_init()
    for i in range(cycle_time):
        test_task.run(test_mail_service(), debug=True)


def scales_test():
    core_task = scale_core.scale_console(debug=True, config=test_date)
    try:
        core_task.run()
    except KeyboardInterrupt:
        print('Good Bye.')


def test_task():
    # timer_test(1)
    # bilibili_spider_test()
    bangumi_bilibili_test()


if __name__ == '__main__':
    # test_task()
    scales_test()
