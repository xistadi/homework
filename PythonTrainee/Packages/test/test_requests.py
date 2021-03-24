from Packages.get_requests import GetRequests
import pytest


@pytest.fixture()
def response(url):
    response = GetRequests(url).get_response()
    return response


@pytest.fixture()
def main_text(url):
    main_text = GetRequests(url).get_main_text(GetRequests(url).get_response())
    return main_text


class TestRequests:
    @pytest.mark.parametrize('url', ['https://rabota.by'])
    def test_request_page_available(self, response):
        """Test request page available"""
        assert response.ok, 'Ошибка в статус коде'

    @pytest.mark.parametrize('url', ['https://rabota.by/asdwq'])
    def test_request_page_unavailable(self, response):
        """Test request page unavailable"""
        assert response is None, 'Ошибка в статус коде'

    @pytest.mark.parametrize('url', ['https://rabota.by'])
    def test_get_main_text_page_available(self, main_text):
        """Test get main_text page available"""
        assert main_text != '', 'Ошибка в получении main_text'
