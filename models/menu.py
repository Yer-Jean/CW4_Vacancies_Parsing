import json

from models.hh_api import HeadHunterAPI
from models.vacancy import Vacancy


class Menu:

    MENU = {
        'level_1': {
            '1': 'HeadHunter',
            '2': 'SuperJob',
            '3': 'HeadHunter и SuperJob',
            '4': 'Новый запрос\n----------------------',
            '0': 'Выход из программы'
        },
        'level_2': {
            '1': 'Новый запрос',
            '2': 'Добавить запрос',
            '3': 'Фильтровать результаты',
            '4': 'Вывести результаты на экран',
            '5': 'Сохранить результаты в файл\n-------------------------------',
            '0': 'Выход из программы'
        },
        'Level_3': {
            '1': 'Сбросить фильтр',
            '2': 'Добавить фильтр',
            '8': 'Вывести результаты на экран',
            '9': 'Сохранить результаты в файл\n-------------------------------',
            '0': 'Выход из программы'
        }
    }

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
            choice = self.menu_interaction('На каких ресурсах ищем:', self.MENU['level_1'])
            match choice:
                case '1':  # Поиск по запросу на HeadHunter
                    hh_api = HeadHunterAPI()
                    hh_vacancies = hh_api.get_vacancies(query)
                    if hh_vacancies:
                        print(f'По запросу "{query}"')
                        print(f'найдено вакансий: {len(hh_vacancies)} (HeadHunter)')
                        for vacancy in hh_vacancies:
                            Vacancy(**vacancy)
                    else:
                        print(f'\nПо вашему запросу "{query}"'
                              f'\nна HeadHunter ничего не найдено.'
                              f'\nИзмените параметры запроса')
                        continue
                case '2':  # Поиск по запросу на SuperJob
                    # sj_api = SuperJobAPI()
                    # sj_vacancies = sj_api.get_vacancies(query)
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
                    Vacancy.clear_all_vacancies()
                    start = True
                    # Удаляем предыдущие результаты
                    continue
                case '0':  # Выход из программы
                    return

            # -----------  Выводим меню 2 уровня  -----------
            while True:
                choice = self.menu_interaction('Что делаем дальше:', self.MENU['level_2'])
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
        while True:
            print(f'\n{menu_name}')
            print('\n'.join([f"({key}) {value}" for key, value in menu.items()]))
            choice = input('\nВыберите одну из опций: ')
            if choice not in menu:
                print("\nВыберите одну из доступных опций.")
                continue
            return choice
