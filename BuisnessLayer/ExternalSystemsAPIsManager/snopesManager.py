import os
import subprocess
import threading
import time

import pandas as pd
import schedule as schedule


class SnopesManager:
    def __init__(self):
        self.snopes = pd.read_csv('snopes.csv')[['claim', 'rating']].dropna().to_dict('index')
        self.quit = False

    def get_snopes(self):
        return self.snopes

    def search_snopes(self):
        if os.path.exists("snopes.csv"):
            os.remove("snopes.csv")
        process = subprocess.call(["python", "scrapy_snopes.py"], stdout=open(os.devnull, 'wb'))
        self.snopes = pd.read_csv('snopes.csv')[['claim', 'rating']].dropna().to_dict('index')
        print('searched')

    def stop(self):
        self.quit = False

    def start(self):
        def scrap():
            self.quit = True
            schedule.every().day.at("15:40").do(lambda: self.search_snopes())
            while self.quit:
                schedule.run_pending()
                time.sleep(24 * 360)

        search_thread = threading.Thread(target=scrap)
        search_thread.start()
