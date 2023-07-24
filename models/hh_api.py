from models.exceptions import GetRemoteDataException
from models.site_api import SiteAPI
from models.get_remote_data_mixin import GetRemoteData
from models.validate_mixin import ValidateMixin
from settings import HH_API_URL


class HeadHunterAPI(SiteAPI, ValidateMixin, GetRemoteData):

    def get_vacancies(self, search_string) -> list[dict] | None:
        vacancies = []
        current_page = 0
        per_pages = 2
        request_params = {'search_field': 'name',
                          'per_page': per_pages,
                          'page': current_page,
                          'text': search_string}
        start = True

        while True:
            try:
                data = self.get_remote_data(url=HH_API_URL, params=request_params)
            except GetRemoteDataException as err:  # Если произошли ошибки, то возвращаем None
                print(err.message)
                print('\nПопробуйте немного позже или измените параметры запроса')
                return None

            if data['found'] == 0:  # Если не найдена ни одна вакансия, то возвращаем None
                print('\nПо вашему запросу на HeadHunter ничего не найдено. Измените параметры запроса')
                return None
                # raise GetRemoteDataException('По вашему запросу ничего не найдено')

            if start:
                num_of_pages = data['pages']
                start = False
                print(num_of_pages)

            vacancies_data = data['items']
            # print(json.dumps(vacancies_data, indent=4, ensure_ascii=False))

            for i in range(len(vacancies_data)):  # Цикл по вакансиям на странице
                vacancies += [{
                    'vacancy_id': vacancies_data[i]['id'],
                    'name': vacancies_data[i]['name'],
                    'employer': vacancies_data[i]['employer']['name'],
                    'city': vacancies_data[i]['area']['name'],
                    'employment': self.validate_value(vacancies_data[i], 'str', 'employment', 'name'),
                    'salary_from': self.validate_value(vacancies_data[i], 'int', 'salary', 'from'),
                    'salary_to': self.validate_value(vacancies_data[i], 'int', 'salary', 'to'),
                    'experience': self.validate_value(vacancies_data[i], 'str', 'experience', 'name'),
                    'requirement': self.validate_value(vacancies_data[i], 'str', 'snippet', 'requirement'),
                    'url': vacancies_data[i]['url'],
                    'source': 'hh.ru',
                }]
            current_page += 1
            request_params.update({'page': current_page})
            if current_page == 3:  # num_of_pages + 1
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
