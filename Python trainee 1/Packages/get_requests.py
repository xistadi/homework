import requests


class GetRequests:
    """Класс для работы с библиотекой requests"""

    def __init__(self, url):
        self.url = url

    def get_main_text(self):
        """Получить html страницы по url"""
        headers = {'User-Agent': 'Mozilla/5.0'}  # воспользуемся мозиллой в качестве юзер-агента
        source = requests.get(self.url, headers=headers)  # гет запрос по url
        main_text = source.text  # декодируем
        return main_text


if __name__ == "__main__":
    GetRequests('http://google.com').get_main_text()
