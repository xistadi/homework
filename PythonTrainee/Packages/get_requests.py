import requests
from urllib.error import HTTPError


class GetRequests:
    """Class for working with the requests library"""

    def __init__(self, url):
        self.url = url

    def get_main_text(self):
        """Get html pages by url"""
        headers = {'User-Agent': 'Mozilla/5.0'}  # use mozilla as a user agent
        source = requests.get(self.url, headers=headers)  # get requests by url
        if source.status_code == 404:  # if status code equal 404
            raise HTTPError
        else:
            main_text = source.text  # decode it
            return main_text


if __name__ == "__main__":
    GetRequests('http://google.com').get_main_text()
