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
            response = requests.get(self.url, headers=headers)  # get requests by url
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  
        except Exception as err:
            print(f'Other error occurred: {err}')  
        else:
            print('Success!')
            return response

    def get_main_text(self, response):
        """Get html pages by url"""
        main_text = response.text  # decode response
        return main_text


if __name__ == "__main__":
    response = GetRequests('http://google.com').get_requests()
    print(GetRequests('http://google.com').get_main_text(response))
