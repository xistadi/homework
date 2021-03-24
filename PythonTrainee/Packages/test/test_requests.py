from Packages.get_requests import GetRequests
import pytest


class TestRequests:
    def test_request_page_available(self):
        response = GetRequests('https://rabota.by/').get_response()
        assert response.ok, 'Ошибка в статус коде'


    def test_request_page_unavailable(self):
        response = GetRequests('https://rabota.by/asdqw').get_response()
        assert response == None, 'Ошибка в статус коде'
