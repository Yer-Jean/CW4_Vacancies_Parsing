from api_models.site_api import SiteAPI
from api_models.get_remote_data_mixin import GetRemoteData
from api_models.validate_mixin import ValidateMixin
from models.exceptions import GetRemoteDataException
from settings import SJ_API_KEY, SJ_API_URL, RESULTS_PER_PAGE


class SuperJobAPI(SiteAPI, ValidateMixin, GetRemoteData):
    __sj_api_url = SJ_API_URL
    __sj_api_key = SJ_API_KEY

    def get_vacancies(self, search_string) -> list[dict] | None:
        vacancies = []
        current_page = 0
        __headers = {'X-Api-App-Id': SJ_API_KEY}
        request_params = {'keys': search_string,
                          'count': RESULTS_PER_PAGE,
                          'page': current_page}
        start = True

        while True:
            try:
                data = self.get_remote_data(url=self.__sj_api_url,
                                            headers=__headers,
                                            params=request_params)
            except GetRemoteDataException as err:  # Если произошли ошибки, то возвращаем None
                print(err.message)
                print('\nПопробуйте немного позже или измените параметры запроса')
                return None
            if data['total'] == 0:  # Если не найдена ни одна вакансия, то возвращаем None
                # print('\nПо вашему запросу на HeadHunter ничего не найдено. Измените параметры запроса')
                return None

            if start:
                num_of_vacancies = data['total']
                if num_of_vacancies == 0:  # Если не найдена ни одна вакансия, то возвращаем None
                    return None
                start = False

            vacancies_data = data['objects']
            # print(json.dumps(vacancies_data, indent=4, ensure_ascii=False))
            for i in range(len(vacancies_data)):  # Цикл по вакансиям на странице
                vacancies += [{
                    'vacancy_id': vacancies_data[i]['id'],
                    'name': vacancies_data[i]['profession'],
                    'employer': vacancies_data[i]['firm_name'],
                    'city': vacancies_data[i]['town']['title'],
                    # Со следующими двумя параметрами надо поработать
                    'employment': self.validate_value(vacancies_data[i], 'str', 'type_of_work', 'title'),
                    'schedule': self.validate_value(vacancies_data[i], 'str', 'place_of_work', 'title'),
                    'salary_from': vacancies_data[i]['payment_from'],
                    'salary_to': vacancies_data[i]['payment_to'],
                    'currency': vacancies_data[i]['currency'],
                    'experience': self.validate_value(vacancies_data[i], 'str', 'experience', 'title'),
                    'requirement': vacancies_data[i]['vacancyRichText'],
                    'url': vacancies_data[i]['link'],
                    'source': 'superjob.ru',
                }]

            current_page += 1
            request_params.update({'page': current_page})
            if not data['more']:  # Страницы результатов заканчиваются, когда параметр more = False
                # print(num_of_vacancies)
                return vacancies
