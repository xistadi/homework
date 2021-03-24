from Packages.parser import Parser
import pytest


class TestParser:
    @pytest.mark.xfail
    def test_shotgun(self):
        kek = Parser()
        kek.url = 'https://rabota.by/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=shotgun'
        kek.get_soup()
        kek.get_links_for_parse()
        assert len(kek.links) == 0, 'Ошибка в статус коде'

    def test_avg(self):
        oshibka = ''
        kek = Parser()
        kek.url = 'https://rabota.by/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=python'
        kek.get_soup()
        kek.get_links_for_parse()
        kek.dict_word_count = {'python': 0, 'linux': 0, 'flask': 0}
        kek.parse_jobs_tut_by()
        kek.get_avg()
        for key, value in kek.dict_avg_count.items():
            if (value + 20) > kek.dict_word_count[key] / kek.count > (value - 20):
                pass
            else:
                oshibka += key
        assert len(oshibka) == 0, f'Ошибка по словам: {oshibka}'
