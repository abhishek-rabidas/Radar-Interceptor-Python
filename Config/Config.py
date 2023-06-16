import json


class Config:
    def __init__(self):
        self.IP = ""
        self.Port = ""
        self.OutputDir = ""
        self.PrintLog = None

    def load_config(self):
        config_file_path = "Config/config.json"

        try:
            with open(config_file_path, "r") as config_file:
                config_data = json.load(config_file)
                self.IP = config_data.get("Radar_IP", "")
                self.Port = config_data.get("Port", "")
                self.OutputDir = config_data.get("Output_Directory", "")
                self.PrintLog = config_data.get("PrintLog", "")
                print(f"Loaded config: {self.__dict__}")
                return self
        except Exception as e:
            print(e)
            return None
