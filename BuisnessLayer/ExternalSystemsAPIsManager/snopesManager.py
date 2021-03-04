import os
import subprocess
import threading
import time

import pandas as pd
import schedule as schedule


class SnopesManager:
    def __init__(self):
        if os.path.exists("snopes.csv"):
            self.snopes = pd.read_csv('snopes.csv')[['claim', 'rating']].dropna().to_dict('index')
        else:
            self.snopes = {}
        self.quit = False

    def get_snopes(self):
        return self.snopes


    def search_snopes(self):

        import os
        cwd = os.getcwd()
        if os.path.exists("snopes.csv"):
            os.remove("snopes.csv")
        if os.path.exists("BuisnessLayer\ExternalSystemsAPIsManager\scrapy_snopes.py"):
            process = subprocess.call(["python","scrapy_snopes.py"])#, stdout=open(os.devnull, 'wb'))
            self.snopes = pd.read_csv('BuisnessLayer\ExternalSystemsAPIsManager\snopes.csv')[['claim', 'rating']].dropna().to_dict('index')
        else:
            process = subprocess.call(["python", "../../../BuisnessLayer\ExternalSystemsAPIsManager\scrapy_snopes.py"], stdout=open(os.devnull, 'wb'))
            self.snopes = pd.read_csv("../../../BuisnessLayer\ExternalSystemsAPIsManager\snopes.csv")[['claim', 'rating']].dropna().to_dict('index')

        print('searched')

    def stop(self):
        self.quit = False

    def start(self):
        def scrap():
            self.search_snopes()
            self.quit = True
            schedule.every().day.at("15:40").do(lambda: self.search_snopes())
            while self.quit:
                schedule.run_pending()
                time.sleep(24 * 360)

        search_thread = threading.Thread(target=scrap)
        search_thread.setDaemon(True)
        search_thread.start()
