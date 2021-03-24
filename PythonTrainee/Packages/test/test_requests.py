from Packages.get_requests import GetRequests
import pytest


@pytest.fixture()
def response(params):
    response = GetRequests(params).get_response()
    return response


class TestRequests:
    @pytest.mark.parametrize('params', ['https://rabota.by'])
    def test_request_page_available(self, response):
        """Test request page available"""
        assert response.ok, 'Ошибка в статус коде'

    @pytest.mark.parametrize('params', ['https://rabota.by/asdwq'])
    def test_request_page_unavailable(self, response):
        """Test request page unavailable"""
        assert response is None, 'Ошибка в статус коде'
