import re


class Vacancy:
    __all_vacancies: list = []

    __slots__ = ('vacancy_id',
                 'name',
                 'employer',
                 'city',
                 'employment',
                 'schedule',
                 'salary_from',
                 'salary_to',
                 'currency',
                 'experience',
                 'requirement',
                 'url',
                 'source')

    def __init__(self, vacancy_id: str, name: str, employer: str, city: str, employment: str, schedule: str,
                 salary_from: int, salary_to: int, currency: str, experience: str, requirement: str, url: str,
                 source: str):
        self.vacancy_id: str = vacancy_id
        self.name: str = name
        self.employer: str = employer
        self.city: str = city
        self.employment: str = employment
        self.schedule: str = schedule
        self.salary_from: int = salary_from
        self.salary_to: int = salary_to
        self.currency: str = currency
        self.experience: str = experience
        self.requirement: str = self.clean_and_cut_requirement(requirement)
        self.url: str = url
        self.source: str = source

        self.__all_vacancies.append(self)

    @classmethod
    def get_all_vacancies(cls):
        return cls.__all_vacancies

    @classmethod
    def clear_all_vacancies(cls):
        cls.__all_vacancies.clear()

    @staticmethod
    def clean_and_cut_requirement(text: str) -> str:
        """Метод удаляет из строки text HTML-теги и специальные символы и возвращает
        результат в виде очищенной строки максимальной длиной 115 символов."""
        result_string: str = re.sub(r'\s', ' ', re.sub(r'<.*?>', '', text))
        return f'{result_string[:115]}...' if len(result_string) > 115 else result_string

    def __repr__(self):
        return f'{self.__class__.__name__} = {self.__dict__}'

    def __str__(self):
        salary: str = {self.salary_from == 0 and self.salary_to == 0: 'по договоренности',
                       self.salary_from > 0 and self.salary_to == 0: f'от {self.salary_from:,}',
                       self.salary_from == 0 and self.salary_to > 0: f'до {self.salary_to:,}',
                       self.salary_from > 0 and self.salary_to > 0: f'{self.salary_from:,} - {self.salary_to:,}'}[True]
        return f'\nВакансия: {self.name}\nРаботодатель: {self.employer}\nГород {self.city}' \
               f'\nОплата {salary} {self.currency}\nНеобходимый опыт: {self.experience}' \
               f'\nОтрывок из требований по вакансии:\n{self.requirement}' \
               f'\nПолный текст вакансии по ссылке {self.url}\nИсточник - {self.source}'


if __name__ == '__main__':

    test_str = '<highlighttext>Python</highlighttext>3 (знание на\nуровне написания'

    # result = re.sub(r'[\n\t\r]', ' ', re.sub(r'<.*?>', '', test_str))
    # result = re.sub(r'\s', ' ', test_str)
    result = re.sub(r'<.*?>', '', test_str)  # Удаляем все html-теги
    # result = test_str.replace('\n', ' ').replace('<.*?>', '')
    print(result)

    title = 'Error 404. Page not found'
    # example = re.match(r'(.*)\. (.*?) .*', title, re.M|re.I)
    # print(example.group())
    # print(example.group(1))
    # print(example.group(2))
    # print(example.groups)
