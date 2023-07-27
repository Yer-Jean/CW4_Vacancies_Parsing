import json

from api_models.hh_api import HeadHunterAPI
from api_models.sj_api import SuperJobAPI
from models.vacancy import Vacancy
from settings import MENU


class Menu:

    __menu = MENU
    total_vacancies = 0

    def __call__(self, *args, **kwargs):
        start = True

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
                    if not self.search_processing(class_names=['HeadHunterAPI'], query=query):
                        continue
                case '2':  # Поиск по запросу на SuperJob
                    if not self.search_processing(class_names=['SuperJobAPI'], query=query):
                        continue
                case '3':  # Поиск по запросу и на HeadHunter и на SuperJob
                    if not self.search_processing(class_names=['HeadHunterAPI', 'SuperJobAPI'], query=query):
                        continue
                case '4':  # Новый запрос
                    Vacancy.clear_all_vacancies()  # Перед новым запросом удаляем предыдущие результаты
                    self.total_vacancies = 0
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
                        self.total_vacancies = 0
                        start = True
                        break
                    case '2':  # Добавить запрос
                        # Добавляем к предыдущим результатам, не очищая уже полученный список с вакансиями
                        start = True
                        break
                    case '4':  # Вывести результаты на экран
                        # print(json.dumps(vacancies, indent=4, ensure_ascii=False))
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
    def search_processing(cls, class_names: list, query: str, **kwargs) -> bool:
        """Обрабатывает запросы на HeadHunter и SuperJob.
        :param class_names: Названия классов API.
        :param query: Поисковый запрос.
        :param kwargs: Параметры API.
        :return: Возвращает True, если вакансии найдены.
        """
        # total_vacancies = 0
        print(f'\nПо запросу "{query}"')

        for class_name in class_names:
            class_api = globals()[class_name]()  # Создаем экземпляр класса class_name
            vacancies = class_api.get_vacancies(query)

            if vacancies:
                num_of_vacancies = len(vacancies)
                # удаляем последние 3 символа от имени класса
                print(f'найдено вакансий на {class_name[:-3]}: {num_of_vacancies}')
                for vacancy in vacancies:
                    Vacancy(**vacancy)
            else:
                print(f'\nна {class_name[:-3]} ничего не найдено.'
                      f'\nИзмените параметры запроса')
            cls.total_vacancies += num_of_vacancies

        print(f'------------------\nВсего вакансий: {cls.total_vacancies}\n')
        return bool(vacancies)
