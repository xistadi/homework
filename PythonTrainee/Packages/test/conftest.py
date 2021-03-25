from Packages.getrequests import GetRequests
from Packages.parser import Parser
import pytest


@pytest.fixture()
def response(url):
    response = GetRequests(url).get_response()
    return response


@pytest.fixture()
def main_text(url):
    main_text = GetRequests(url).get_main_text(GetRequests(url).get_response())
    return main_text

@pytest.fixture()
def parser_url(url):
    parser_url = Parser()
    parser_url.url = url
    parser_url.get_soup()
    parser_url.get_links_for_parse()
    return parser_url


@pytest.fixture(scope="class")
def parser():
    parser = Parser()
    parser.url = 'https://rabota.by/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=python'
    parser.get_soup()
    parser.get_links_for_parse()
    parser.dict_word_count = {'python': 0, 'linux': 0, 'flask': 0}  # enter the keywords values
    parser.parse_jobs_tut_by()
    parser.get_avg_word_count()
    return parser
