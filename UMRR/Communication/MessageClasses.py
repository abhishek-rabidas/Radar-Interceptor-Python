class ObjectDetection:
    def __init__(self):
        self.Time = 0
        self.ObjectID = 0
        self.X = 0.0
        self.Y = 0.0
        self.X_Speed = 0.0
        self.Y_Speed = 0.0
        self.Length = 0.0

    def __str__(self):
        return f"[Time: {self.Time}, ObjectID: {self.ObjectID}, X: {self.X}, Y: {self.Y}, X_Speed: {self.X_Speed}, Y_Speed: {self.Y_Speed}, Length: {self.Length}]"


class ObjectStatusMessage:
    def __init__(self):
        self.num_objects = 0
        self.num_msgs = 0
        self.cycle_duration = 0
        self.cycle_count = 0


class StatusMessage:
    def __init__(self):
        self.timestamp = 0



