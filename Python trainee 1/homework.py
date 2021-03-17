import requests
from bs4 import BeautifulSoup

vacancy = input('Какую вакансию ищем: ')
url = f'https://rabota.by/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text={vacancy}'
headers = {'User-Agent': 'Mozilla/5.0'}
source = requests.get(url, headers=headers)
main_text = source.text
soup = BeautifulSoup(main_text, features="html.parser")

links = soup.find('div', {'class': 'vacancy-serp'}).findAll('a', {'class': 'HH-LinkModifier'})
if len(links) == 0:
    print('По введенному ключевому слову ничего не найдено!')
else:
    count = 0
    count_python = 0
    count_linux = 0
    count_flask = 0
    for link in links:
        second_url = link.get('href')
        count += 1
        second_source = requests.get(second_url, headers=headers)
        second_main_text = second_source.text
        second_main_text_split = second_main_text.split()
        for w in second_main_text_split:
            if 'python' in w.lower():
                count_python += 1
            elif 'linux' in w.lower():
                count_linux += 1
            elif 'flask' in w.lower():
                count_flask += 1
        print('===============\n' + second_url)
    print(count)
    print(count_python)
    print(count_linux)
    print(count_flask)

    print('AVG python: ' + str(round((count_python / count), 1)))
    print('AVG linux: ' + str(round((count_linux / count), 1)))
    print('AVG flask: ' + str(round((count_flask / count), 1)))
