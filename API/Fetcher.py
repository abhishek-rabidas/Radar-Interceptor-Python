from UMRR import UMRR_Radar


class Fetcher:

    def __init__(self):
        self.umrr = UMRR_Radar()
        self.umrr.connect()
        self.buffer = self.umrr.parser.OBJECT_DETECTION_BUFFER
        return

    def get_object_detection(self, size):
        if len(self.buffer) >= size:
            return self.buffer[:size]
        else:
            return self.buffer
