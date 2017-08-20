

class task():
    # task template v1.0.0
    def __init__(self, targets=None):
        pass

    def _handle(self, target):
        return 'helloworld'

    def _run(self, targets):
        return self._handle(targets)

    def run(self, que, targets=None):
        if targets:
            self.targets = targets
        res = self._run(self.targets)
        for item in res:
            if item:
                que.put(item)
