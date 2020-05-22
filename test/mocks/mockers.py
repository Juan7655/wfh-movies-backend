from unittest.mock import ANY

from uuid import uuid4

from sqlalchemy.exc import IntegrityError
from app import database
from app.service import commons


class BaseMock:
    def __init__(self, service, mocker) -> None:
        super().__init__()
        print(f"Importing {ANY}")
        self.service = service
        self.service_name = service.__name__.split(".")[-1]
        self.mocker = mocker
        self.components = set()
        self.expressions = list()
        self.mock_decorator_db()

    def register(self, expression, value):
        component = expression.split('.', maxsplit=1)[0]
        self.components.add(component.split('(')[0])
        self.expressions.append((expression, value))
        return self

    def apply(self):
        for component in self.components:
            self.mocker.patch.object(self.service, component)
        for expression, result in self.expressions:
            self.evaluate_patch(expression=f'{self.service_name}.{expression}', result=result)

    @staticmethod
    def evaluate_patch(expression, result):
        method_name = str(hash(expression)).replace('-', 'n') + str(uuid4()).replace('-', '_')
        exec(f'def fun_{method_name}(result):\n    {expression} = result')
        fun = eval('fun_' + method_name)
        fun(result)

    def mock_decorator_db(self):
        self.mocker.patch.object(database, 'get_db')
        base_expression = 'decorators.db.%s.return_value'
        for m in ['add', 'add_all', 'commit', 'close', 'refresh']:
            self.evaluate_patch(base_expression % m, None)

    @staticmethod
    def filters(n):
        return '.filter(ANY)' * n


class DBMock(BaseMock):
    def __init__(self, mocker) -> None:
        super().__init__(database, mocker)

    def exception(self):
        self.register('get_db.add.side_effect', IntegrityError(None, None, None))
        self.register('get_db.rollback.return_value', None)
        return self.register('get_db.close.return_value', None)


class CommonsMock(BaseMock):

    def __init__(self, mocker) -> None:
        super().__init__(commons, mocker)

    def save_instance(self, result):
        return self.register('save_instance.return_value', result)
