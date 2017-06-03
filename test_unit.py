class test_output:
    def run(self, queue):
        while True:
            item = queue.get()
            print(item)


def mod_init():
    return test_output()
