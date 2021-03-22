from bs4 import BeautifulSoup
from Packages.get_requests import GetRequests


class Parser:
    """Class for parsing html pages"""

    def __init__(self):
        self.count = 0
        self.dict_word_count = {}
        self.url = ''
        self.links = []
        self.soup = ''
        self.main_text = ''

    def get_url_jobs_tut_by_for_parse(self):
        """Get url jobs.tut.by for parsing"""
        keyword = input('Какую вакансию ищем: ')  # getting the keyword values from the keyboard
        self.url = f'https://rabota.by/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text={keyword}'

    def get_links_for_parse(self):
        """Html parse jobs.tut.by to get job links"""
        self.main_text = GetRequests(self.url).get_main_text()  # getting html pages from the resulting url
        self.soup = BeautifulSoup(self.main_text, features="html.parser")  # BS Initialization
        # looking for a div with a class and in the resulting result we take all the links with a certain class
        self.links = self.soup.find('div', {'class': 'vacancy-serp'}).findAll('a', {'class': 'HH-LinkModifier'})

    def parse_jobs_tut_by(self):
        """Pars jobs.tut.by vacancies by keyword"""
        if len(self.links) == 0:  # if nothing is found for the keyword
            print('По введенному ключевому слову ничего не найдено!')
        else:  # if found something
            words_count = input('Какие слова ищем?(введите через пробел): ').split()
            for word_key in words_count:
                self.dict_word_count[word_key] = 0  # writing key and value = 0 to the dictionary
            for link in self.links:  # pass through each received link
                second_url = link.get('href')  # getting the href value from a string
                self.count += 1
                second_main_text = GetRequests(second_url).get_main_text()  # getting html pages by second_url
                second_main_text_split = second_main_text.lower().split()  # splitting words from html by space
                for word_second_main_text in second_main_text_split:  # go through each word
                    for key in self.dict_word_count.keys():
                        if key in word_second_main_text:  # when finding a word, we add it to value by key
                            self.dict_word_count[key] += 1
                print('==========================\n' + second_url)

    def output_values(self):
        """Output of the received values"""
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
