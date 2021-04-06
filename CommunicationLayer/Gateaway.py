import time
from dataclasses import asdict

from flask import Flask, abort, request, jsonify, g, url_for
from flask_cors import CORS

from CommunicationLayer import app
from ServiceLayer.DashboardFacade import DashboardFacade

dashboard_facade = DashboardFacade("username", "123") # TODO
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
    return jsonify(asdict(dashboard_facade.getTemperature()))
    # return jsonify({'sentiment': 42, 'fakiness': 38, 'authenticity': 15})


@app.route('/getEmotions', methods=['get'])
def get_emotions():
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
    print(dashboard_facade.get_emotion_tweets(emotion))
    return jsonify(dashboard_facade.get_emotion_tweets(emotion))


@app.route('/getSentiment')
def get_sentiment():
    return jsonify(asdict(dashboard_facade.get_sentiment()))


@app.route('/getTopic')
def get_topic():
    t = request.args.get('topic') # t = id of topic
    print(dashboard_facade.get_topic(t))
    return jsonify(dashboard_facade.get_topic(t))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')   # TODO- https   https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https