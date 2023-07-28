from models.exceptions import APIDataException
from models.vacancy import Vacancy
from api_models.hh_api import HeadHunterAPI
from api_models.sj_api import SuperJobAPI


class SearchFilter:
    total_vacancies: int = 0
    filter_keyword: str = ''
    filtered_vacancies: list = []

    @classmethod
    def search_processing(cls, class_names: list, query: str) -> bool:
        """Обрабатывает запросы на HeadHunter и SuperJob.
        :param class_names: Названия классов API.
        :param query: Поисковый запрос.
        :param kwargs: Параметры API.
        :return: Возвращает True, если вакансии найдены.
        """
        num_of_vacancies: int = 0
        vacancies: list = []
        print(f'\nПо запросу "{query}"')

        for class_name in class_names:
            class_api = globals()[class_name]()  # Создаем экземпляр класса class_name
            try:
                finding_vacancies: list | None = class_api.get_vacancies(query)
            except APIDataException as err:
                print(err.message)
                # continue
                # return False

            if finding_vacancies:
                num_of_vacancies = len(finding_vacancies)
                vacancies += finding_vacancies
                cls.total_vacancies += num_of_vacancies
                # удаляем последние 3 символа от имени класса
                print(f'найдено вакансий на {class_name.replace("API", "")}: {num_of_vacancies}')
                for vacancy in finding_vacancies:
                    Vacancy(**vacancy)
            else:
                print(f'на {class_name.replace("API", "")} ничего не найдено.\nИзмените параметры запроса')

        print(f'------------------\nВсего вакансий: {cls.total_vacancies}\n')
        return bool(vacancies)

    @staticmethod
    def filter_list(vacancies) -> bool:
        for key in vacancies.__dict__:
            if type(vacancies.__dict__[key]) == str:
                if SearchFilter.filter_keyword.lower() in vacancies.__dict__[key].lower():
                    return True
        return False

    @classmethod
    def filter_processing(cls) -> bool:
        non_filtered_vacancies: list = Vacancy.get_all_vacancies()
        cls.filtered_vacancies = list(filter(cls.filter_list, non_filtered_vacancies))
        # cls.filtered_vacancies = list(filter(lambda dic: (dic['state'] == 'EXECUTED'), non_filtered_vacancies)

        print(f'\nПо фильтру "{SearchFilter.filter_keyword}"')
        if cls.filtered_vacancies:
            num_of_vacancies = len(cls.filtered_vacancies)
            print(f'найдено вакансий: {num_of_vacancies}')
        else:
            print(f'ничего не найдено.\nИзмените параметры фильтра')
        return bool(cls.filtered_vacancies)
