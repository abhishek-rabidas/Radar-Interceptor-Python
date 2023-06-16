import socket
import struct

from Config import Config
from Radar import Radar
from UMRR.Communication import DataCommunication


def _reverse(payload):
    return payload[::-1]


class UMRR_Radar(Radar):

    def __init__(self):
        super().__init__()
        self.logging_status = None
        self.is_connected = None
        self.START = bytes([0xca, 0xcb, 0xcc, 0xcd])
        self.END = bytes([0xea, 0xeb, 0xec, 0xed])
        self.parser = DataCommunication()

    def connect(self):
        config = Config().load_config()

        address = config.IP, config.Port

        print(f"-----Connecting to [{address}]-----")
        connection = socket.create_connection(address)
        self.is_connected = True
        self.read_data(connection)

    def read_data(self, connection):
        while True:
            packet, err = self.pre_process_stream(connection)
            if err is None:
                self.packet_handler(packet)

    def pre_process_stream(self, stream):
        buf = bytearray(1)
        i = 0
        while True:
            byte_data = stream.recv(1)
            if not byte_data:
                return None, EOFError()
            buf[0] = byte_data[0]
            if buf[0] == self.START[i]:
                i += 1
            else:
                i = 0
            if i == len(self.START):
                break
        packet = bytearray(512)
        i = 0
        cnt = 0
        while True:
            byte_data = stream.recv(1)
            if not byte_data:
                return None, EOFError()
            buf[0] = byte_data[0]
            if buf[0] == self.END[i]:
                i += 1
            else:
                packet[cnt] = buf[0]
                cnt += 1
                i = 0
            if i == len(self.END):
                return packet[:cnt], None
        pass

    def packet_handler(self, packet):
        idx = 0
        packet_size = len(packet)
        time_stamp = None
        while idx < packet_size - 1:
            msg_type = struct.unpack('>H', packet[idx:idx + 2])[0]
            idx += 2
            msg_len = packet[idx]
            idx += 1
            payload = packet[idx:idx + msg_len]
            idx += msg_len
            if idx >= packet_size - 1:
                break
            payload = _reverse(payload)
            if msg_type == 0x0500:
                time_stamp = self.parser.parse_status_message(payload).timestamp
            elif msg_type == 0x0501:
                self.parser.parse_object_status_message(payload)
            elif msg_type == 0x02ff:
                self.parser.parse_sync_message(payload)
            elif 0x0502 <= msg_type <= 0x057F:
                print(self.parser.parse_object_data(payload, time_stamp))
            else:
                print(f"Unknown type: 0x{msg_type:X}")
