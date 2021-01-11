import datetime
import hashlib
import time


class Message:
    def __init__(self, data):
        self.hash = None
        self.prev_hash = None
        self.timestamp = time.time()
        self.size = len(data.encode('utf-8'))
        self.data = data

    def __repr__(self):
        return 'Message<### hash: {}, prev_hash: {}, data: {} ###>'.format(
            self.hash, self.prev_hash, self.data[:20]
        )


if __name__ == "__main__":
    m0 = Message('test data0')
    print(m0)
    m1 = Message('test data1')
    print(m1)
