import time

from flask import Flask, abort, request, jsonify, g, url_for
from flask_cors import CORS

from ServiceLayer.DashboardFacade import DashboardFacade

app = Flask(__name__)
cors = CORS(app)

dashboard_facade = DashboardFacade("username","123")
time.sleep(10)


@app.route('/get_fake_news_data', methods=['GET'])
def get_fake_news_data():
    return jsonify(dashboard_facade.retrieveFakeNewsData())

@app.route('/stop', methods=['GET'])
def stop():
    dashboard_facade.externalSystemsManager.extrenalManagerLogic.twitterManager.stop()
    return jsonify(True)

@app.route('/analyze', methods=['GET'])
def analyze():
    dashboard_facade.retrieveGoogleTrendsData()
    return jsonify(True)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
