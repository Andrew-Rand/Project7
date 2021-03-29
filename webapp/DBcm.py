# Для соответствия требованиям протокола управления контекстом класс должен иметь
# метод __init__ выполняющий инициализацию
# метод __enter__ выполняющий настройки
# метод __exit__ выполняющий завершающие операции (уборку)


import mysql.connector

class ConnectionError(Exception):
    pass

class CredentialsError(Exception):
    pass

class SQLError(Exception):
    pass

class UseDatabase:

    def __init__(self, config: dict) -> None:  #метод принимает единственный словарь, None  - метод не возвращает значение
        self.configuration = config  # значение аргумента config присваивается атрибуту configuration

    def __enter__(self) -> 'cursor':
        try:
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.connector.errors.InterfaceError as err:
            raise ConnectionError(err)  #таким образом создается авторское исключение, которое потом проверяется в основном коде
        except mysql.connector.errors.ProgrammingError as err:
            raise CredentialsError

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:  #  аргументы кроме self нужны для обработки исключений (особенности протокола управления контекстом)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type is mysql.connector.errors.ProgrammingError:
            raise SQLError(exc_value)


    