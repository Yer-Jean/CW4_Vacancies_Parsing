import json

import requests

from models.site_api import SiteAPI
from models.validate_mixin import ValidateMixin
from settings import HH_API_URL


class HeadHunterAPI(SiteAPI, ValidateMixin):

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
            if response['found'] == 0:  # Если не найдена ни одна вакансия, то возвращаем None
                return None

            if start:
                num_of_pages = response['pages']
                start = False
                print(num_of_pages)

            response_data = response['items']

            print(json.dumps(response_data, indent=4, ensure_ascii=False))

            for i in range(len(response_data)):  # Цикл по вакансиям на странице
                vacancies += [{
                    'vacancy_id': response_data[i]['id'],  # id - обязательный параметр, валидация не нужна
                    'name': response_data[i]['name'],  # name - обязательный параметр, валидация не нужна
                    'employer': response_data[i]['employer']['name'],  # name - обязательный параметр, валидация не нужна
                    'city': response_data[i]['area']['name'],  # name - обязательный параметр, валидация не нужна
                    'employment': self.validate_value(response_data[i], 'str', 'employment', 'name'),
                    'salary_from': self.validate_value(response_data[i], 'int', 'salary', 'from'),
                    'salary_to': self.validate_value(response_data[i], 'int', 'salary', 'to'),
                    'experience': self.validate_value(response_data[i], 'str', 'experience', 'name'),
                    'requirement': self.validate_value(response_data[i], 'str', 'snippet', 'requirement'),
                    'url': response_data[i]['url'],     # url - обязательный параметр, валидация не нужна
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
