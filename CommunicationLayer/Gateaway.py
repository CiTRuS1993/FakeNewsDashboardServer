import time

from flask import Flask, abort, request, jsonify, g, url_for
from flask_cors import CORS

from CommunicationLayer import app
from ServiceLayer.DashboardFacade import DashboardFacade

dashboard_facade = DashboardFacade("username", "123")
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


@app.route('/getTemp', methods=['get'])
def get_temp():
    return jsonify({'sentiment': 42, 'fakiness': 38, 'authenticity': 15})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)