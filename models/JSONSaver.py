import json
import os

from settings import SEARCH_RESULTS_FILE


class JSONSaver:
    __result_file = SEARCH_RESULTS_FILE

    def save_to_json(self, data: dict) -> None:
        """Сохраняет данные в JSON-файл"""

        with open(self.__result_file, "a") as f:
            if os.stat(self.__result_file).st_size == 0:  # Проверяем файл на содержимое. Размер = 0 значит пустой
                json.dump([data], f)                      # и можно просто записать в него данные
            else:
                with open(self.__result_file) as json_file:  # Иначе считываем из файла данные
                    data_list = json.load(json_file)
                data_list.append(self.__result_file)                        # добавляем к ним новые
                with open(self.__result_file, "w") as json_file:
                    json.dump(data_list, json_file)           # и записываем всё вместе в файл

    def load_from_json(self) -> list:
        pass

    def add_to_json(self) -> None:
        pass
