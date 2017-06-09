'standard store modules for scale.'
import json
import hashlib


class data_file():
    'the class that save data, use a hash dict to store nearly all thing'
    def __init__(self, sid):
        import sys
        self.path = sys.path[0]+'/laxect.data_file.1.0.0.tmp'
        self.id = sid

    def __enter__(self):
        # special design for with
        try:
            with open(self.path, 'r') as tmp_file:
                self.dict = json.loads(tmp_file.read())
        except FileNotFoundError:
            self.dict = {}
        return self

    def _hash(self, text):
        # in prevent that text may contain chinese, that check_up_to_date()
        # function can't work proprely, so i change all text to hex number.
        res = hashlib.new('ripemd160')
        res.update(str(text).encode('utf-8'))
        return res.hexdigest()

    def check_up_to_date(self, text):
        'check if a index is in store'
        text = self._hash(text)
        if self.dict.get(self.id) == text:
            return False
        else:
            self.dict[self.id] = text
            return True

    def __exit__(self, exc_ty, exc_val, tb):
        with open(self.path, 'w+') as tmp_file:
            tmp_file.write(json.dumps(self.dict))
        del self.dict
