import json

from models.hh_api import HeadHunterAPI


class Menu:

    MENU = {
        'level_1_main': {
            '1': 'HeadHunter',
            '2': 'SuperJob',
            '3': 'HeadHunter и SuperJob',
            '9': 'Изменить запрос',
            '0': 'Выход из программы'}
        # 'level_2_main'
    }

    def __call__(self, *args, **kwargs):
        start = True
        # total_vacancies = 0

        # Выводим первое меню
        while True:
            if start:   # Возможно этого блока со start можно избежать
                query: str = 'python django flask'
                # query: str = input("\nВведите поисковый запрос: ").strip()
                start = False
            else:
                print(f'\nВаш запрос: {query}')

            choice = self.menu_interaction('На каких ресурсах ищем:', self.MENU['level_1_main'])
            match choice:
                case '1':
                    hh_api = HeadHunterAPI()
                    hh_vacancies = hh_api.get_vacancies(query)
                    if hh_vacancies:
                        print(f'По запросу "{query}":')
                        print(f'найдено вакансий: {len(hh_vacancies)} (HeadHunter)')
                        break
                case '2':
                    # sj_api = SuperJobAPI()
                    # sj_vacancies = sj_api.get_vacancies(query)
                    # if sj_vacancies:
                    #     print(f'Найдено вакансий: {len(sj_vacancies)} (SuperJob)')
                    break
                case '3':
                    hh_api = HeadHunterAPI()
                    # sj_api = SuperJobAPI()
                    hh_vacancies = hh_api.get_vacancies(query)
                    # sj_vacancies = sj_api.get_vacancies(query)
                    if hh_vacancies:  # or hh_vacancies:
                        print(f'Найдено вакансий: {len(hh_vacancies)} (HeadHunter)')
                        # print(f'Найдено вакансий: {len(sj_vacancies)} (SuperJob)')
                        # print(f'Всего вакансий: {len(hh_vacancies) + len(sj_vacancies)}')
                        break
                case '9':
                    start = True
                    continue
                case '0':
                    return
        print(json.dumps(hh_vacancies, indent=4, ensure_ascii=False))

    @staticmethod
    def menu_interaction(menu_name: str, menu: dict) -> str:
        """Печатает доступные опции меню выбора в консоль.
        :param menu_name:
        :param menu:
        :return:
        """
        while True:
            print(f'\n{menu_name}')
            print('\n'.join([f"({key}) {value}" for key, value in menu.items()]))
            choice = input('\nВыберите одну из опций: ')
            if choice not in menu:
                print("\nВыберите одну из доступных опций.")
                continue
            return choice
