from bs4 import BeautifulSoup
from .get_requests import GetRequests


class Parser:
    """Класс для парсинга html страниц"""

    def __init__(self):
        self.count = 0
        self.dict_word_count = {}
        self.url = ''
        self.links = []
        self.soup = ''
        self.main_text = ''

    def get_url_jobs_tut_by_for_parse(self):
        """Получить url jobs.tut.by для парсинга"""
        keyword = input('Какую вакансию ищем: ')  # получаем значения keyword с клавиатуры
        self.url = f'https://rabota.by/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text={keyword}'

    def get_links_for_parse(self):
        """Парс html jobs.tut.by для получения линков вакансий"""
        self.main_text = GetRequests(self.url).get_main_text()  # получаем html страницы по получившемуся url
        self.soup = BeautifulSoup(self.main_text, features="html.parser")  # инициализация BS
        # Ищем div с классом и в полученном результате забираем все ссылки с определенным классом
        self.links = self.soup.find('div', {'class': 'vacancy-serp'}).findAll('a', {'class': 'HH-LinkModifier'})

    def parse_jobs_tut_by(self):
        """Парс jobs.tut.by вакансий по ключевому слову"""
        if len(self.links) == 0:  # если по ключевому слову ничего не найдено
            print('По введенному ключевому слову ничего не найдено!')
        else:  # если же что-то нашли
            words_count = input('Какие слова ищем?(введите через пробел): ').split()
            for word_key in words_count:
                self.dict_word_count[word_key] = 0  # записываем key и value = 0 в словарь
            for link in self.links:  # проход по каждому полученному линку
                second_url = link.get('href')  # получение значения href из строки
                self.count += 1
                second_main_text = GetRequests(second_url).get_main_text()  # получаем html страницы по second_url
                second_main_text_split = second_main_text.lower().split()  # разбиваем слова из html по пробелу
                for word_second_main_text in second_main_text_split:  # проходимся по каждому слову
                    for key in self.dict_word_count.keys():
                        if key in word_second_main_text:  # при нахождении слова прибавляем к value по key
                            self.dict_word_count[key] += 1
                print('==========================\n' + second_url)

    def output_values(self):
        """Вывод полученных значений"""
        print('\n==========================\n' + f'Просмотренно вакансий: {self.count}')
        for key, value in self.dict_word_count.items():
            print(f'Упоминаний \'{key}\': {value}')
        print('==========================')
        for key, value in self.dict_word_count.items():
            print(f'AVG {key}: ' + str(round((value / self.count), 1)))


if __name__ == "__main__":
    a = Parser()
    a.get_url_jobs_tut_by_for_parse()
    a.get_links_for_parse()
    a.parse_jobs_tut_by()
    a.output_values()
