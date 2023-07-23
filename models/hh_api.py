import json

import requests

from models.site_api import SiteAPI
from settings import HH_API_URL


class HeadHunterAPI(SiteAPI):

    # def __init__(self, search_string: str):
    #     self.search_string = search_string



    def get_vacancies(self, search_string) -> list[dict] | None:

        current_page = 0
        per_pages = 2
        request_params = {'search_field': 'name',
                          'per_page': per_pages,
                          'page': current_page,
                          'text': search_string}
        vacancies = []
        start = True

        while True:
            response = requests.get(HH_API_URL, params=request_params).json()
            # print(json.dumps(response, indent=4, ensure_ascii=False))

            if response['found'] == 0:  # Если не найдена ни одна вакансия, то возвращаем None
                return None

            if start:
                num_of_pages = response['pages']
                start = False
                print(num_of_pages)

            response_data = response['items']

            print(json.dumps(response_data, indent=4, ensure_ascii=False))

            for i in range(len(response_data)):  # Цикл по вакансиям на странице
                # Если нет словаря с зарплатой, или не указаны её верхняя или нижняя граница,
                # то присваиваем границам нулевые значения
                salary_from = 0
                salary_to = 0
                # Если же есть словарь со значениями одной из границ или обеих, то присваиваем их
                if response_data[i]['salary'] is not None and response_data[i]['salary']['from'] is not None:
                    salary_from = response_data[i]['salary']['from']
                if response_data[i]['salary'] is not None and response_data[i]['salary']['to'] is not None:
                    salary_to = response_data[i]['salary']['to']

                vacancies += [{
                        'vacancy_id': response_data[i]['id'],
                        'name': response_data[i]['name'],
                        'employer': response_data[i]['employer']['name'],
                        'city': response_data[i]['area']['name'],
                        'employment': response_data[i]['employment']['name'],
                        'salary_from': salary_from,
                        'salary_to': salary_to,

                        'experience': response_data[i]['experience']['name'],
                        'requirement': response_data[i]['snippet']['requirement'],
                        'url': response_data[i]['url'],
                        'source': 'hh.ru',
                }]
            current_page += 1
            request_params.update({'page': current_page})
            if current_page == 3:  # num_of_pages + 1
                print(json.dumps(vacancies, indent=4, ensure_ascii=False))
                return vacancies

        # if response.status_code == 200:
        #     response_data = json.loads(response.text)
        #     print(json.dumps(response_data, indent=4, ensure_ascii=False))
        #     return response.json()['items']
        # else:
        #     return None

        # with open(filename) as file:
        #     try:
        #         return json.load(file)  # put JSON-data to a variable
        #     except json.decoder.JSONDecodeError:
        #         print("Invalid JSON")  # in case json is invalid
        #     else:
        #         print("Valid JSON")  # in case json is valid
