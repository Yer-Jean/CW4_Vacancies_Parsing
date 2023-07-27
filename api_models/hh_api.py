from models.exceptions import GetRemoteDataException
from api_models.site_api import SiteAPI
from api_models.get_remote_data_mixin import GetRemoteData
from api_models.validate_mixin import ValidateMixin
from settings import HH_API_URL, RESULTS_PER_PAGE


class HeadHunterAPI(SiteAPI, ValidateMixin, GetRemoteData):
    __hh_api_url = HH_API_URL

    def get_vacancies(self, search_string) -> list[dict] | None:
        vacancies = []
        current_page = 0
        request_params = {'search_field': 'name',
                          'text': search_string,
                          'per_page': RESULTS_PER_PAGE,
                          'page': current_page}
        start = True

        while True:
            try:
                data = self.get_remote_data(url=self.__hh_api_url, params=request_params)
            except GetRemoteDataException as err:  # Если произошли ошибки, то возвращаем None
                print(err.message)
                print('\nПопробуйте немного позже или измените параметры запроса')
                return None

            if start:
                num_of_pages = data['pages']
                num_of_vacancies = data['found']
                if num_of_vacancies == 0:  # Если не найдена ни одна вакансия, то возвращаем None
                    # print('\nПо вашему запросу на HeadHunter ничего не найдено. Измените параметры запроса')
                    return None
                    # raise GetRemoteDataException('По вашему запросу ничего не найдено')
                start = False

            vacancies_data = data['items']
            # print(json.dumps(vacancies_data, indent=4, ensure_ascii=False))

            for i in range(len(vacancies_data)):  # Цикл по вакансиям на странице
                vacancies += [{
                    'vacancy_id': vacancies_data[i]['id'],
                    'name': vacancies_data[i]['name'],
                    'employer': vacancies_data[i]['employer']['name'],
                    'city': vacancies_data[i]['area']['name'],
                    'employment': self.validate_value(vacancies_data[i], 'str', 'employment', 'name'),
                    'schedule': self.validate_value(vacancies_data[i], 'str', 'schedule', 'name'),
                    'salary_from': self.validate_value(vacancies_data[i], 'int', 'salary', 'from'),
                    'salary_to': self.validate_value(vacancies_data[i], 'int', 'salary', 'to'),
                    'currency': self.validate_value(vacancies_data[i], 'str', 'salary', 'currency'),
                    'experience': self.validate_value(vacancies_data[i], 'str', 'experience', 'name'),
                    'requirement': self.validate_value(vacancies_data[i], 'str', 'snippet', 'requirement'),
                    'url': vacancies_data[i]['alternate_url'],
                    'source': 'hh.ru',
                }]
            current_page += 1
            request_params.update({'page': current_page})
            if current_page == 3:  # num_of_pages + 1:
                # print(num_of_vacancies)
                ###### print(num_of_pages)
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
