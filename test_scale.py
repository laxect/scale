#!/usr/bin/python3.6
import gevent
from gevent import monkey
from gevent.queue import Empty
# my modules need to test.
import standard_task
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
    'timer': (0, ()),
}  # test date


class test_mail_service():
    def __init__(self, contents=None, output=True):
        self.count = 0
        self.output = output
        if contents:
            self.contents = contents
            self.count = len(self.contents)

    def get(self, block=True, timeout=False):
        if block:
            gevent.sleep(0)
        self.count -= 1
        if self.count < 0:
            raise Empty
        return {
            'msg': self.contents[self.count]
        }

    def put(self, item):
        if not self.output:
            return
        print(div_line + div_line)
        for key in item:
            print(div_line2 + div_line2)
            print('    ' + str(key) + ' :')
            print(item[key])
            print(div_line2 + div_line2)
        print(div_line + div_line)


class scale_core_test_apis():
    def __init__(self):
        pass


def standard_task_test():
    class test_task(standard_task.task):
        def __init__(self, mail_service):
            super.__init__(mail_service)
            self.id = 'laxect.test_task'
            self.page_get_switch = True

        def mail_handle(self, msg):
            print(msg)

        def _run(self):
            self.scale_core_apis('test', ['helloworld'])
            print('test task is runing')


def test_task():
    standard_task_test()


if __name__ == '__main__':
    test_task()
    # scales_test()
