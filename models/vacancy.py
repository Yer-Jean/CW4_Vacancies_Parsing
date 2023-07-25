import re


class Vacancy:
    __slots__ = ('vacancy_id',
                 'name',
                 'employer',
                 'city',
                 'employment',
                 'schedule',
                 'salary_from',
                 'salary_to',
                 'experience',
                 'requirement',
                 'url',
                 'source')

    def __init__(self, vacancy_id: str, name: str, employer: str, city: str, employment: str, schedule: str,
                 salary_from: int, salary_to: int, experience: str, requirement: str, url: str, source: str):
        self.vacancy_id: str = vacancy_id
        self.name: str = name
        self.employer: str = employer
        self.city: str = city
        self.employment: str = employment
        self.schedule: str = schedule
        self.salary_from: int = salary_from
        self.salary_to: int = salary_to
        self.experience: str = experience
        self.requirement: str = self.clean_string(requirement)
        self.url: str = url
        self.source: str = source

    def __repr__(self):
        return f'{self.__class__.__name__} = {self.__dict__}'

    @staticmethod
    def clean_string(text: str) -> str:
        """Метод удаляет из строки text HTML-теги и специальные символы
        и возвращает результат в виде очищенной строки"""
        return re.sub(r'\s', ' ', re.sub(r'<.*?>', '', text))


if __name__ == '__main__':

    test_str = '<highlighttext>Python</highlighttext>3 (знание на\nуровне написания'

    # result = re.sub(r'[\n\t\r]', ' ', re.sub(r'<.*?>', '', test_str))
    # result = re.sub(r'\s', ' ', test_str)
    result = re.sub(r'<.*?>', '', test_str)  # Удаляем все html-теги
    # result = test_str.replace('\n', ' ').replace('<.*?>', '')
    print(result)

    title = 'Error 404. Page not found'
    example = re.match(r'(.*)\. (.*?) .*', title, re.M|re.I)
    print(example.group())
    print(example.group(1))
    print(example.group(2))
    print(example.groups)
