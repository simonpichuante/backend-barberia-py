from abc import ABC, abstractmethod

class BaseService(ABC):
    def __init__(self, db):
        self.db = db

    @abstractmethod
    def create(self, payload):
        pass

    @abstractmethod
    def update(self, id_, payload):
        pass

    @abstractmethod
    def delete(self, id_):
        pass

    @abstractmethod
    def get(self, id_):
        pass

    @abstractmethod
    def list(self, **filters):
        pass
