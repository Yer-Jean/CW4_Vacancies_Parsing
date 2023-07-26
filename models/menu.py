import json

from api_models.hh_api import HeadHunterAPI
from api_models.sj_api import SuperJobAPI
from models.vacancy import Vacancy
from settings import MENU


class Menu:

    __menu = MENU

    def __call__(self, *args, **kwargs):
        start = True
        # total_vacancies = 0

        # Выводим первое меню
        while True:
            if start:   # Возможно этого блока со start можно избежать
                # query: str = 'django'
                query: str = input("\nВведите поисковый запрос: ").strip()
                start = False
            # else:
            #     print(f'\nВаш запрос: {query}')

            # -----------  Выводим меню 1 уровня  -----------
            choice = self.menu_interaction('На каких ресурсах ищем:', self.__menu['level_1'])
            match choice:
                case '1':  # Поиск по запросу на HeadHunter
                    self.case_realization('HeadHunterAPI')
                    # hh_api = HeadHunterAPI()
                    hh_vacancies = hh_api.get_vacancies(query)
                    if hh_vacancies:
                        print(f'По запросу "{query}"')
                        print(f'найдено вакансий: {len(hh_vacancies)} (HeadHunter)')
                        for vacancy in hh_vacancies:
                            Vacancy(**vacancy)
                    else:
                        print(f'\nПо запросу "{query}"'
                              f'\nна HeadHunter ничего не найдено.'
                              f'\nИзмените параметры запроса')
                        continue
                case '2':  # Поиск по запросу на SuperJob
                    sj_api = SuperJobAPI()
                    sj_vacancies = sj_api.get_vacancies(query)
                    # if sj_vacancies:
                    #     print(f'Найдено вакансий: {len(sj_vacancies)} (SuperJob)')
                    break
                case '3':  # Поиск по запросу на HeadHunter и SuperJob
                    hh_api = HeadHunterAPI()
                    # sj_api = SuperJobAPI()
                    hh_vacancies = hh_api.get_vacancies(query)
                    # sj_vacancies = sj_api.get_vacancies(query)
                    if hh_vacancies:  # or hh_vacancies:
                        print(f'Найдено вакансий: {len(hh_vacancies)} (HeadHunter)')
                        # print(f'Найдено вакансий: {len(sj_vacancies)} (SuperJob)')
                        # print(f'Всего вакансий: {len(hh_vacancies) + len(sj_vacancies)}')
                        # break
                    else:
                        print('\nПо вашему запросу на HeadHunter и SuperJob ничего не найдено.'
                              '\nИзмените параметры запроса.')
                        continue
                case '4':  # Новый запрос
                    Vacancy.clear_all_vacancies()  # Перед новым запросом удаляем предыдущие результаты
                    start = True
                    continue
                case '0':  # Выход из программы
                    return

            # -----------  Выводим меню 2 уровня  -----------
            while True:
                choice = self.menu_interaction('Что делаем дальше:', self.__menu['level_2'])
                match choice:
                    case '1':  # Новый запрос
                        # Удаляем предыдущие результаты, очищая список с вакансиями
                        Vacancy.clear_all_vacancies()
                        start = True
                        break
                    case '2':  # Добавить запрос
                        # Добавляем к предыдущим результатам, не очищая уже полученный список с вакансиями
                        start = True
                        break
                    case '4':  # Вывести результаты на экран
                        print(json.dumps(hh_vacancies, indent=4, ensure_ascii=False))
                        for vacancy in Vacancy.get_all_vacancies():
                            print(vacancy)
                        continue
                    case '0':  # Выход из программы
                        return

    @staticmethod
    def menu_interaction(menu_name: str, menu: dict) -> str:
        """Печатает доступные опции меню выбора в консоль.
        :param menu_name: Заголовок меню.
        :param menu: Пункты меню.
        :return: Выбранная опция меню.
        """
        print(f'\n{menu_name}')
        print('\n'.join([f"({key}) {value}" for key, value in menu.items()]))

        while True:
            choice = input('\nВведите номер пункта меню: ')
            if choice not in menu:
                print("\nНеправильный номер. Выберите один из доступных номеров.")
                continue
            return choice

    @classmethod
    def case_realization(cls, class_name: str):
        temp = globals()[class_name]()
        # cls.__class__.__name__ = class_name
        # temp = cls.__class__.__name__
        print(type(temp))
        print(1)
