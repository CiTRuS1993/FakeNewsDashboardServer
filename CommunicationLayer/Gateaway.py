import time
from dataclasses import asdict

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
    print(f"get_temp = {dashboard_facade.getTemperature()}")
    return jsonify(dashboard_facade.getTemperature())
    # return jsonify({'sentiment': 42, 'fakiness': 38, 'authenticity': 15})


@app.route('/getEmotions', methods=['get'])
def get_emotions():
    print(f"get_emotions = {dashboard_facade.get_emotions()}")
    return jsonify(dashboard_facade.get_emotions())


@app.route('/getTrends')
def get_trends():
    print(f"get_trends = {dashboard_facade.googleTrendsStatistics()}")
    return jsonify(dashboard_facade.googleTrendsStatistics())
# {"Donald Trump": {'words': [
#         {
#             'text': 'told',
#             'value': 64,
#         },
#         {
#             'text': 'mistake',
#             'value': 11,
#         },
#         {
#             'text': 'thought',
#             'value': 16,
#         },
#         {
#             'text': 'bad',
#             'value': 17,
#         },
#     ], 'statistics': {
#         'mainEmo': "fear", 'avgSentiment': -1, 'avgAuthenticity': 17, 'avgFakiness': 78
#     }},
#         "some Trends": {'words': [
#             {'text': 'foos',
#              'value': 23},
#             {'text': 'other',
#              'value': 50},
#             {
#                 'text': 'thought',
#                 'value': 16,
#             },
#             {
#                 'text': 'bad',
#                 'value': 17,
#             },
#         ], 'statistics': {
#             'mainEmo': "happy", 'avgSentiment': 3, 'avgAuthenticity': 87, 'avgFakiness': 2
#         }}
#     }


@app.route('/getEmotionsTweet')
def get_emotions_tweet():
    emotion = request.args.get('emotion')
    return jsonify({'tweets': [{'id': "1361577298282094592", 'emotion': "happy", 'real': "fake",'sentiment': 3},
                               {'id': "1361577298282094592", 'emotion': "happy", 'real': "true", 'sentiment': 3}]})


@app.route('/getSentiment')
def get_sentiment():
    print(f"get_sentiment = {asdict(dashboard_facade.get_sentiment())}")
    return jsonify(asdict(dashboard_facade.get_sentiment()))


@app.route('/getTopic')
def get_topic():
    t = request.args.get('topic') # t = id of topic
    return jsonify({'tweets': [{'id': "1361577298282094592", 'emotion': "happy", 'real': "fake", 'sentiment': 3},
                               {'id': "1361577298282094592", 'emotion': "happy", 'real': "true", 'sentiment': -2}],
                    'emotions': [{'y': 32, 'label': "Anger"},
                                 {'y': 22, 'label': "Disgust"},
                                 {'y': 15, 'label': "Sad"},
                                 {'y': 19, 'label': "Happy"},
                                 {'y': 5, 'label': "Surprise"},
                                 {'y': 16, 'label': "Fear"}]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')   # TODO- https   https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https