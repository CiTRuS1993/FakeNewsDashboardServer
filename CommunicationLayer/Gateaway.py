import time

from flask import Flask, abort, request, jsonify, g, url_for
from flask_cors import CORS

from CommunicationLayer import app
from ServiceLayer.DashboardFacade import DashboardFacade

dashboard_facade = DashboardFacade("citrus", "123")
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


@app.route('/getEmotions', methods=['get'])
def get_emotion():
    return jsonify({'emotions': [
        {'y': 32, 'label': "Anger"},
        {'y': 22, 'label': "Disgust"},
        {'y': 15, 'label': "Sad"},
        {'y': 19, 'label': "Happy"},
        {'y': 5, 'label': "Surprise"},
        {'y': 16, 'label': "Fear"}
    ]})


@app.route('/getTrends')
def get_trends():
    return jsonify({"Donald Trump": {'words': [
        {
            'text': 'told',
            'value': 64,
        },
        {
            'text': 'mistake',
            'value': 11,
        },
        {
            'text': 'thought',
            'value': 16,
        },
        {
            'text': 'bad',
            'value': 17,
        },
    ], 'statistics': {
        'mainEmo': "fear", 'avgSentiment': -1, 'avgAuthenticity': 17, 'avgFakiness': 78
    }},
        "some Trends": {'words': [
            {'text': 'foos',
             'value': 23},
            {'text': 'other',
             'value': 50},
            {
                'text': 'thought',
                'value': 16,
            },
            {
                'text': 'bad',
                'value': 17,
            },
        ], 'statistics': {
            'mainEmo': "happy", 'avgSentiment': 3, 'avgAuthenticity': 87, 'avgFakiness': 2
        }}
    })


@app.route('/getEmotionsTweet')
def get_emotions_tweet():
    emotion = request.args.get('emotion')
    return jsonify({'tweets': [{'id': "1361577298282094592", 'emotion': "happy", 'real': "fake"},
                               {'id': "1361577298282094592", 'emotion': "happy", 'real': "true"}]})


@app.route('/getSentiment')
def get_sentiment():
    return jsonify({
        'topics': [
            {'y': 1, 'label': "1.1.2021"},
            {'y': 1, 'label': "2.1.2021"},
            {'y': -1, 'label': "3.1.2021"},
            {'y': 1, 'label': "4.1.2021"},
            {'y': 2, 'label': "5.1.2021"},
            {'y': 1, 'label': "6.1.2021"},
            {'y': 3, 'label': "7.1.2021"},
            {'y': -1, 'label': "8.1.2021"},
            {'y': 1, 'label': "9.1.2021"},
            {'y': 1, 'label': "10.1.2021"},
            {'y': -3, 'label': "11.1.2021"},
            {'y': 1, 'label': "12.1.2021"}
        ], 'trends': [
            {'y': 3, 'label': "1.1.2021"},
            {'y': 1, 'label': "2.1.2021"},
            {'y': 0, 'label': "3.1.2021"},
            {'y': 0, 'label': "4.1.2021"},
            {'y': 0, 'label': "5.1.2021"},
            {'y': 0, 'label': "6.1.2021"},
            {'y': 1, 'label': "7.1.2021"},
            {'y': -1, ' label': "8.1.2021"},
            {'y': 1, 'label': "9.1.2021"},
            {'y': 1, 'label': "10.1.2021"},
            {'y': 1, 'label': "11.1.2021"},
            {'y': -2, 'label': "12.1.2021"}
        ],
        'claims': [
            {'y': 1, 'label': "1.1.2021"},
            {'y': 1, 'label': "2.1.2021"},
            {'y': 3, 'label': "3.1.2021"},
            {'y': 2, 'label': "4.1.2021"},
            {'y': -1, ' label': "5.1.2021"},
            {'y': 1, 'label': "6.1.2021"},
            {'y': 1, 'label': "7.1.2021"},
            {'y': 0, 'label': "8.1.2021"},
            {'y': -3, ' label': "9.1.2021"},
            {'y': 1, 'label': "10.1.2021"},
            {'y': -2, ' label': "11.1.2021"},
            {'y': 1, 'label': "12.1.2021"}
        ]
    })


@app.route('/getTopic')
def get_topic():
    t = request.args.get('topic')
    return jsonify({'tweets': [{'id': "1361577298282094592", 'emotion': "happy", 'real': "fake"},
                               {'id': "1361577298282094592", 'emotion': "happy", 'real': "true"}],
                    'emotions': [{'y': 32, 'label': "Anger"},
                                 {'y': 22, 'label': "Disgust"},
                                 {'y': 15, 'label': "Sad"},
                                 {'y': 19, 'label': "Happy"},
                                 {'y': 5, 'label': "Surprise"},
                                 {'y': 16, 'label': "Fear"}]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
