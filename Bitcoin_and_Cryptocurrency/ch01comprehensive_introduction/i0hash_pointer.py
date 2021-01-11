import datetime
import hashlib
import time
from termcolor import colored

class Message:
    def __init__(self, data):
        self.hash = None
        self.prev_hash = None
        self.timestamp = time.time()
        self.size = len(data.encode('utf-8'))
        self.data = data
        self.payload_hash = self._hash_payload()


    def _hash_payload(self):
        return hashlib.sha256(bytearray(str(self.timestamp) + str(self.data), "utf-8")).hexdigest()


    def _hash_message(self):
        return hashlib.sha256(bytearray(str(self.prev_hash) + self.payload_hash, "utf-8")).hexdigest()


    def seal(self):
        """ Get the message hash. """
        self.hash = self._hash_message()

    def __repr__(self):
        return 'Message<### hash: {}, prev_hash: {}, data: {} ###>'.format(
            self.hash, self.prev_hash, self.data[:20]
        )


if __name__ == "__main__":
    m0 = Message('test data0')
    m0.seal()
    print(colored('m0', 'red'))
    print(m0)

    m1 = Message('test data1')
    m1.seal()
    print(colored('m1', 'red'))
    print(m1)
