import json
class Information():
    def __init__(self):
        pass

    def get_data_from_json(self, file):
        with open(file) as file_json:
            config = json.load(file_json)
        return config