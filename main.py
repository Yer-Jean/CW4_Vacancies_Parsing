from models.hh_api import HeadHunterAPI


if __name__ == '__main__':
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies('python')

    # url = 'https://api.hh.ru/vacancies?search_field=name&per_page=5&text=python'
    # url = 'https://api.hh.ru/vacancies'
    # response = requests.get(url, params={'search_field': 'name',
    #                                      'per_page': '5',
    #                                      'text': 'python'}).json()
    # response = requests.get(url, headers={'apikey': API_KEY}, params={'base': currency})
    # response_data = json.loads(response.text)

    ################################################################

    # response = requests.get(url, params={'search_field': 'name',
    #                                      'per_page': '5',
    #                                      'text': 'python'})
    # new_json = json.loads(response.text)  #, object_hook=remove_dot_key)

    # print(json.dumps(new_json, indent=4, ensure_ascii=False))

    #
    # new_text = response.text.replace('premium', 'premium123')
    # print(new_text)
    # print(type(response.text))
    # print(len(response.text))
    # # print(type(new_json))
    # new_json = json.loads(new_text) #, object_hook=remove_dot_key)

    # print(json.dumps(new_json, indent=4, ensure_ascii=False))

    ################################################################

    # print(f"{response['page']} / {response['pages']}")
    #
    # print(json.dumps(response, indent=4, ensure_ascii=False))
    # print(json.dumps(response_data, indent=4, ensure_ascii=False))
    # print(f"{response_data['page']} / {response_data['pages']}")
