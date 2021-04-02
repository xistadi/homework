import requests
import flask
from flask import jsonify, request


class Reaper:
    """Class reaper"""

    def __init__(self):
        self.all_rate = []

    def scrape_from_api(self):
        """Scrape api nbrb.by exchange rates"""
        url = 'https://www.nbrb.by/api/exrates/rates?periodicity=0'
        source = requests.get(url)  # get api from nbrb
        self.all_rate = source.json()
        self.all_rate = [rate for rate in self.all_rate]  # list comprehension for all_rate

    def input_all_rate(self):
        """Input all_rate to localhost port 3300"""
        app = flask.Flask(__name__)
        app.config["DEBUG"] = True

        @app.route('/', methods=['POST', 'GET'])
        def home():
            if request.method == 'POST':
                a = Reaper()
                a.scrape_from_api()
                return flask.redirect('http://localhost:3100')
            else:
                return jsonify(self.all_rate)
        app.run(host='0.0.0.0', port=3300)


if __name__ == "__main__":
    a = Reaper()
    a.scrape_from_api()
    a.input_all_rate()
