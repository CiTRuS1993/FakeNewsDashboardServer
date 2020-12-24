import time


class ClassifierAdapter:
    def __init__(self):
        pass
    def analyze(self,data,callback):
        processed_data = {}
        for key in data.keys():
            processed_data[key] = "wow it's fake"
        time.sleep(1)
        callback(processed_data)