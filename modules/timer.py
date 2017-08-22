from . import stand_task
import datetime


class scales_bot_1(stand_task.timer):
    def __init__(self, targets=None):
        '''
        the init func for timer.
        nextdate    func        : give the datetime of now, cal the next date.
        once the time nextdate get, it will send msg.
        '''
        super().__init__()
        self.id = 'laxect.scale_bot_1'

    def next_time(self, now_time):
        return datetime.datetime(now_time.year, now_time.month, now_time.day+1)

    def action(self, mail_service, targets, inbox=None):
        message = '又熬夜到 12:00 了哦， 快睡！\n'
        mail_service.put(self.gen_msg_pack(message))


def mod_init(targets=None):
    return scales_bot_1(targets)
