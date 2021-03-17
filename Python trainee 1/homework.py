import requests
from bs4 import BeautifulSoup


class Parser:
    """Класс для парсинга html страниц"""

    def __init__(self):
        pass

    @staticmethod
    def get_main_text(url):
        """Получить html страницы по url"""
        headers = {'User-Agent': 'Mozilla/5.0'}  # воспользуемся мозиллой в качестве юзер-агента
        source = requests.get(url, headers=headers)  # гет запрос по url
        main_text = source.text  # декодируем
        return main_text

    @staticmethod
    def parse_jobs_tut_by():
        """Парс jobs.tut.by вакансий по ключевому слову"""
        key = input('Какую вакансию ищем: ')  # получаем значения keyword с клавиатуры
        url = f'https://rabota.by/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text={key}'
        main_text = Parser.get_main_text(url)  # получаем html страницы по получившемуся url
        soup = BeautifulSoup(main_text, features="html.parser")  # инициализация BS
        # ищем div с классом и в полученном результате забираем все ссылки с определенным классом
        links = soup.find('div', {'class': 'vacancy-serp'}).findAll('a', {'class': 'HH-LinkModifier'})
        if len(links) == 0:  # если по ключевому слову ничего не найдено
            print('По введенному ключевому слову ничего не найдено!')
        else:
            # инициализация счетчиков
            count = 0
            count_python = 0
            count_linux = 0
            count_flask = 0
            for link in links:  # проход по каждому полученному линку
                second_url = link.get('href')  # получение значения href из строки
                count += 1
                second_main_text = Parser.get_main_text(
                    second_url)  # получаем html страницы по получившемуся second_url
                second_main_text_split = second_main_text.split()  # разбиваем слова из html по пробелу
                for w in second_main_text_split:  # проходимся по каждому слову и нахождении слова прибавляем к счетчику
                    if 'python' in w.lower():
                        count_python += 1
                    elif 'linux' in w.lower():
                        count_linux += 1
                    elif 'flask' in w.lower():
                        count_flask += 1
                print('==========================\n' + second_url)
            # вывод полученных значений
            print('\n==========================\n' + f'Просмотренно вакансий: {count}')
            print(f'Упоминаний \'python\': {count_python}')
            print(f'Упоминаний \'linux\': {count_linux}')
            print(f'Упоминаний \'flask\': {count_flask}' + '\n==========================')
            print('AVG python: ' + str(round((count_python / count), 1)))
            print('AVG linux: ' + str(round((count_linux / count), 1)))
            print('AVG flask: ' + str(round((count_flask / count), 1)) + '\n==========================')


def main():
    """Основная (начальная) точка"""
    Parser.parse_jobs_tut_by()


if __name__ == "__main__":
    main()
