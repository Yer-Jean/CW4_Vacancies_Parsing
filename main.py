import json
import string

from models.hh_api import HeadHunterAPI

MENU = {
    'level_1': {
                '1': 'HeadHunter',
                '2': 'SuperJob',
                '3': 'HeadHunter и SuperJob',
                '9': 'Изменить запрос',
                '0': 'Выход из программы'}
}


def menu_interaction(menu_name: str, menu: dict) -> string:
    """Печатает доступные опции выбора в консоль."""
    while True:
        print(f'\n{menu_name}')
        print('\n'.join([f"({key}) {value}" for key, value in menu.items()]))
        choice = input('\nВыберите одну из опций: ')
        if choice not in MENU['level_1']:
            print("\nВыберите одну из доступных опций.")
            continue
        return choice


def main() -> None:
    start = True

    while True:
        if start:
            # query: str = 'qqqqqqqqq'
            query: str = input("\nВведите поисковый запрос: ")
            start = False
        else:
            print(f'\nВаш запрос: {query}')

        choice = menu_interaction('На каких ресурсах ищем:', MENU['level_1'])
        match choice:
            case '1':
                hh_api = HeadHunterAPI()
                hh_vacancies = hh_api.get_vacancies(query)
                if hh_vacancies:
                    break
            case '2':
                hh_api = HeadHunterAPI()
                hh_vacancies = hh_api.get_vacancies(query)
                if hh_vacancies:
                    break
            case '3':
                hh_api = HeadHunterAPI()
                hh_vacancies = hh_api.get_vacancies(query)
                if hh_vacancies:
                    break
            case '9':
                start = True
                continue
            case '0':
                return

    print(json.dumps(hh_vacancies, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()

    # new_text = response.text.replace('premium', 'premium123')  # Замена имен ключей в строке
    # print(new_text)
    # print(type(response.text))
    # print(len(response.text))
    # # print(type(new_json))
    # new_json = json.loads(new_text) #, object_hook=remove_dot_key

    ################################################################

    # print(f"{response['page']} / {response['pages']}")
    #
    # print(json.dumps(response, indent=4, ensure_ascii=False))
    # print(json.dumps(response_data, indent=4, ensure_ascii=False))
    # print(f"{response_data['page']} / {response_data['pages']}")
