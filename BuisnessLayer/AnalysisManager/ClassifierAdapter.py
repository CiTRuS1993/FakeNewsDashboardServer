import time
from random import random

def get_emotion_by_id(id):
    if id == 1:
        return 'Anger'
    elif id == 2:
        return 'Disgust'
    elif id == 3:
        return 'Sad'
    elif id == 4:
        return 'Happy'
    elif id == 5:
        return 'Surprise'
    else:
        return 'Fear'


class ClassifierAdapter:
    def __init__(self):
        pass

    def analyze(self, data, callback):  # data is tweets
        processed_data = {}
        for key in data.keys():
            rand = random.randint(100)
            if rand < 50:
                processed_data[key]['fake'] = "wow it's fake"
            else:
                processed_data[key]['fake'] = "100% true"
            processed_data[key]['sentiment'] = random.randint(-3, 3)
            rand = random.randint(6)
            processed_data[key]['emotional'] = get_emotion_by_id(rand)

        time.sleep(1)
        callback(processed_data)

