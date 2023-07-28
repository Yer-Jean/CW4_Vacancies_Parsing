from models.vacancy import Vacancy
from settings import MENU
from utils.search_filter import SearchFilter


class Menu:

    __menu = MENU

    def __call__(self, *args, **kwargs):
        start_search = True
        start_filter = True
        search_or_filter = SearchFilter()
        # Выводим первое меню
        while True:
            if start_search:
                # -----------  Выводим начальное меню  -----------
                choice: str = self.menu_interaction(self.__menu['titles'][0], self.__menu['level_0'])
                match choice:
                    case '1':  # Ввести запрос
                        # query: str = 'django'
                        query: str = input("\nВведите поисковый запрос: ").strip()
                        start_search = False
                    case '0':  # Выход из программы
                        return

            # -----------  Выводим меню 1 уровня  -----------
            choice: str = self.menu_interaction(self.__menu['titles'][0], self.__menu['level_1'])
            match choice:
                case '1':  # Поиск по запросу на HeadHunter
                    if not search_or_filter.search_processing(class_names=['HeadHunterAPI'], query=query):
                        continue
                case '2':  # Поиск по запросу на SuperJob
                    if not search_or_filter.search_processing(class_names=['SuperJobAPI'], query=query):
                        continue
                case '3':  # Поиск по запросу и на HeadHunter, и на SuperJob
                    if not search_or_filter.search_processing(class_names=['HeadHunterAPI', 'SuperJobAPI'],
                                                              query=query):
                        continue
                case '4':  # Новый запрос
                    Vacancy.clear_all_vacancies()  # Перед новым запросом удаляем предыдущие результаты
                    SearchFilter.total_vacancies = 0  # и обнуляем счетчик
                    start_search = True
                    continue
                case '0':  # Выход из программы
                    return

            # -----------  Выводим меню 2 уровня  -----------
            while True:
                choice: str = self.menu_interaction(self.__menu['titles'][1], self.__menu['level_2'])
                match choice:
                    case '1':  # Новый запрос
                        # Удаляем предыдущие результаты, очищая список с вакансиями
                        Vacancy.clear_all_vacancies()
                        SearchFilter.total_vacancies = 0
                        start_search = True
                        break
                    case '2':  # Добавить запрос
                        # Добавляем к предыдущим результатам, не очищая уже полученный список с вакансиями
                        start_search = True
                        break
                    case '8':  # Вывести результаты на экран
                        # print(json.dumps(vacancies, indent=4, ensure_ascii=False))
                        for vacancy in Vacancy.get_all_vacancies():
                            print(vacancy)
                        continue
                    case '0':  # Выход из программы
                        return

                # -----------  Выводим меню 3 уровня  -----------
                while True:
                    if start_filter:  # Возможно этого блока со start можно избежать
                        # SearchFilter.filter_keyword: str = 'Москва'
                        SearchFilter.filter_keyword = input("\nВведите слова для фильтра: ").strip()
                        search_or_filter.filter_processing()
                        start_filter = False

                    choice: str = self.menu_interaction(self.__menu['titles'][2], self.__menu['level_3'])
                    match choice:
                        case '1':  # Новый фильтр
                            SearchFilter.filtered_vacancies.clear()
                            start_filter = True
                            continue
                            # filter_keyword: str = input("\nВведите слова для фильтра: ").strip()
                            # if not search_or_filter.filter_processing(filter_keyword):
                            #     continue
                        case '3':  # Новый фильтр
                            SearchFilter.filtered_vacancies.clear()
                            start_filter = True
                            break
                        case '8':  # Вывести результаты на экран
                            # print(json.dumps(vacancies, indent=4, ensure_ascii=False))
                            for vacancy in SearchFilter.filtered_vacancies:
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
            choice: str = input('\nВведите номер пункта меню: ')
            if choice not in menu:
                print("\nНеправильный номер. Выберите один из доступных номеров.")
                continue
            return choice
