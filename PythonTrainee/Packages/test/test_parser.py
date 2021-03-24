from Packages.parser import Parser
import pytest


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


class TestParser:
    @pytest.mark.xfail
    @pytest.mark.parametrize('url', ['https://rabota.by/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=shotgun'])
    def test_shotgun(self, parser_url):
        """Test that there are no search results for the word "shotgun"""
        assert len(parser_url.links) == 0, 'Ошибка в статус коде'

    @pytest.mark.parametrize('url', ['https://rabota.by/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=shotgun'])
    def test_shotgun_second(self, parser_url):
        """Check if there are any search results for the word "shotgun"""
        assert len(parser_url.links) > 0, 'Ошибка в статус коде'

    def test_boundaries_avg(self, parser):
        """Test that the occurrence of words "python", "linux", "flask" is within boundaries avg +-20"""
        mistakes = ''
        for key, value in parser.dict_avg_count.items():
            if (value + 20) > parser.dict_word_count[key] / parser.count > (value - 20):  # if located within the boundaries of avg +20
                pass
            else:
                mistakes += key  # adding keys to the error output string
        assert len(mistakes) == 0, f'Ошибка по словам: {mistakes}'

    def test_keywords_not_zero(self, parser):
        """Check that the occurrence of the words "python", "linux", "flask" is not zero"""
        mistakes = ''
        for key, value in parser.dict_word_count.items():
            if value > 0:  # if count word value > 0
                pass
            else:
                mistakes += key  # adding keys to the error output string
        assert len(mistakes) == 0, f'Ошибка по словам: {mistakes}'
