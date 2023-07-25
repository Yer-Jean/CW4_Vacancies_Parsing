from models.menu import Menu


def main() -> None:
    menu = Menu()
    menu()



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
