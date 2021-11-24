import re
import node
from tqdm import tqdm


class validator:
    '''
      Объект класса validator.

      Он нужен для того, чтобы произвести валидацию данных.
      Список всех необработанных записей, а также список валидных и невалидных записей сохраняются в свойства класса.

      Attributes
      ----------
        entries: list[entry]
            Список словарей, в котором хранятся необработанные записи.
        valid_entries: list[entry]
            Список словарей, в котором хранятся валидные записи.
        invalid_entries: list[entry]
            Список словарей, в котором хранятся невалидные записи.
        error_types: entry
            Словарь, в котором хранится статистика ошибок.
        number_degrees: entry
            Словарь, в котором хранится количество повторений каждой ученой степени.
        number_worldviews: entry
            Словарь, в котором хранится количество повторений каждой религии.
    '''
    entries: list[node]
    valid_entries: list[node]
    invalid_entries: list[node]
    error_types: node
    number_degrees: node
    number_worldviews: node

    def __init__(self, entries: list) -> None:
        '''
            Инициализирует экземпляр класса validator.

            Parameters
            ----------
              entries: list
                Список словарей, в котором хранятся необработанные записи.
        '''
        self.entries = []
        for entry in entries:
            self.entries.append(entry)
        self.valid_entries = []
        self.invalid_entries = []
        self.error_types = {
            "telephone": 0,
            "weight": 0,
            "inn": 0,
            "passport_series": 0,
            "occupation": 0,
            "age": 0,
            "academic_degree": 0,
            "worldview": 0,
            "address": 0
        }
        self.number_degrees = {}
        self.number_worldviews = {}

    def get_valid_entries(self) -> list:
        '''
          Возвращает валидные записи.

          Returns
          -------
            list:
              Список словарей.
        '''
        return self.valid_entries

    def get_count_valid_entries(self) -> int:
        '''
          Возвращает количество валидных записей.

          Returns
          -------
            int:
              Целочисленный результат количества словарей в списке.
        '''
        return len(self.valid_entries)

    def get_count_invalid_entries(self) -> int:
        '''
          Возвращает количество невалидных записей.

          Returns
          -------
            int:
              Целочисленный результат количества словарей в списке.
        '''
        return len(self.invalid_entries)

    def get_error_types(self) -> dict:
        '''
          Возвращает словарь по типам ошибок.

          Returns
          -------
            dict:
              Словарь по типам ошибок
        '''
        return self.error_types

    def parse(self) -> None:
        '''
          Выполняет обработку ствойства entries.

          Если словарь валидный, то добавляет словарь в ствойство valid_entries.
          Если словарь невалидный, то добавляет словарь в ствойство invalid_entries.
          И изменяет статистику ошибок в ствойстве error_types.
        '''
        for entry in self.entries and tqdm(self.entries):
            key_list = self.parse_entry(entry)
            if not key_list:
                self.valid_entries.append(entry)
            else:
                self.invalid_entries.append(entry)
                for key in key_list:
                    self.error_types[key] += 1

    def parse_entry(self, entry: dict) -> list[str]:
        '''
          Выполняет обработку отдельного элемента списка .

          Если словарь валидный, то будет возвращен пустой список.

          Parameters
          ----------
            entry: dict
              Словарь, с необработанными записями.

          Returns
          -------
            list[str]:
              Список ключей с невалидными значениями.
        '''
        keys = []
        for key in entry.keys():
            self.calculate_repetitions(key, entry[key])
        for key in entry.keys():
            if not self.check(key, entry[key]):
                keys.append(key)
        return keys

    def check(self, key: str, value: str) -> bool:
        '''
          Выполняет проверку строки.

          Если строка валидна, возвращает True.

          Parameters
          ----------
            key: str
              Строка в качестве флага.
            value: str
              Строка, с проверяемым значением.
          Returns
          -------
            bool:
              Булевый результат проверки.
        '''
        pattern = ''
        if key == 'telephone':
            pattern = '^\\+[0-9]-\\([0-9]{3}\\)-[0-9]{3}-[0-9]{2}-[0-9]{2}$'
        elif key == 'weight':
            try:
                float_weight = float(value)
                return 200 > float_weight > 40
            except ValueError:
                return False
        elif key == 'inn':
            pattern = '^\\d{12}$'
        elif key == 'passport_series':
            pattern = '^\\d{2}\\s\\d{2}$'
        elif key == 'occupation':
            pattern = '^[а-яА-Яa-zA-Z]+([\\s|-][а-яА-Яa-zA-Z]+|$)$'
        elif key == 'age':
            try:
                int_age = int(value)
                return int_age >= 18 and int_age < 120
            except ValueError:
                return False
        elif key == 'academic_degree':
            if self.number_degrees[value] < 200:
                return False
            pattern = '^[а-яА-Я]+([\\s|-][а-яА-Я]+|$)$'
        elif key == 'worldview':
            if self.number_worldviews[value] < 200:
                return False
            pattern = '^[а-яА-Я]+([\\s|-][а-яА-Я]+|$)$'
        elif key == 'address':
            pattern = '^[а-яА-Я]+[\\s|\\.]+[а-яА-Я\\s]+([0-9-]+[а-я]+\\s[0-9]+|\\s[0-9]+$)'
        if re.match(pattern, value):
            return True
        return False

    def calculate_repetitions(self, key: str, value: str) -> None:
        '''
          Выполняет подсчет значений по ключам(academic_degree и worldview) и сохраняет их в словарь.

          Parameters
          ----------
            key: str
              Строка в качестве флага.
            value: str
              Строка в качестве ключа в словаре.
        '''
        if key == 'academic_degree':
            if value in self.number_degrees:
                self.number_degrees[value] += 1
            else:
                self.number_degrees[value] = 1
        if key == 'worldview':
            if value in self.number_worldviews:
                self.number_worldviews[value] += 1
            else:
                self.number_worldviews[value] = 1
