from models.exceptions import APIDataException
from models.vacancy import Vacancy
from api_models.hh_api import HeadHunterAPI
from api_models.sj_api import SuperJobAPI


class SearchFilter:
    total_vacancies = 0
    filtered_vacancies = []

    @classmethod
    def search_processing(cls, class_names: list, query: str, **kwargs) -> bool:
        """Обрабатывает запросы на HeadHunter и SuperJob.
        :param class_names: Названия классов API.
        :param query: Поисковый запрос.
        :param kwargs: Параметры API.
        :return: Возвращает True, если вакансии найдены.
        """
        num_of_vacancies = 0
        print(f'\nПо запросу "{query}"')

        for class_name in class_names:
            class_api = globals()[class_name]()  # Создаем экземпляр класса class_name
            try:
                vacancies = class_api.get_vacancies(query)
            except APIDataException as err:
                print(err.message)
                return False

            if vacancies:
                num_of_vacancies = len(vacancies)
                # удаляем последние 3 символа от имени класса
                print(f'найдено вакансий на {class_name[:-3]}: {num_of_vacancies}')
                for vacancy in vacancies:
                    Vacancy(**vacancy)
            else:
                print(f'на {class_name[:-3]} ничего не найдено.\nИзмените параметры запроса')
            cls.total_vacancies += num_of_vacancies

        print(f'------------------\nВсего вакансий: {cls.total_vacancies}\n')
        return bool(vacancies)

    @classmethod
    def filter_processing(cls, filter_keyword: str, **kwargs) -> bool:
        non_filtered_vacancies = Vacancy.get_all_vacancies()
        # cls.filtered_vacancies = list(filter(lambda key: (key == filter_keyword), non_filtered_vacancies))
        cls.filtered_vacancies = list(filter(lambda key: (key.city == filter_keyword), non_filtered_vacancies))
        # list(filter(lambda dic: (dic['state'] == 'EXECUTED'), non_empty_transactions))

        print(f'\nПо фильтру "{filter_keyword}"')
        if cls.filtered_vacancies:
            num_of_vacancies = len(cls.filtered_vacancies)
            print(f'найдено вакансий: {num_of_vacancies}')
            # return cls.filtered_vacancies
        else:
            print(f'\nничего не найдено.\nИзмените параметры фильтра')
        return bool(cls.filtered_vacancies)
