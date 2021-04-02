import requests
import flask
from flask import jsonify, render_template


class Master:
    """Class master"""

    def __init__(self):
        self.dict_for_api = {}

    def get_data_from_keeper(self):
        """Get json from keeper"""
        url = 'http://keeper:3200'  # url to get json dict from keeper
        source = requests.get(url)
        self.dict_for_api = source.json()

    def show_api(self):
        """Show dict api localhost port 3100"""
        app = flask.Flask(__name__)
        app.config["DEBUG"] = True

        @app.route('/', methods=['GET'])
        def home():
            return render_template('home.html', dict_for_api=self.dict_for_api)

        @app.route('/json', methods=['GET'])
        def json():
            return jsonify(self.dict_for_api)
        app.run(host='0.0.0.0', port=3100)


if __name__ == "__main__":
    a = Master()
    a.get_data_from_keeper()
    a.show_api()
