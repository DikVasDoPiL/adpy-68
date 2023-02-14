import requests as req
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
import re
from time import sleep
import json


def get_vacancies(res):
    soup = BS(res.text, 'lxml')
    return soup.find_all(class_="serp-item")


def get_result(vacancies):
    result = {}
    print(f'Поиск в {len(vacancies)} предложениях')
    if vacancies:
        i = 1
        for vacancy in vacancies:
            sleep(1)
            link = vacancy.find(class_="serp-item__title").get('href')
            current = req.get(link, headers=HEADERS)
            current_soup = BS(current.text, 'lxml')
            soup_description = current_soup.find(class_="g-user-content")
            description_text = soup_description.get_text(separator='\n')
            pattern_search = re.compile(r'(Django.*Flask)|(Flask.*Django)')
            matches = pattern_search.findall(description_text)

            if matches:
                soup_salary = current_soup.find(
                    class_="vacancy-title").find(class_="bloko-header-section-2").get_text()
                soup_company = current_soup.find(
                    class_="vacancy-company-redesigned")
                company_name = soup_company.find(
                    'span', {"class": "vacancy-company-name"}).get_text()
                soup_location = soup_company.find(
                    'p', {"data-qa": "vacancy-view-location"})
                if soup_location:
                    company_location = soup_location.get_text().split(',')[0]
                print(link, soup_salary, company_name,
                      company_location, sep='\n')
                result[i] = {
                    'link': link,
                    'salary': soup_salary.replace(u'\xa0', u' '),
                    'company': company_name.replace(u'\xa0', u' '),
                    'location': company_location
                }
                i += 1
        print(f'Найдено всего предложений: {i-1}')
    else:
        print('Не найдено совпадений')
    return result


if __name__ == '__main__':
    ua = UserAgent()
    URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    HEADERS = {
        "Accept-Language": "ru-RU,ru;q=0.5",
        "User-Agent": ua.random
    }
    res = req.get(URL, headers=HEADERS)
    vacancies = get_vacancies(res)

    with open('vacancies.json', 'w', encoding='utf-8') as out:
        out.write(json.dumps(get_result(vacancies)))
