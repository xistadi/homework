import requests
from requests.exceptions import HTTPError


class GetRequests:
    """Class for working with the requests library"""

    def __init__(self, url):
        self.url = url

    def get_response(self):
        """Get requests by url"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}  # use mozilla as a user agent
            response_from_requests = requests.get(self.url, headers=headers)  # get requests by url
            response_from_requests.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  
        except Exception as err:
            print(f'Other error occurred: {err}')  
        else:
            print('Success!')
            return response_from_requests

    def get_main_text(self, response_from_requests):
        """Get html pages by url"""
        main_text = response_from_requests.text  # decode response
        return main_text


if __name__ == "__main__":
    response = GetRequests('http://google.com').get_response()
    print(GetRequests('http://google.com').get_main_text(response))
