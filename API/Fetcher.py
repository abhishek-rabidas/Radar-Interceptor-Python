from UMRR.Communication import OBJECT_DETECTION_BUFFER
from UMRR import UMRR_Radar


class Fetcher:

    def __init__(self):
        umrr = UMRR_Radar()
        umrr.connect()
        return

    def get_object_detection(self, size):
        if len(OBJECT_DETECTION_BUFFER) >= size:
            return OBJECT_DETECTION_BUFFER[:size]
        else:
            return OBJECT_DETECTION_BUFFER
