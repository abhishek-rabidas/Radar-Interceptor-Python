import struct

from UMRR.Communication.MessageClasses import ObjectDetection, ObjectStatusMessage, StatusMessage


class DataCommunication:
    def __init__(self):
        self.object_detection_buffer = []

    def parse_status_message(self, payload):
        status_message = StatusMessage()
        status_message.timestamp = struct.unpack("<I", payload[4:8])[0]
        return status_message

    def parse_object_status_message(self, payload):
        object_status_message = ObjectStatusMessage()
        object_status_message.num_objects = payload[0]
        object_status_message.num_msgs = payload[1]
        object_status_message.cycle_duration = payload[2]
        object_status_message.cycle_count = struct.unpack("<I", payload[4:8])[0]
        # TODO: return __str__()
        print(
            f"OBJ MSG>CC: [{object_status_message.cycle_count}], dur: [{object_status_message.cycle_duration}], numObjects: [{object_status_message.num_objects}], numMsgs: [{object_status_message.num_msgs}]")

    def parse_object_data(self, payload, timestamp):
        object_detection = ObjectDetection()
        object_detection.Time = timestamp

        value = struct.unpack("<II", payload[0:8])[0]
        xp1 = value & 0b00000000_00000000_00000000_00000000_00000000_00000000_00111111_11111110 >> 1
        yp1 = value & 0b00000000_00000000_00000000_00000000_00000111_11111111_11000000_00000000 >> 14
        sx1 = value & 0b00000000_00000000_00000000_00111111_11111000_00000000_00000000_00000000 >> 27
        sy1 = value & 0b00000000_00000001_11111111_11000000_00000000_00000000_00000000_00000000 >> 38
        oll = value & 0b00000000_11111110_00000000_00000000_00000000_00000000_00000000_00000000 >> 49
        oid = value & 0b11111111_00000000_00000000_00000000_00000000_00000000_00000000_00000000 >> 56

        object_detection.ObjectID = int(oid)
        object_detection.X = (float(xp1) - 4096) * 0.128
        object_detection.Y = (float(yp1) - 4096) * 0.128
        object_detection.X_Speed = (float(sx1) - 1024) * 0.1
        object_detection.Y_Speed = (float(sy1) - 1024) * 0.1
        object_detection.Length = float(oll) * 0.2

        # caching object detection output
        if len(self.object_detection_buffer) > 10:
            self.object_detection_buffer.clear()
        else:
            self.object_detection_buffer.append(object_detection)

        return object_detection.__str__()

    def parse_sync_message(self, payload):
        pass
